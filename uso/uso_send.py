import numpy as np

from uso.sent_packet import uso_dtype, uso_bitfield_names


def create_packet(lamps_state):
    uso_packet = np.zeros(1, dtype=uso_dtype)    
    uso_packet["bitfield"] = np.packbits(lamps_state, bitorder="little")
    return uso_packet


uso_lamp_send_map = {
    "pty_lh": "O10_a12",
}


# replace lamps bit ids with indecies
for lamp_id, bit_id in uso_lamp_send_map.items():
    idx = uso_bitfield_names.index(bit_id)
    uso_lamp_send_map[lamp_id] = idx
