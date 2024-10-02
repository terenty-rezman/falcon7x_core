import numpy as np

from uso.to_model_packet import uso_dtype, uso_float_field_names, uso_bitfield_names


def unpack_packet(uso_udp_packet):
    uso_packet = np.frombuffer(uso_udp_packet, uso_dtype)    

    unpacked = {}
    
    for name in uso_float_field_names:
        unpacked[name] = float(uso_packet[name][0])

    # unpack bitfield
    bits = np.unpackbits(uso_packet["bitfield"][0], count=len(uso_bitfield_names), bitorder='little')
    unpacked["bits"] = bits

    return unpacked


uso_buttons_receive_map = {
    "swap_lh": "I06_b26",
    "fdtd_lh": "I06_b27",
    "vhf_push_lh": "I06_b32",
    "baro_push_lh": "I06_c03",
    "fp_autothrottle": "I06_c04",
    "fp_speed_is_mach_push": "I06_c05",
    "fp_approach": "I06_c08",
    "fp_lnav": "I06_c09",
    "fp_hdg_trk_mode": "I06_c10",
    "fp_hdg_trk_push": "I06_c11",
    "fp_pilot_side": "I06_c14",
    "fp_autopilot": "I06_c15",
    "fp_clb": "I06_c18",
    "fp_vs": "I06_c19",
    "fp_vnav": "I06_c20",
    "fp_alt": "I06_c21",
    "swap_rh": "I06_b16",
    "fdtd_rh": "I06_b17",
    "vhf_push_rh": "I06_b22",
    "baro_push_rh": "I06_b25",
    "event_lh": "I06_b11",
    "fms_msg_lh": "I06_b12",
    "master_caution_lh": "I06_b13",
    "master_warning_lh": "I06_b14",
    "sil_aural_alarm_lh": "I06_b15",
    "event_rh": "I06_c24",
    "fms_msg_rh": "I06_c25",
    "sil_aural_alarm_rh": "I06_c26",
    "master_caution_rh": "I06_c27",
    "master_warning_rh": "I06_c28",
    "sfd_menu": "I06_b05",
    "sfd_std": "I06_b06",
}

# replace buttons bit ids with indecies
for button_id, bit_id in uso_buttons_receive_map.items():
    idx = uso_bitfield_names.index(bit_id)
    uso_buttons_receive_map[button_id] = idx
