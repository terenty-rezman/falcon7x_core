import binascii
import platform
import socket
import struct
import asyncio
from common.aioudp import open_local_endpoint, open_local_endpoint

from xplane import master

# From https://github.com/charlylima/XPlaneUDP/blob/master/XPlaneUdp.py
#  and https://gitlab.bliesener.com/jbliesener/PiDisplay/-/blob/master/XPlaneUDP.py


class XPlaneIpNotFound(Exception):
    args = "Could not find any running xplane instance in network."


def find_xp(wait=3.0):
    """
    Waits for X-Plane to startup, and returns IP (and other) information
    about the first running X-Plane found.

    wait: floating point, maximum seconds to wait for beacon.
    """

    MCAST_GRP = '239.255.1.1'  # Standard multicast group
    MCAST_PORT = 49707  # (MCAST_PORT was 49000 for XPlane10)

    # Set up to listen for a multicast beacon
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if platform.system() == 'Windows':
        sock.bind(('', MCAST_PORT))
    else:
        sock.bind((MCAST_GRP, MCAST_PORT))
    mreq = struct.pack("=4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    if wait > 0:
        sock.settimeout(wait)

    beacon_data = {}
    while not beacon_data:
        try:
            packet, sender = sock.recvfrom(15000)
            header = packet[0:5]
            if header != b"BECN\x00":
                # We assume X-Plane is the only multicaster on this port
                print("Unknown packet from " + sender[0])
                print(str(len(packet)) + " bytes")
                print(packet)
                print(binascii.hexlify(packet))

            else:
                # header matches, so looks like the X-Plane beacon
                # * Data
                data = packet[5:21]

                # X-Plane documentation says:
                # struct becn_struct
                # {
                #    uchar beacon_major_version;    // 1 at the time of X-Plane 10.40, 11.55
                #    uchar beacon_minor_version;    // 1 at the time of X-Plane 10.40, 2 for 11.55
                #    xint application_host_id;      // 1 for X-Plane, 2 for PlaneMaker
                #    xint version_number;           // 104014 is X-Plane 10.40b14, 115501 is 11.55r2
                #    uint role;                     // 1 for master, 2 for extern visual, 3 for IOS
                #    ushort port;                   // port number X-Plane is listening on
                #    xchr    computer_name[500];    // the hostname of the computer
                #    ushort  raknet_port;           // port number the X-Plane Raknet clinet is listening on
                # };

                (beacon_major_version, beacon_minor_version, application_host_id,
                 xplane_version_number, role, port) = struct.unpack("<BBiiIH", data)

                computer_name = packet[21:]  # Python3, these are bytes, not a string
                computer_name = computer_name.split(b'\x00')[0]  # get name upto, but excluding first null byte
                (raknet_port, ) = struct.unpack('<H', packet[-2:])

                if all([beacon_major_version == 1,
                        beacon_minor_version == 2,
                        application_host_id == 1]):
                    beacon_data = {
                        'ip': sender[0],
                        'port': port,
                        'hostname': computer_name.decode('utf-8'),
                        'xplane_version': xplane_version_number,
                        'role': role,
                        'raknet_port': raknet_port
                    }

        except socket.timeout:
            raise XPlaneIpNotFound()

    sock.close()
    return beacon_data


# async def main():
#     beacon = find_xp()
#     port = beacon['port']
#     ip = beacon['ip']
#     ip = "127.0.0.1"
#     port = 49555

#     # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock = await open_local_endpoint("0.0.0.0", 62222)

#     # 1) Subscribe to receive once per second
#     cmd = b'RREF'  # "Request DataRef(s)"
#     freq = 1       # number of times per second (integer)
#     index = 0      # "my" number, so I can match responsed with my request
#     msg = struct.pack("<4sxii400s", cmd, freq, index, b'sim/aircraft/engine/acf_num_engines')
#     # sock.sendto(msg, (ip, port))
#     sock.send(msg, (ip, port))

#     # 2) Block, waiting to receive a packet
#     # data, addr = sock.recvfrom(2048)
#     data, addr = await sock.receive()
#     header = data[0:4]
#     if header[0:4] != b'RREF':
#         raise ValueError("Unknown packet")

#     # 3) Unpack the data:
#     idx, value = struct.unpack("<if", data[5:13])
#     assert idx == index
#     print("Number of engines is {}".format(int(value)))

#     # 4) Unsubscribe -- as otherwise we'll continue to get this data, once every second!
#     freq = 0
#     msg = struct.pack("<4sxii400s", cmd, freq, index, b'sim/aircraft/engine/acf_num_engines')
#     sock.sendto(msg, (ip, port))

from time import time
import common.sane_tasks as sane_tasks
from xplane.params_to_subscribe import udp_params_list

class XPconnectionUDP():
    """ connection to native XPlane udp protocol """

    def __init__(self) -> None:
        self.remote_host = "127.0.0.1"
        self.remote_port = 49000

        self.listen_host = "127.0.0.1"
        self.receive_port = 62222 
        self.send_port = 62223 

        self.sock_receive = None
        self.sock_send = None
        self.udp_read_task = None
        self.terminate_reader_task = False

        self.on_new_data_callback = None 
        self.on_data_exception_callback = None

        self.last_packet_received_time = None

    async def connect(self, remote_address, remote_port, on_new_data_callback, on_data_exception_callback):
        """ connect to ExtPlane plugin """
        # remember for reconnect
        self.remote_host = remote_address
        self.remote_port = remote_port

        await self.disconnect()

        self.on_new_data_callback = on_new_data_callback
        self.on_data_exception_callback = on_data_exception_callback
        await self.start_read_task()

    async def start_read_task(self):
        # self.sock = await open_local_endpoint(self.listen_host, self.listen_port)
        self.sock_receive = await open_local_endpoint(host='127.0.0.1', port=self.receive_port)
        self.sock_send = await open_local_endpoint(host='127.0.0.1', port=self.send_port)
        self.udp_read_task = sane_tasks.spawn(self.read_udp_task())    

    async def read_udp_task(self):
        while not self.terminate_reader_task:
            data, (host, port) = await self.sock_receive.receive()
            print("prinyal main")

            self.last_packet_received_time = time()

            continue

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

    async def disconnect(self):
        pass

    def set_param(self, param, value):
        msg = struct.pack(
            '<4sxf500s', 
            b'DREF',
            value,
            str(param).encode('utf-8')
        )

        self.sock_send.send(msg, (self.remote_host, self.remote_port))

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

        self.sock_send.send(msg, (self.remote_host, self.remote_port)) 


from xplane.params import Params
from xplane.params_to_subscribe import to_subscribe

class ParamSubscriberUDP:
    def __init__(self) -> None:
        self.to_subscribe = asyncio.Queue()
        self.xp_udp: XPconnectionUDP = None
        self.terminate_task = False

    def run_subsriber_task(self):
        sane_tasks.spawn(self._subscriber_task())
    
    async def _subscriber_task(self):
        while not self.terminate_task:
            now = time()
            if not self.xp_udp.last_packet_received_time or \
                now - self.xp_udp.last_packet_received_time > 4:
                
                print("poslal main")
                for p, freq, proto, in to_subscribe:
                    if proto == "udp":
                        self.xp_udp.subscribe_to_param(p, freq)
                
            await asyncio.sleep(2)


async def send_task(resp):
    while True:
        host = '127.0.0.1'
        port = 49555 
        resp.send("hello".encode(), (host, port))
        print("x")

        await asyncio.sleep(1)
    
xp_master_udp = XPconnectionUDP()
udp_param_subscriber = ParamSubscriberUDP() 
udp_param_subscriber.xp_udp = xp_master_udp


async def read_task(endpoint):
    while True:
        data, (host, port) = await endpoint.receive()
        # print(f"Received {len(data)} bytes from {host}:{port}")
        # print(">", data)
        print("y")
    
async def start_read_task():
    endpoint = await open_local_endpoint(host='127.0.0.1', port=62222)


async def main():
    endpoint = await open_local_endpoint(host='127.0.0.1', port=62222)
    asyncio.create_task(send_task(endpoint))
    
    udp_read_task = sane_tasks.spawn(read_task(endpoint))    

    while True:
        await asyncio.sleep(2)


async def main2():
    def a(data):
        pass

    def b(err):
        pass

    await master.xp_master_udp.connect('127.0.0.1', 49555, a, b)
    master.udp_param_subscriber.run_subsriber_task()

    while True:
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main2())
