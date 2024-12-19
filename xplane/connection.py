"""""
Connection to xplane ExtPlane plugin
ExtPlane plugin is used to communicate with xplane https://github.com/vranki/ExtPlane
"""

import asyncio
import struct
import json
from time import time, ctime
from common.aioudp import open_local_endpoint, open_local_endpoint

import common.sane_tasks as sane_tasks
from xplane.params import Params
from xplane.params_to_subscribe import udp_params_list


def parse_xplane_dataref(data_line: str):
    type, dataref, value = data_line.split()

    if type == "ui":
        value = int(value) 
    elif type in ["uf", "ud"]:
        value = float(value)
    elif type in ["uia", "ufa"]:
        # arrays
        value = json.loads(value)
    else:
        print("Warning: dataref parse not INPLEMENTED!")
    
    return type, dataref, value


class XPconnection():
    """ connection to ExtPlane plugin """

    def __init__(self) -> None:
        self.host = None
        self.port = None

        self.writer = None
        self.reader = None
        self.reader_task = None
        self.terminate_reader_task = False
        self._is_connecting = False

        self.on_new_data_callback = None 
        self.on_data_exception_callback = None
        self.on_connected_callback = None
        self.on_subscription_failed_callback = None

    async def connect(self, server_address, server_port, on_new_data_callback, on_data_exception_callback):
        """ connect to ExtPlane plugin """
        # remember for reconnect
        self.host = server_address
        self.port = server_port

        await self.disconnect()

        self.on_new_data_callback = on_new_data_callback
        self.on_data_exception_callback = on_data_exception_callback
        self.reader, self.writer = await asyncio.open_connection(server_address, server_port)

        self.reader_task = sane_tasks.spawn(self._handle_read())    

    async def disconnect(self):
        if self.writer:
            self.writer.close()
            try:
                await self.writer.wait_closed()
            except ConnectionError as e:
                print(e)

            self.writer = None

        if self.reader_task:
            self.terminate_reader_task = True
            await self.reader_task
            self.terminate_reader_task = False
            self.reader_task = None
            self.reader = None
        
    async def connect_until_success(self, server_address, server_port, on_new_data_callback, on_data_exception_callback, retry_interval=1):
        while True:
            try:
                print(f"connecting to xplane: {server_address}:{server_port}...")
                await self.connect(server_address, server_port, on_new_data_callback, on_data_exception_callback)
                print(f"connected to xplane: {server_address}:{server_port} !")

                self._is_connecting = False

                if self.on_connected_callback:
                    self.on_connected_callback()

                break
            except (ConnectionRefusedError, OSError) as e:
                print(f"Could not connect to xplane: {server_address}:{server_port} !")
                print(f"retrying...")
                await asyncio.sleep(retry_interval)

    async def _handle_read(self):
        try:
            # read first 3 welcome lines
            l = await self.reader.readline()
            l = await self.reader.readline()
            l = await self.reader.readline()

            while not self.terminate_reader_task or self.reader.at_eof():
                data = await self.reader.readline()
                if not data:
                    # connection closed
                    break

                data = data.decode()

                # extplane warning received
                if data.startswith("EXTP"):
                    print(data)

                    if data.startswith("EXTPLANE-WARNING Can't find dataref "):
                        dataref = data.split("EXTPLANE-WARNING Can't find dataref ")[1].rstrip()
                        if self.on_subscription_failed_callback:
                            await self.on_subscription_failed_callback(Params[dataref])

                    continue

                # data received
                type, dataref, value = parse_xplane_dataref(data)

                if self.on_new_data_callback:
                    self.on_new_data_callback(type, dataref, value) 

            # recursive reconnect
            if self._is_connecting is False:
                self._auto_reconnect()

        except Exception as ex:
            if self.on_data_exception_callback:
                self.on_data_exception_callback(ex)

    def _auto_reconnect(self):
        self._is_connecting = True

        async def _reconnect():
            await self.disconnect()

            await self.connect_until_success(
                self.host, self.port, self.on_new_data_callback, self.on_data_exception_callback
            )
        
        sane_tasks.spawn(_reconnect())

    async def send_string(self, msg: str):
        if not self.writer:
            print("not connected to xplane!")
            return 

        if self._is_connecting:
            print("reconnecting")
            return  

        if self.writer.is_closing():
            self._auto_reconnect()

        msg += "\n"
        self.writer.write(msg.encode())
        await self.writer.drain()
        await asyncio.sleep(0) # NOTE: needed to call event loop !


class XPconnectionUDP():
    """ connection to native XPlane udp protocol """

    def __init__(self) -> None:
        self.remote_host = "127.0.0.1"
        self.remote_port = 49000

        self.listen_host = "127.0.0.1"
        self.listen_port = 62222 

        self.sock = None
        self.udp_read_task = None
        self.terminate_reader_task = False

        self.on_new_data_callback = None 
        self.on_data_exception_callback = None

        self.last_packet_received_time = None

    async def connect(self, remote_address, remote_port, on_new_data_callback, on_data_exception_callback, listen_port=62222):
        """ connect to ExtPlane plugin """
        # remember for reconnect
        self.remote_host = remote_address
        self.remote_port = remote_port
        self.listen_port = listen_port

        self.on_new_data_callback = on_new_data_callback
        self.on_data_exception_callback = on_data_exception_callback
        await self.start_read_task()

    async def start_read_task(self):
        # self.sock = await open_local_endpoint(self.listen_host, self.listen_port)
        self.sock = await open_local_endpoint(host='127.0.0.1', port=self.listen_port)
        self.udp_read_task = sane_tasks.spawn(self.read_udp_task())    

    async def read_udp_task(self):
        while not self.terminate_reader_task:
            try:
                data, (host, port) = await self.sock.receive()
                # while True:
                #     try:
                #         data, (host, port) = self.sock.receive_nowait()
                #     except asyncio.QueueEmpty:
                #         break
            except IOError:
                # open new connection if prev connection was reset
                await self.start_read_task()
                break

            self.last_packet_received_time = time()

            try:
                values = data[5:]
                num_values = int(len(values) / 8)
                received_vals = {}

                for i in range(num_values):
                    dref_info = data[(5 + 8 * i):(5 + 8 * (i + 1))]
                    (index, value) = struct.unpack("<if", dref_info)
                    param = udp_params_list[index]
                    received_vals[param] = value
                
                self.on_new_data_callback(received_vals)
            except Exception as ex:
                if self.on_data_exception_callback:
                    self.on_data_exception_callback(ex)

    def set_param(self, param, value):
        msg = struct.pack(
            '<4sxf500s', 
            b'DREF',
            value,
            str(param).encode('utf-8')
        )

        try:
            self.sock.send(msg, (self.remote_host, self.remote_port))
        except IOError as e:
            print(e)

    def subscribe_to_param(self, param, freq=1):
        freq = 1 if freq is None else freq

        index = udp_params_list.index(param)

        msg = struct.pack(
            "<4sxii400s", 
            b'RREF',
            freq,
            index,
            str(param).encode('utf-8')
        )

        try:
            self.sock.send(msg, (self.remote_host, self.remote_port)) 
        except IOError as e:
            print(e)

