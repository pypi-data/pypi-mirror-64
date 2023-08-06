import asyncio
import struct
from argparse import Namespace


# Default event handlers
async def _tlv_packetizer(addr, reader):
    header = await reader.readexactly(3)
    pkt_type, pkt_len = struct.unpack(">BH", header)
    payload = await reader.readexactly(pkt_len)

    return header + payload


async def _disconnect_callback(addr):
    pass


async def _connect_callback(addr):
    pass


async def _recv_callback(addr, message):
    pass


async def _send_callback(addr, message):
    pass


# Server
class AsyncStreamServer:
    def __init__(self,
                 ip,
                 port,
                 connect_callback=None,
                 recv_callback=None,
                 send_callback=None,
                 disconnect_callback=None,
                 packetizer=_tlv_packetizer):
        self.server = None
        self.ip = ip
        self.port = port
        self.connect_callback = connect_callback or _connect_callback
        self.recv_callback = recv_callback or _recv_callback
        self.send_callback = send_callback or _send_callback
        self.disconnect_callback = disconnect_callback or _disconnect_callback
        self.packetizer = packetizer
        self.event_loop = asyncio.get_event_loop()
        self.streams = {}

    async def handle_new_stream(self, reader, writer):
        done = False
        client_addr = writer.get_extra_info('peername')
        self.streams[client_addr] = Namespace(reader=reader, writer=writer)
        await self.connect_callback(client_addr)

        while not done:
            try:
                # Receive on socket
                pkt = await self.packetizer(client_addr, reader)
                await self.recv_callback(client_addr, pkt)
            except (asyncio.IncompleteReadError, ConnectionResetError):
                await self.disconnect_callback(client_addr)
                writer.close()
                del reader
                del writer
                del self.streams[client_addr]
                done = True

    async def send(self, addr, reply):
        writer = self.streams[addr].writer
        writer.write(bytes(reply))
        await writer.drain()
        await self.send_callback(addr, reply)

    def start(self):
        server_coroutine = asyncio.start_server(self.handle_new_stream, self.ip, self.port)
        self.server = self.event_loop.run_until_complete(server_coroutine)
        # print('Serving on {}'.format(self.server.sockets[0].getsockname()))  # TODO fix logging

    def stop(self):
        # print('Closing server')
        self.server.close()
        self.event_loop.run_until_complete(self.server.wait_closed())

