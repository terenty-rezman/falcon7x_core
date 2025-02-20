from cas import cas
import synoptic_remote.synoptic_connection as synoptic_connection


# mfi slave xplane
MFI_XP_HOST = "192.168.32.252"

# cas displays
cas.CAS_HOST = "127.0.0.1"
cas.CAS_PORT_LEFT = 8881
cas.CAS_PORT_RIGHT = 8882

# connect to master xplane plugin
XP_MASTER_HOST = "127.0.0.1"
XP_MASTER_PORT = 51000

# native xplane udp port to send to
XP_MASTER_UDP_PORT = 49000

# web interface listens on this address:
WEB_INTERFACE_HOST = "0.0.0.0"
WB_INTERFACE_PORT = 6070

# uso udp ports
USO_HOST = "127.0.0.1"
USO_RECEIVE_PORT = 5122
USO_SEND_PORT = 6022
USO_SEND_DELAY = 0.1

# qml synoptic address
synoptic_connection.Settings.QML_SYNOPTIC_HOST = "127.0.0.1"
synoptic_connection.Settings.QML_SYNOPTIC_PORT = 8800
