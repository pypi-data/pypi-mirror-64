import asyncio
import struct


# Default event handlers
async def _tlv_packetizer(reader):
    header = await reader.readexactly(3)
    pkt_type, pkt_len = struct.unpack(">BH", header)
    payload = await reader.readexactly(pkt_len)

    return header + payload


async def _disconnect_callback():
    pass


async def _connect_callback():
    pass


async def _recv_callback(message):
    pass


async def _send_callback(message):
    pass


class AsyncStreamClient:
    def __init__(self,
                 connect_callback=None,
                 recv_callback=None,
                 send_callback=None,
                 disconnect_callback=None,
                 packetizer=_tlv_packetizer):
        self.server = None
        self.connect_callback = connect_callback or _connect_callback
        self.recv_callback = recv_callback or _recv_callback
        self.send_callback = send_callback or _send_callback
        self.disconnect_callback = disconnect_callback or _disconnect_callback
        self.packetizer = packetizer
        self.event_loop = asyncio.get_event_loop()
        self.streams = {}
        self.writer = None
        self.reader = None
        self.server_addr = None
        self.sock_addr = None
        self.connected = False

    async def connect(self, ip, port, socks=None):
        if self.connected:
            await self.close()

        if socks:
            import aiosocks
            proxy = aiosocks.Socks5Addr('127.0.0.1', 9050)
            self.reader, self.writer = await aiosocks.open_connection(proxy=proxy, proxy_auth=None, dst=(ip, port), remote_resolve=True)
        else:
            self.reader, self.writer = await asyncio.open_connection(ip, port, loop=self.event_loop)
        self.connected = True
        self.server_addr = self.writer.get_extra_info('peername')
        self.sock_addr = self.writer.get_extra_info('sockname')
        await self.connect_callback()
        self.event_loop.create_task(self._recv())

    async def send(self, message):
        self.writer.write(bytes(message))
        await self.writer.drain()
        await self.send_callback(message)

    async def _recv(self):
        while self.connected:
            try:
                pkt = await self.packetizer(self.reader)
                await self.recv_callback(pkt)
            except (asyncio.IncompleteReadError, ConnectionResetError):
                await self.disconnect_callback()
                self.connected = False

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()
