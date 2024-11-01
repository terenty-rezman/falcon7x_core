import numpy as np

from uso.received_packet import uso_dtype, uso_float_field_names, uso_bitfield_names


def unpack_packet(uso_udp_packet):
    uso_packet = np.frombuffer(uso_udp_packet, uso_dtype)    

    unpacked = {}
    floats = [0] * len(uso_float_field_names) 

    for i, name in enumerate(uso_float_field_names):
        floats[i] = float(uso_packet[name][0])

    unpacked["floats"] = floats

    # unpack bitfield
    bits = np.unpackbits(uso_packet["bitfield"][0], count=len(uso_bitfield_names), bitorder='little')
    unpacked["bits"] = bits

    return unpacked


uso_pushbuttons_receive_map = {
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
    "wc_trim_pitch_up_lh": "I03_b06",
    "wc_trim_pitch_down_lh": "I03_b07",
    "wc_trim_pitch_up_rh": "I03_b08",
    "wc_trim_pitch_down_rh": "I03_b09",
    "wc_trim_roll_right_lh": "I03_b10",
    "wc_trim_roll_left_lh": "I03_b11",
    "wc_trim_roll_right_rh": "I03_b12",
    "wc_trim_roll_left_rh": "I03_b13",
    "wc_trim_yaw_right_lh": "I03_b14",
    "wc_trim_yaw_left_lh": "I03_b15",
    "wc_trim_yaw_right_rh": "I03_b16",
    "wc_trim_yaw_left_rh": "I03_b17",
    "apu_master": "I07_a18",
    "apu_start_stop": "I07_a19",
    "backup_pump": "I07_a20",
    "cabin_master": "I07_b04",
    "rh_master": "I07_b05",
    "rh_init": "I07_b06",
    "bus_tie": "I07_b07",
    "lh_init": "I07_b08",
    "rh_master": "I07_b09",
    "galley_master": "I07_b10",
    "gen1": "I07_b11",
    "lh_isol": "I07_b12",
    "rat_reset": "I07_b13",
    "rh_isol": "I07_b14",
    "gen2": "I07_b15",
    "gen3": "I07_b16",
    "crew_temp_push": "I07_a27",
    "fwd_temp_push": "I07_a26",
    "gnd_vent": "I07_b01",
    "xbleed_ecs": "I07_b03",
    "bleed1": "I07_b24",
    "bleed12": "I07_b25",
    "bleed13": "I07_b26",
    "bleed3": "I07_b27",
    "bleed_apu": "I07_b28",
    "bleed2": "I07_b29",
    "bag_vent": "I07_b01",
    "boost1": "I07_c14",
    "boost2": "I07_c15",
    "boost3": "I07_c16",
    "probe_12": "I07_c03",
    "probe_3": "I07_c04",
    "probe_4": "I07_c05",
    "windshield_backup": "I07_c06",
    "windshield_lh": "I07_c07",
    "windshield_rh": "I07_c08",
    "el_anticol": "I07_c26",
    "el_nav": "I07_c27",
    "el_taxi": "I08_a02",
    "el_wing": "I08_a03",
    "rain_rplint_lh": "I08_a04",
    "il_cabin": "I08_a05",
    "il_fasten": "I08_a06",
    "il_smoking": "I08_a07",
    "rain_rplint_rh": "I08_a11",
}


uso_switches_receive_map = {
    "en_motor": "I03_c09",
    "en_ign": "I03_c10",
    "en_normal": "I03_c11",
    "en_start": "I03_c12",
    "en_fuel_1": "I03_c16",
    "en_fuel_2": "I03_c17",
    "en_fuel_3": "I03_c18",
    "ep_aural_warn_1": "I03_a22",
    "ep_aural_warn_2": "I03_a23",
    "ep_bag_fan": "I03_a24",
    "ep_elec_rh_ess": "I03_a25",
    "ep_fuel_2_bu": "I03_a26",
    "ep_rat_auto": "I03_a27",
    "ep_trim_emerg": "I03_a28",
    # "ep_empty_btn": "I03_a29",
    "firebutton_1": "I06_c29",
    "disch_11": "I06_c30",
    "disch_12": "I06_c31",
    "firebutton_2": "I06_c32",
    "disch_21": "I07_a01",
    "disch_22": "I07_a02",
    "firebutton_3": "I07_a03",
    "disch_31": "I07_a04",
    "disch_32": "I07_a05",
    "apu_disch": "I07_a06",
    "firerearcomp_button": "I07_a07",
    "firebagcomp_button": "I07_a08",
    "airbrake_auto": "I07_a11",
    "fcs_engage_norm": "I07_a11",
    "fcs_engage_stby": "I07_a13",
    "fcs_steering": "I07_a14",
    "eng_1": "I07_a15",
    "eng_2": "I07_a16",
    "eng_3": "I07_a17",
    "shutoff_a1": "I07_a21",
    "shutoff_a3": "I07_a22",
    "shutoff_b2": "I07_a23",
    "shutoff_b3": "I07_a24",
    "shutoff_c2": "I07_a25",
    "bat1": "I07_b17",
    "bat2": "I07_b18",
    "ice_brake": "I07_b19",
    "ice_eng1": "I07_b20",
    "ice_eng2": "I07_b21",
    "ice_eng3": "I07_b22",
    "ice_wings": "I07_b23",
    "pack_crew_off": "I07_a28",
    "pack_normal": "I07_a29",
    "pack_backup": "I07_a30",
    "pack_emerg": "I07_a31",
    "pack_pax_off": "I07_a32",
    "bag_isol": "I07_b02",
    "dump": "I07_b30",
    "pressu_man": "I07_b32",
    "cabin_alt_climb": "I07_c01",
    "cabin_alt_descent": "I07_c02",
    "backup_13": "I07_c13",
    "xbp_12": "I07_c17",
    "xbp_13": "I07_c18",
    "xbp_23": "I07_c19",
    "xtk_down_1": "I07_c20",
    "xtk_down_2": "I07_c21",
    "xtk_left": "I07_c22",
    "xtk_right": "I07_c23",
    "xtk_up_1": "I07_c24",
    "xtk_up_2": "I07_c25",
    "pax_oxygen_closed": "I07_c09",
    "pax_oxygen_firstaid": "I07_c10",
    "pax_oxygen_normal": "I07_c11",
    "pax_oxygen_oride": "I07_c12",
    "el_landing_lh_off": "I07_c28",
    "el_landing_lh_on": "I07_c29",
    "el_landing_lh_pulse": "I07_c30",
    "el_landing_rh_off": "I07_c31",
    "el_landing_rh_on": "I07_c32",
    "el_landing_rh_pulse": "I08_a01",
    "il_emerge_lights_arm": "I08_a08",
    "il_emerge_lights_off": "I08_a09",
    "il_emerge_lights_on": "I08_a10",
} # switches

uso_rotate_switch_receive_map = {
    "vhf_control_lh": "I06_b28", # second bit for rotate switch (IO) always comes next in uso packet so we dont need its index
    "baro_rot_lh": "I06_c01",
    "fp_speed_kts_mach": "I06_c06",
    "fp_hdg_trk": "I06_c12",
    "fp_vs_path": "I06_c16",
    "fp_asel": "I06_c22",
    "vhf_control_rh": "I06_b18",
    "baro_rot_rh": "I06_b23",
    "sfd_set": "I06_b03", 
}

uso_floats_receive_map = {
   "pc_bank_lh": "A001",
   "pc_pitch_lh": "A002",
   "pc_right_brake_lh": "A003",
   "pc_left_brake_lh": "A004",
   "pc_heading_lh": "A005",
   "pc_right_brake_rh": "A006",
   "pc_left_brake_rh": "A007",
   "pc_heading_rh": "A008",
   "pc_throttle_1": "A012",
   "pc_throttle_2": "A013",
   "pc_throttle_3": "A015",
   "wc_sf": "A016",
   "wc_ab": "A017",
   "aft_temp": "A028",
   "fwd_temp": "A029",
   "crew_temp": "A030",
   "crew_ratio": "A031"
}

# replace buttons bit ids with indecies
for button_id, bit_id in uso_pushbuttons_receive_map.items():
    idx = uso_bitfield_names.index(bit_id)
    uso_pushbuttons_receive_map[button_id] = idx

for button_id, bit_id in uso_switches_receive_map.items():
    idx = uso_bitfield_names.index(bit_id)
    uso_switches_receive_map[button_id] = idx

for button_id, bit_id in uso_rotate_switch_receive_map.items():
    idx = uso_bitfield_names.index(bit_id)
    uso_rotate_switch_receive_map[button_id] = idx

for float_id, bit_id in uso_floats_receive_map.items():
    idx = uso_float_field_names.index(bit_id)
    uso_floats_receive_map[float_id] = idx
