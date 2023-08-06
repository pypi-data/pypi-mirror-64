import asyncio
import functools
import inspect
import logging
import weakref
from abc import ABC, abstractmethod
from collections.abc import Awaitable
from concurrent.futures import ThreadPoolExecutor

import zmq
import zmq.asyncio

from .exceptions import QuLabRPCError, QuLabRPCServerError, QuLabRPCTimeout
from .serialize import pack, unpack
from .utils import acceptArg, randomID

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

# message type

RPC_REQUEST = b'\x01'
RPC_RESPONSE = b'\x02'
RPC_PING = b'\x03'
RPC_PONG = b'\x04'
RPC_CANCEL = b'\x05'
RPC_SHUTDOWN = b'\x06'


class RPCMixin(ABC):
    __pending = None
    __tasks = None

    @property
    def pending(self):
        if self.__pending is None:
            self.__pending = {}
        return self.__pending

    @property
    def tasks(self):
        if self.__tasks is None:
            self.__tasks = {}
        return self.__tasks

    def start(self):
        pass

    def stop(self):
        pass

    def close(self):
        self.stop()
        for task in list(self.tasks.values()):
            task.cancel()
        self.tasks.clear()
        for fut, timeout in list(self.pending.values()):
            fut.cancel()
            timeout.cancel()
        self.pending.clear()

    def createTask(self, msgID, coro, timeout=0):
        """
        Create a new task for msgID.
        """
        if timeout > 0:
            coro = asyncio.wait_for(coro, timeout)
        task = asyncio.ensure_future(coro, loop=self.loop)
        self.tasks[msgID] = task

        def clean(fut, msgID=msgID):
            if msgID in self.tasks:
                del self.tasks[msgID]

        task.add_done_callback(clean)

    def cancelTask(self, msgID):
        """
        Cancel the task for msgID.
        """
        if msgID in self.tasks:
            self.tasks[msgID].cancel()

    def createPending(self, addr, msgID, timeout=1, cancelRemote=True):
        """
        Create a future for request, wait response before timeout.
        """
        fut = self.loop.create_future()
        self.pending[msgID] = (fut,
                               self.loop.call_later(timeout,
                                                    self.cancelPending, addr,
                                                    msgID, cancelRemote))

        def clean(fut, msgID=msgID):
            if msgID in self.pending:
                del self.pending[msgID]

        fut.add_done_callback(clean)

        return fut

    def cancelPending(self, addr, msgID, cancelRemote):
        """
        Give up when request timeout and try to cancel remote task.
        """
        if msgID in self.pending:
            fut, timeout = self.pending[msgID]
            if cancelRemote:
                self.cancelRemoteTask(addr, msgID)
            if not fut.done():
                fut.set_exception(QuLabRPCTimeout('Time out.'))

    def cancelRemoteTask(self, addr, msgID):
        """
        Try to cancel remote task.
        """
        asyncio.ensure_future(self.sendto(RPC_CANCEL + msgID, addr),
                              loop=self.loop)

    @property
    @abstractmethod
    def loop(self):
        """
        Event loop.
        """

    @abstractmethod
    async def sendto(self, data, address):
        """
        Send message to address.
        """

    __rpc_handlers = {
        RPC_PING: 'on_ping',
        RPC_PONG: 'on_pong',
        RPC_REQUEST: 'on_request',
        RPC_RESPONSE: 'on_response',
        RPC_CANCEL: 'on_cancel',
        RPC_SHUTDOWN: 'on_shutdown',
    }

    def handle(self, source, data):
        """
        Handle received data.

        Should be called whenever received data from outside.
        """
        msg_type, data = data[:1], data[1:]
        log.debug(f'received request {msg_type} from {source}')
        handler = self.__rpc_handlers.get(msg_type, None)
        if handler is not None:
            getattr(self, handler)(source, data)

    async def ping(self, addr, timeout=1):
        await self.sendto(RPC_PING, addr)
        fut = self.createPending(addr, addr, timeout, False)
        try:
            return await fut
        except QuLabRPCTimeout:
            return False

    async def pong(self, addr):
        await self.sendto(RPC_PONG, addr)

    async def request(self, address, msgID, msg):
        log.debug(f'send request {address}, {msgID.hex()}, {msg}')
        await self.sendto(RPC_REQUEST + msgID + msg, address)

    async def response(self, address, msgID, msg):
        log.debug(f'send response {address}, {msgID.hex()}, {msg}')
        await self.sendto(RPC_RESPONSE + msgID + msg, address)

    async def shutdown(self, address):
        await self.sendto(RPC_SHUTDOWN, address)

    def on_request(self, source, data):
        """
        Handle request.

        Overwrite this method on server.
        """

    def on_response(self, source, data):
        """
        Handle response.

        Overwrite this method on client.
        """

    def on_ping(self, source, data):
        log.debug(f"received ping from {source}")
        asyncio.ensure_future(self.pong(source), loop=self.loop)

    def on_pong(self, source, data):
        log.debug(f"received pong from {source}")
        if source in self.pending:
            fut, timeout = self.pending[source]
            timeout.cancel()
            if not fut.done():
                fut.set_result(True)

    def on_cancel(self, source, data):
        msgID = data[:20]
        self.cancelTask(msgID)

    def on_shutdown(self, source, data):
        if self.is_admin(source, data):
            raise SystemExit(0)

    def is_admin(self, source, data):
        return True


class RPCClientMixin(RPCMixin):
    _client_defualt_timeout = 10

    def set_timeout(self, timeout=10):
        self._client_defualt_timeout = timeout

    def remoteCall(self, addr, methodNane, args=(), kw={}):
        if 'timeout' in kw:
            timeout = kw['timeout']
        else:
            timeout = self._client_defualt_timeout
        msg = pack((methodNane, args, kw))
        msgID = randomID()
        asyncio.ensure_future(self.request(addr, msgID, msg), loop=self.loop)
        return self.createPending(addr, msgID, timeout)

    def on_response(self, source, data):
        """
        Client side.
        """
        msgID, msg = data[:20], data[20:]
        if msgID not in self.pending:
            return
        fut, timeout = self.pending[msgID]
        timeout.cancel()
        result = unpack(msg)
        if not fut.done():
            if isinstance(result, Exception):
                fut.set_exception(result)
            else:
                fut.set_result(result)


class RPCServerMixin(RPCMixin):
    def _unpack_request(self, msg):
        try:
            method, args, kw = unpack(msg)
        except:
            raise QuLabRPCError("Could not read packet: %r" % msg)
        return method, args, kw

    @property
    def executor(self):
        return None

    @abstractmethod
    def getRequestHandler(self, methodNane, source, msgID):
        """
        Get suitable handler for request.

        You should implement this method yourself.
        """

    def on_request(self, source, data):
        """
        Received a request from source.
        """
        msgID, msg = data[:20], data[20:]
        method, args, kw = self._unpack_request(msg)
        self.createTask(msgID,
                        self.handle_request(source, msgID, method, *args,
                                            **kw),
                        timeout=kw.get('timeout', 0))

    async def handle_request(self, source, msgID, method, *args, **kw):
        """
        Handle a request from source.
        """
        try:
            func = self.getRequestHandler(method, source=source, msgID=msgID)
            if 'timeout' in kw and not acceptArg(func, 'timeout'):
                del kw['timeout']
            if inspect.iscoroutinefunction(func):
                result = await func(*args, **kw)
            else:
                result = await self.loop.run_in_executor(
                    self.executor, functools.partial(func, *args, **kw))
                if isinstance(result, Awaitable):
                    result = await result
        except QuLabRPCError as e:
            result = e
        except Exception as e:
            result = QuLabRPCServerError.make(e)
        msg = pack(result)
        await self.response(source, msgID, msg)


class ZMQServer(RPCServerMixin):
    def __init__(self, bind='*', port=None, loop=None):
        self.zmq_main_task = None
        self.zmq_ctx = None
        self.zmq_socket = None
        self.bind = bind
        self._port = 0 if port is None else port
        self._loop = loop or asyncio.get_event_loop()
        self._module = None

    def set_module(self, mod):
        self._module = mod

    async def sendto(self, data, address):
        self.zmq_socket.send_multipart([address, data])

    def getRequestHandler(self, methodNane, **kw):
        path = methodNane.split('.')
        ret = getattr(self._module, path[0])
        for n in path[1:]:
            ret = getattr(ret, n)
        return ret

    @property
    def loop(self):
        return self._loop

    @property
    def port(self):
        return self._port

    def set_socket(self, sock):
        self.zmq_socket = sock

    def start(self):
        super().start()
        self.zmq_ctx = zmq.asyncio.Context.instance()
        self.zmq_main_task = asyncio.ensure_future(self.run(), loop=self.loop)

    def stop(self):
        if self.zmq_main_task is not None and not self.zmq_main_task.done():
            self.zmq_main_task.cancel()
        super().stop()

    async def run(self):
        with self.zmq_ctx.socket(zmq.ROUTER, io_loop=self._loop) as sock:
            sock.setsockopt(zmq.LINGER, 0)
            addr = f"tcp://{self.bind}" if self._port == 0 else f"tcp://{self.bind}:{self._port}"
            if self._port != 0:
                sock.bind(addr)
            else:
                self._port = sock.bind_to_random_port(addr)
            self.set_socket(sock)
            while True:
                addr, data = await sock.recv_multipart()
                log.debug('received data from %r' % addr.hex())
                self.handle(addr, data)


class _ZMQClient(RPCClientMixin):
    def __init__(self, addr, timeout=10, loop=None):
        self._loop = loop or asyncio.get_event_loop()
        self.set_timeout(timeout)
        self.addr = addr
        self._ctx = zmq.asyncio.Context()
        self.zmq_socket = self._ctx.socket(zmq.DEALER, io_loop=self._loop)
        self.zmq_socket.setsockopt(zmq.LINGER, 0)
        self.zmq_socket.connect(self.addr)
        self.zmq_main_task = None
        asyncio.ensure_future(asyncio.shield(self.run(weakref.proxy(self))),
                              loop=self.loop)

    def __del__(self):
        self.zmq_socket.close()
        self.close()
        self.zmq_main_task.cancel()

    @property
    def loop(self):
        return self._loop

    async def ping(self, timeout=1):
        return await super().ping(self.addr, timeout=timeout)

    async def shutdownServer(self):
        return await super().shutdown(self.addr)

    async def sendto(self, data, addr):
        await self.zmq_socket.send_multipart([data])

    @staticmethod
    async def run(client):
        async def main():
            while True:
                data, = await client.zmq_socket.recv_multipart()
                client.handle(client.addr, data)

        client.zmq_main_task = asyncio.ensure_future(main(), loop=client.loop)
        try:
            await client.zmq_main_task
        except asyncio.CancelledError:
            pass


class ZMQRPCCallable:
    def __init__(self, methodNane, owner):
        self.methodNane = methodNane
        self.owner = owner

    def __call__(self, *args, **kw):
        fut = self.owner._zmq_client.remoteCall(self.owner._zmq_client.addr,
                                                self.methodNane, args, kw)
        fut.add_done_callback(self.owner._remoteCallDoneCallbackHook)
        return fut

    def __getattr__(self, name):
        return ZMQRPCCallable(f"{self.methodNane}.{name}", self.owner)


class ZMQClient():
    def __init__(self, addr, timeout=10, loop=None):
        self._zmq_client = _ZMQClient(addr, timeout=timeout, loop=loop)
        self.ping = self._zmq_client.ping
        self.shutdownServer = self._zmq_client.shutdownServer

    def __getattr__(self, name):
        return ZMQRPCCallable(name, self)

    def _remoteCallDoneCallbackHook(self, fut):
        """overwrite this method"""
        pass
