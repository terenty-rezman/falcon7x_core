import numpy as np

from uso.to_model_packet import uso_dtype, uso_field_names


def bitfield_get(byte_array, bit_idx: int):
    byte_idx = bit_idx # 8
    bit_offset = bit_idx % 8

    val = byte_array[byte_idx]
    val = int(val)

    if bit_offset:
        val = val  & (1 << bit_offset)

    return 1 if val else 0


def unpack_packet(uso_udp_packet):
    uso_packet = np.frombuffer(uso_udp_packet, uso_dtype)    

    unpacked = {}

    unpacked["A001"] = float(uso_packet["A001"][0])
    unpacked["A002"] = float(uso_packet["A002"][0])
    unpacked["A003"] = float(uso_packet["A003"][0])
    unpacked["A004"] = float(uso_packet["A004"][0])
    unpacked["A005"] = float(uso_packet["A005"][0])
    unpacked["A006"] = float(uso_packet["A006"][0])
    unpacked["A007"] = float(uso_packet["A007"][0])
    unpacked["A008"] = float(uso_packet["A008"][0])
    unpacked["A009"] = float(uso_packet["A009"][0])

    # unpack bitfield
    name_i = uso_field_names.index("I03_a01")
    last_name_i = uso_field_names.index("I03_a30")

    bit_field_count = last_name_i - name_i + 1

    for b in uso_packet["bitfield"][0]:
        byte_val = int(b)

        for offset in range(0, 8):
            val = byte_val  & (1 << offset)
        
            name = uso_field_names[name_i]
            name_i += 1
            
            unpacked[name] = 1 if val else 0 
            bit_field_count -= 1

            if bit_field_count == 0:
                break

    return unpacked
