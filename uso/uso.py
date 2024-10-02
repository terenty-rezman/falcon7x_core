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
    "clc_undo_lh": "I03_c19",
    "clc_ent_lh": "I03_c20",
    "clc_next_lh": "I03_c21",
    "clc_prev_lh": "I03_c22",
    "clc_cl_lh": "I03_c23",
    "clc_undo_rh": "I04_a20",
    "clc_ent_rh": "I04_a21",
    "clc_next_rh": "I04_a22",
    "clc_prev_rh": "I04_a23",
    "clc_cl_rh": "I04_a24",
    "wc_backup_slats": "I03_b02",
    #
    "tb_mic_rh": "I04_a26",
    "tb_disp_left_rh": "I04_a27",
    "tb_disp_right_rh": "I04_a28",
    "tb_disp_up_rh": "I04_a29",
    "tb_disp_down_rh": "I04_a30",
    "tb_menu_rh": "I04_a25",
    "tb_mic_lh": "I03_c25",
    "tb_disp_left_lh": "I03_c26",
    "tb_disp_right_lh": "I03_c27",
    "tb_disp_up_lh": "I03_c28",
    "tb_disp_down_lh": "I03_c29",
    "tb_menu_rl": "I03_c24",
}


uso_switches_receive_map = {
    "wc_sf_0": "I03_a30",
    "wc_sf_1": "I03_a31",
    "wc_sf_2": "I03_a32",
    "wc_sf_3": "I03_b01",
    "wc_ab_0": "I03_b03",
    "wc_ab_1": "I03_b04",
    "wc_ab_2": "I03_b05",
}


# replace buttons bit ids with indecies
for button_id, bit_id in uso_buttons_receive_map.items():
    idx = uso_bitfield_names.index(bit_id)
    uso_buttons_receive_map[button_id] = idx

for button_id, bit_id in uso_switches_receive_map.items():
    idx = uso_bitfield_names.index(bit_id)
    uso_switches_receive_map[button_id] = idx
