"""""
Connection to xplane ExtPlane plugin
ExtPlane plugin is used to communicate with xplane https://github.com/vranki/ExtPlane
"""

import asyncio
import json

import sane_tasks
from xplane.params import Params


def parse_xplane_dataref(data_line: str):

    type, dataref, value = data_line.split()
    # type = type.decode()
    # dataref = dataref.decode()

    if type == "ui":
        value = int(value) 
    elif type in ["uf", "ud"]:
        value = float(value)
    elif type in ["uia", "ufa"]:
        # value = value.decode()
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
        
    async def connect_until_success(self, server_address, server_port, on_new_data_callback, on_data_exception_callback):
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
                await asyncio.sleep(0.5)

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

