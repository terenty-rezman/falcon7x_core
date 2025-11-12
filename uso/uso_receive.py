import numpy as np

from uso.received_packet import uso_dtype, uso_float_field_names, uso_bitfield_names


def unpack_packet(uso_udp_packet):
    uso_packet = np.frombuffer(uso_udp_packet, dtype=uso_dtype)    

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
    "swap_lh": "I06_b26", # SWAP [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "fdtd_lh": "I06_b27", # FD/TD [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "vhf_push_lh": "I06_b32", # VHF 8.33/25 button left [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "baro_push_lh": "I06_c03", # BARO PUSH STD button left [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "fp_autothrottle": "I06_c04", # AT [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "fp_speed_is_mach_push": "I06_c05", # CHG PUSH button [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "fp_approach": "I06_c08", # APP [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "fp_lnav": "I06_c09", # LNAV [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "fp_hdg_trk_mode": "I06_c10", # HDG/TRK [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "fp_hdg_trk_push": "I06_c11", # SYNK PUSH button [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "fp_pilot_side": "I06_c14", # PILOT SIDE [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "fp_autopilot": "I06_c15", # AP [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "fp_clb": "I06_c18", # CLB [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "fp_vs": "I06_c19", # VS [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "fp_vnav": "I06_c20", # VNAV [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "fp_alt": "I06_c21", # ALT [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "swap_rh": "I06_b16", # SWAP [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "fdtd_rh": "I06_b17", # FD/TD [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "vhf_push_rh": "I06_b22", # VHF 8.33/25 button right [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "baro_push_rh": "I06_b25", # BARO PUSH STD button right [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "event_lh": "I06_b11", # EVENT [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [22 Пульт козырька левый]
    "fms_msg_lh": "I06_b12", # FMS MSG [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [22 Пульт козырька левый]
    "master_caution_lh": "I06_b13", # MASTER CAUTION [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [22 Пульт козырька левый]
    "master_warning_lh": "I06_b14", # MASTER WARNING [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [22 Пульт козырька левый]
    "sil_aural_alarm_lh": "I06_b15", # SIL [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [22 Пульт козырька левый]
    "event_rh": "I06_c24", # EVENT [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [23 Пульт козырька правый]
    "fms_msg_rh": "I06_c25", # FMS MSG [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [23 Пульт козырька правый]
    "sil_aural_alarm_rh": "I06_c26", # SIL [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [23 Пульт козырька правый]
    "master_caution_rh": "I06_c27", # MASTER CAUTION [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [23 Пульт козырька правый]
    "master_warning_rh": "I06_c28", # MASTER WARNING [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [23 Пульт козырька правый]
    "sfd_menu": "I06_b05", # MENU [K2 Средний пульт (Pedestal)] [Приборная доска] [33 Attitude Display]
    "sfd_std": "I06_b06", # STD [K2 Средний пульт (Pedestal)] [Приборная доска] [33 Attitude Display]
    "clc_undo_lh": "I03_c19", # switch UND [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [04 Пульт управления чеклистом (CLC) левый]
    "clc_ent_lh": "I03_c20", #  switch TEN [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [04 Пульт управления чеклистом (CLC) левый]
    "clc_next_lh": "I03_c21", # switch NEXT [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [04 Пульт управления чеклистом (CLC) левый]
    "clc_prev_lh": "I03_c22", # switch PREV [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [04 Пульт управления чеклистом (CLC) левый]
    "clc_cl_lh": "I03_c23", # C/L [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [04 Пульт управления чеклистом (CLC) левый]
    "clc_undo_rh": "I04_a20", # switch UND [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [05 Пульт управления чеклистом (CLC) правый]
    "clc_ent_rh": "I04_a21", # switch TEN [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [05 Пульт управления чеклистом (CLC) правый]
    "clc_next_rh": "I04_a22", # switch NEXT [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [05 Пульт управления чеклистом (CLC) правый]
    "clc_prev_rh": "I04_a23", # switch PREV [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [05 Пульт управления чеклистом (CLC) правый]
    "clc_cl_rh": "I04_a24", # C/L [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [05 Пульт управления чеклистом (CLC) правый]
    #
    "tb_mic_rh": "I04_a26", # MIC [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [07 Пульт трэкбола правый (Trackball)]
    "tb_disp_left_rh": "I04_a27", # DISP LEFT [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [07 Пульт трэкбола правый (Trackball)]
    "tb_disp_right_rh": "I04_a28", # DISP RIGHT [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [07 Пульт трэкбола правый (Trackball)]
    "tb_disp_up_rh": "I04_a29", # DISP UP [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [07 Пульт трэкбола правый (Trackball)]
    "tb_disp_down_rh": "I04_a30", # DISP DOWN [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [07 Пульт трэкбола правый (Trackball)]
    "tb_menu_rh": "I04_a25", # MENU [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [07 Пульт трэкбола правый (Trackball)]
    "tb_mic_lh": "I03_c25", # MIC [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [08 Пульт трэкбола левый (Trackball)]
    "tb_disp_left_lh": "I03_c26", # DISP LEFT [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [08 Пульт трэкбола левый (Trackball)]
    "tb_disp_right_lh": "I03_c27", # DISP RIGHT [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [08 Пульт трэкбола левый (Trackball)]
    "tb_disp_up_lh": "I03_c28", # DISP UP [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [08 Пульт трэкбола левый (Trackball)]
    "tb_disp_down_lh": "I03_c29", # DISP DOWN [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [08 Пульт трэкбола левый (Trackball)]
    "tb_menu_lh": "I03_c24", # MENU [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [08 Пульт трэкбола левый (Trackball)]
    "wc_trim_pitch_up_lh": "I03_b06", # pitch left + [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [09 Пульт ручного триммирования (Manual trims)]
    "wc_trim_pitch_down_lh": "I03_b07", # pitch left - [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [09 Пульт ручного триммирования (Manual trims)]
    "wc_trim_pitch_up_rh": "I03_b08", # pitch right + [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [09 Пульт ручного триммирования (Manual trims)]
    "wc_trim_pitch_down_rh": "I03_b09", # pitch right - [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [09 Пульт ручного триммирования (Manual trims)]
    "wc_trim_roll_up_lh": "I03_b10", # roll left + [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [09 Пульт ручного триммирования (Manual trims)]
    "wc_trim_roll_down_lh": "I03_b11", # roll left - [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [09 Пульт ручного триммирования (Manual trims)]
    "wc_trim_roll_up_rh": "I03_b12", # roll right + [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [09 Пульт ручного триммирования (Manual trims)]
    "wc_trim_roll_down_rh": "I03_b13", # roll right - [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [09 Пульт ручного триммирования (Manual trims)]
    "wc_trim_yaw_up_lh": "I03_b14", # yaw left + [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [09 Пульт ручного триммирования (Manual trims)]
    "wc_trim_yaw_down_lh": "I03_b15", # yaw left - [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [09 Пульт ручного триммирования (Manual trims)]
    "wc_trim_yaw_up_rh": "I03_b16", # yaw right + [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [09 Пульт ручного триммирования (Manual trims)]
    "wc_trim_yaw_down_rh": "I03_b17", # yaw right - [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [09 Пульт ручного триммирования (Manual trims)]
    "apu_start_stop": "I07_a19", # APU Start / Stop [K4 Верхний пульт] [Верхний пульт] [04 - 05 - 06 Engines Manual Start - APU control panel - HYDROLYCS]
    "backup_pump": "I07_a20", # BACK UP PUMP [K4 Верхний пульт] [Верхний пульт] [04 - 05 - 06 Engines Manual Start - APU control panel - HYDROLYCS]
    "cabin_master": "I07_b04", # CABIN MASTER [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
    "rh_master": "I07_b05", # RH MASTER [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
    "rh_init": "I07_b06", # RH INIT [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
    "bus_tie": "I07_b07", # BUS TIE [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
    "lh_init": "I07_b08", # LH INIT [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
    "lh_master": "I07_b09", # LH MASTER [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
    "galley_master": "I07_b10", # GALLEY MASTER [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
    "gen1": "I07_b11", # GEN 1 [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
    "lh_isol": "I07_b12", # LH ISOL [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
    "rat_reset": "I07_b13", # RAT RESET [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
    "rh_isol": "I07_b14", # RH ISOL [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
    "gen2": "I07_b15", # GEN 2 [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
    "gen3": "I07_b16", # GEN 3 [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
    "crew_temp_push": "I07_a27", # CREW TEMP PUSH [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
    "fwd_temp_push": "I07_a26", # PAX FWD TEMP PUSH [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
    "gnd_vent": "I07_b01", # GND VENT [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
    "xbleed_ecs": "I07_b03", # XBLEED ECS [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
    "bleed1": "I07_b24", # BLEED 1 [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
    "bleed12": "I07_b25", # XBLEED 1--2 [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
    "bleed13": "I07_b26", # XBLEED 2--3 [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
    "bleed3": "I07_b27", # BLEED 3 [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
    "bleed_apu": "I07_b28", # BLEED APU [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
    "bleed2": "I07_b29", # BLEED 2 [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
    "bag_vent": "I07_b31", # BAG VENT [K4 Верхний пульт] [Верхний пульт] [11 - 12 - 13 WINDSHEILD HEAT - PILOT HEAT - PAX OXYGEN BLEED - Pressurization]
    "boost1": "I07_c14", # BOOST 1 [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
    "boost2": "I07_c15", # BOOST 2 [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
    "boost3": "I07_c16", # BOOST 3 [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
    "probe_12": "I07_c03", # PROBE 1+2 [K4 Верхний пульт] [Верхний пульт] [11 - 12 - 13 WINDSHEILD HEAT - PILOT HEAT - PAX OXYGEN]
    "probe_3": "I07_c04", # PROBE 4 [K4 Верхний пульт] [Верхний пульт] [11 - 12 - 13 WINDSHEILD HEAT - PILOT HEAT - PAX OXYGEN]
    "probe_4": "I07_c05", # PROBE 4 [K4 Верхний пульт] [Верхний пульт] [11 - 12 - 13 WINDSHEILD HEAT - PILOT HEAT - PAX OXYGEN]
    "windshield_backup": "I07_c06", # BACK UP [K4 Верхний пульт] [Верхний пульт] [11 - 12 - 13 WINDSHEILD HEAT - PILOT HEAT - PAX OXYGEN]
    "windshield_lh": "I07_c07", # LH [K4 Верхний пульт] [Верхний пульт] [11 - 12 - 13 WINDSHEILD HEAT - PILOT HEAT - PAX OXYGEN]
    "windshield_rh": "I07_c08", # RH [K4 Верхний пульт] [Верхний пульт] [11 - 12 - 13 WINDSHEILD HEAT - PILOT HEAT - PAX OXYGEN]
    "el_anticol": "I07_c26", # ANTICOL [K4 Верхний пульт] [Верхний пульт] [15 EXTERIOR LIGHTS + RAIN RPLNT LH]
    "el_nav": "I07_c27", # NAV [K4 Верхний пульт] [Верхний пульт] [15 EXTERIOR LIGHTS + RAIN RPLNT LH]
    "el_taxi": "I08_a02", # TAXI [K4 Верхний пульт] [Верхний пульт] [15 EXTERIOR LIGHTS + RAIN RPLNT LH]
    "el_wing": "I08_a03", # WINGS [K4 Верхний пульт] [Верхний пульт] [15 EXTERIOR LIGHTS + RAIN RPLNT LH]
    "rain_rplint_lh": "I08_a04", # LH [K4 Верхний пульт] [Верхний пульт] [15 EXTERIOR LIGHTS + RAIN RPLNT LH]
    "il_cabin": "I08_a05", # CABIN [K4 Верхний пульт] [Верхний пульт] [16 - 17 COCKPIT LIGHTS - INTERIOR LIGHTS + RAIN RPLNT RH]
    "il_fasten": "I08_a06", # FASTEN BELT [K4 Верхний пульт] [Верхний пульт] [16 - 17 COCKPIT LIGHTS - INTERIOR LIGHTS + RAIN RPLNT RH]
    "il_smoking": "I08_a07", # NO SMOKING [K4 Верхний пульт] [Верхний пульт] [16 - 17 COCKPIT LIGHTS - INTERIOR LIGHTS + RAIN RPLNT RH]
    "rain_rplint_rh": "I08_a11", # RH [K4 Верхний пульт] [Верхний пульт] [16 - 17 COCKPIT LIGHTS - INTERIOR LIGHTS + RAIN RPLNT RH]
    "fcs_engage_norm": "I07_a12", # FCS ENGAGE NORM [K4 Верхний пульт] [Верхний пульт] [02 - 03 FLIGHT CONTROL  - STEERING FL CON]
    "fcs_engage_stby": "I07_a13", # FCS ENGAGE ST-BY [K4 Верхний пульт] [Верхний пульт] [02 - 03 FLIGHT CONTROL  - STEERING FL CON]
    "eng_1": "I07_a15", # man start eng 1 [K4 Верхний пульт] [Верхний пульт] [04 - 05 - 06 Engines Manual Start - APU control panel - HYDROLYCS]
    "eng_2": "I07_a16", # man start eng 2 [K4 Верхний пульт] [Верхний пульт] [04 - 05 - 06 Engines Manual Start - APU control panel - HYDROLYCS]
    "eng_3": "I07_a17", # man start eng 3 [K4 Верхний пульт] [Верхний пульт] [04 - 05 - 06 Engines Manual Start - APU control panel - HYDROLYCS]
    "ice_eng1": "I07_b20", # ENG 1 [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
    "ice_eng2": "I07_b21", # ENG 2 [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
    "ice_eng3": "I07_b22", # ENG 3 [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
    "ice_brake": "I07_b19", # BRAKE [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
    "ice_wings": "I07_b23", # WINGS [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
    "xtk_left": "I07_c22", # XTK LEFT 1 [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
    "xtk_right": "I07_c23", # XTK RIGHT 1 [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
    "rev_ils_vor_lh": "I03_b22", # ILS VOR < [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [18 (Reversion Panel)]
	"rev_pdu_mdu": "I03_b23", # PDU MDU [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [18 (Reversion Panel)]
	"rev_irs_rh": "I03_b24", # IRS > [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [18 (Reversion Panel)]
	"rev_ra_rh": "I03_b25",	# RA > [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [18 (Reversion Panel)]
    "rev_ads_rh": "I03_b26", # ADS > [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [18 (Reversion Panel)]"
	"rev_fms_rh": "I03_b27", # FMS > [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [18 (Reversion Panel)]
	"rev_ils_vor_rh": "I03_b28", # ILS VOR > [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [18 (Reversion Panel)]
	"rev_irs_lh": "I03_b18", # IRS < [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [18 (Reversion Panel)]
	"rev_ra_lh": "I03_b19",	# RA < [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [18 (Reversion Panel)]
    "rev_ads_lh": "I03_b20", # ADS < [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [18 (Reversion Panel)]"
	"rev_fms_lh": "I03_b21", # FMS < [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [18 (Reversion Panel)]
    "mkb_a_rh": "I04_c16",	# A [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_b_rh": "I04_c17",	# B [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_c_rh": "I04_c18",	# C [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_d_rh": "I04_c19",	# D [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_e_rh": "I04_c20",	# E [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_f_rh": "I04_c21",	# F [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_g_rh": "I04_c22",	# G [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_h_rh": "I04_c23",	# H [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_i_rh": "I04_c24",	# I [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_j_rh": "I04_c25",	# J [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_k_rh": "I04_c26",	# K [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_l_rh": "I04_c27",	# L [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_m_rh": "I04_c28",	# M [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_n_rh": "I04_c29",	# N [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_o_rh": "I04_c30",	# O [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_p_rh": "I04_c31",	# P [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_q_rh": "I04_c32",	# Q [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_r_rh": "I05_a01",	# R [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_s_rh": "I05_a02",	# S [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_t_rh": "I05_a03",	# T [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_u_rh": "I05_a04",	# U [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_v_rh": "I05_a05",	# V [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_w_rh": "I05_a06",	# W [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_x_rh": "I05_a07",	# X [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_y_rh": "I04_a31",	# Y [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_z_rh": "I04_a32",	# Z [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
    "mkb_1_rh": "I04_b08",	# 1 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_2_rh": "I04_b09",	# 2 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_3_rh": "I04_b10",	# 3 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_4_rh": "I04_b11",	# 4 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_5_rh": "I04_b12",	# 5 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_6_rh": "I04_b13",	# 6 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_7_rh": "I04_b14",	# 7 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_8_rh": "I04_b15",	# 8 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_9_rh": "I04_b16",	# 9 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_0_rh": "I04_b17",	# 0 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
    "mkb_BKUP_rh": "I04_b21",	# BKUP | VHF [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_HF_rh": "I04_b22",	# HF [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_SAT_rh": "I04_b23",	# SAT [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_ATC_DTLC_rh": "I04_b24",	# ATC DTLC [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_XPDR_rh": "I04_b25",	# XPDR [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_BKUP_NAV_rh": "I04_b26",	# BKUP | NAV [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_TERR_INHIB_rh": "I04_b27",	# TERR INHIB [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_GS_INHIB_rh": "I04_b28",	# G/S INHIB [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_EMPTY1_rh": "I04_b29",	# EMPTY 1 < [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_TRFC_rh": "I04_b30",	# TRFC [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_CRS_rh": "I04_b31",	# CRS [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_SHOW_rh": "I04_b32",	# SHOW [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_DIRTO_rh": "I04_c01",	# DIRTO [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_EMPTY2_rh": "I04_c02",	# EMPTY 2 > [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_ID_rh": "I04_c03",	# ID [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_HSI_RANGE_IO_rh": "I04_c04",	# HSI RANGE IO [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_HSI_RANGE_IO_rh": "I04_c05",	# HSI RANGE IO [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_WX_RADAR_OFF_rh": "I04_c06",	# WX RADAR OFF [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_WX_RADAR_STBY_rh": "I04_c07",	# WX RADAR STBY [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_WX_RADAR_AUTO_rh": "I04_c08",	# WX RADAR AUTO [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_WX_RADAR_GAIN_rh": "I04_c09",	# WX RADAR GAIN [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_WX_RADAR_TILT_rh": "I04_c10",	# WX RADAR TILT [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_WX_RADAR_OVRD_rh": "I04_c11",	# WX RADAR OVRD [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_WX_RADAR_I0_rh": "I04_c12",	# WX RADAR I0 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_WX_RADAR_I0_rh": "I04_c13",	# WX RADAR I0 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_WX_RADAR_PUSH_SECT_rh": "I04_c14",	# WX RADAR PUSH SECT [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
    "mkb_CL_rh": "I04_c15",	# C/L [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
    "mkb_LEFT_arrow_rh": "I04_b01",	# LEFT arrow [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_SPACE_rh": "I04_b02",	# SPACE [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_RIGHT_arrow_rh": "I04_b03",	# RIGHT arrow [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_CLR_rh": "I04_b04",	# CLR | DEL [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_SHIFT_rh": "I04_b05",	# SHIFT [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_ENTER_rh": "I04_b06",	# ENTER [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_SWAP_rh": "I04_b07",	# SWAP [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
    "mkb_multiplic_rh": "I04_b18",	# * | multiplication [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_div_rh": "I04_b19",	# / |division [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
	"mkb_min_plus_rh": "I04_b20",	#  - minus | + plus [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [13Многофункциональная клавиатура (MKB) правая]
    "mkb_a_lh": "I05_b03",	# A [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_b_lh": "I05_b04",	# B [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_c_lh": "I05_b05",	# C [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_d_lh": "I05_b06",	# D [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_e_lh": "I05_b07",	# E [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_f_lh": "I05_b08",	# F [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_g_lh": "I05_b09",	# G [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_h_lh": "I05_b10",	# H [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_i_lh": "I05_b11",	# I [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_j_lh": "I05_b12",	# J [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_k_lh": "I05_b13",	# K [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_l_lh": "I05_b14",	# L [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_m_lh": "I05_b15",	# M [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_n_lh": "I05_b16",	# N [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_o_lh": "I05_b17",	# O [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_p_lh": "I05_b18",	# P [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_q_lh": "I05_b19",	# Q [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_r_lh": "I05_b20",	# R [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_s_lh": "I05_b21",	# S [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_t_lh": "I05_b22",	# T [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_u_lh": "I05_b23",	# U [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_v_lh": "I05_b24",	# V [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_w_lh": "I05_b25",	# W [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_x_lh": "I05_b26",	# X [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_y_lh": "I03_c30",	# Y [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_z_lh": "I03_c31",	# Z [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
    "mkb_1_lh": "I04_a07",	# 1 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_2_lh": "I04_a08",	# 2 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_3_lh": "I04_a09",	# 3 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_4_lh": "I04_a10",	# 4 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_5_lh": "I04_a11",	# 5 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_6_lh": "I04_a12",	# 6 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_7_lh": "I04_a13",	# 7 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_8_lh": "I04_a14",	# 8 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_9_lh": "I04_a15",	# 9 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
	"mkb_0_lh": "I04_a16",	# 0 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [14 Многофункциональная клавиатура (MKB) левая]
}


uso_switches_receive_map = {
    "en_motor": "I03_c09", # Switch MOTOR [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [10 Пульт переключения резервных функций]
    "en_ign": "I03_c12", #"I03_c10", # Switch IGN [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [10 Пульт переключения резервных функций]
    "en_normal": "I03_c10", #"I03_c11", # Switch NORMAL [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [10 Пульт переключения резервных функций]
    "en_start": "I03_c11", #"I03_c12", # Switch START [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [10 Пульт переключения резервных функций]
    "en_fuel_1": "I03_c16", # FUEL ON 1 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [01 Сборка РУД]
    "en_fuel_2": "I03_c17", # FUEL ON 2 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [01 Сборка РУД]
    "en_fuel_3": "I03_c18", # FUEL ON 3 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [01 Сборка РУД]
    "ep_bag_fan": "I03_a24", # BAG FAN [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [12  (Emergency Panel)]
    "ep_elec_rh_ess": "I03_a25", # ELEC RH ESS [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [12  (Emergency Panel)]
    "ep_fuel_2_bu": "I03_a26", # FUEL 2 B/U [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [12  (Emergency Panel)]
    "ep_rat_auto": "I03_a27", # RAT AUTO [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [12  (Emergency Panel)]
    "ep_trim_emerg": "I03_a28", # TRIM EMERG [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [12  (Emergency Panel)]
    # "ep_empty_btn": "I03_a29", # Пустая [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [12  (Emergency Panel)]
    "firebutton_1": "I06_c29", # engine 1 shut off FIRE 1 [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
    "disch1_eng1": "I06_c30", # engine 1 DISCH 1 [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
    "disch2_eng1": "I06_c31", # engine 1 DISCH 2 [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
    "firebutton_2": "I06_c32", # engine 2 shut off FIRE 2 [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
    "disch1_eng2": "I07_a01", # engine 2 DISCH 1 [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
    "disch2_eng2": "I07_a02", # engine 2 DISCH 2 [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
    "firebutton_3": "I07_a03", # engine 3 shut off FIRE 3 [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
    "disch1_eng3": "I07_a04", # engine 3 DISCH 1 [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
    "disch2_eng3": "I07_a05", # engine 3 DISCH 2 [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
    "apu_disch": "I07_a06", # FIRE APU [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
    "firerearcomp_button": "I07_a07", # FIRE REAR COMP DISCH [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
    "firebagcomp_button": "I07_a08", # FIRE BAG COMP DISCH [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
    "airbrake_auto": "I07_a11", # AJB AUTO EXT. [K4 Верхний пульт] [Верхний пульт] [02 - 03 FLIGHT CONTROL  - STEERING FL CON]
    "fcs_steering": "I07_a14", # NWS [K4 Верхний пульт] [Верхний пульт] [02 - 03 FLIGHT CONTROL  - STEERING FL CON]
    "shutoff_a1": "I07_a21", # SHUT OFF A1 [K4 Верхний пульт] [Верхний пульт] [04 - 05 - 06 Engines Manual Start - APU control panel - HYDROLYCS]
    "shutoff_a3": "I07_a22", # SHUT OFF A3 [K4 Верхний пульт] [Верхний пульт] [04 - 05 - 06 Engines Manual Start - APU control panel - HYDROLYCS]
    "shutoff_b2": "I07_a23", # SHUT OFF B2 [K4 Верхний пульт] [Верхний пульт] [04 - 05 - 06 Engines Manual Start - APU control panel - HYDROLYCS]
    "shutoff_b3": "I07_a24", # SHUT OFF B3 [K4 Верхний пульт] [Верхний пульт] [04 - 05 - 06 Engines Manual Start - APU control panel - HYDROLYCS]
    "shutoff_c2": "I07_a25", # SHUT OFF C2 [K4 Верхний пульт] [Верхний пульт] [04 - 05 - 06 Engines Manual Start - APU control panel - HYDROLYCS]
    "bat1": "I07_b17", # BAT 1 [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
    "bat2": "I07_b18", # BAT 2 [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
    "pack_crew_off": "I07_a28", # PACK crew OFF [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
    "pack_normal": "I07_a29", # PACK NORMAL [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
    "pack_backup": "I07_a30", # PACK BACKUP [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
    "pack_emerg": "I07_a31", # PACK EMERG [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
    "pack_pax_off": "I07_a32", # PACK pax OFF [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
    "bag_isol": "I07_b02", # BAG ISOL [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
    "dump": "I07_b30", # DUMP [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
    "pressu_man": "I07_b32", # PRESSU MAN [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
    "cabin_alt_climb": "I07_c01", # CABIN ALT CLIMB [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
    "cabin_alt_descent": "I07_c02", # CABIN ALT DESCENT [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
    "backup_13": "I07_c13", # BACK UP 1<-->3 [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
    "xbp_12": "I07_c17", # X-BP 1<-->2 [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
    "xbp_13": "I07_c18", # X-BP 1<-->3 [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
    "xbp_23": "I07_c19", # X-BP 2<-->3 [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
    "xtk_down_1": "I07_c20", # XTK DOWN 1 [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
    "xtk_down_2": "I07_c21", # XTK DOWN 2 [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
    "xtk_up_1": "I07_c24", # XTK UP 1 [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
    "xtk_up_2": "I07_c25", # XTK UP 2 [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
    "pax_oxygen_closed": "I07_c09", # Selector CLOSED [K4 Верхний пульт] [Верхний пульт] [11 - 12 - 13 WINDSHEILD HEAT - PILOT HEAT - PAX OXYGEN]
    "pax_oxygen_firstaid": "I07_c10", # Selector switch FIRST AID [K4 Верхний пульт] [Верхний пульт] [11 - 12 - 13 WINDSHEILD HEAT - PILOT HEAT - PAX OXYGEN]
    "pax_oxygen_normal": "I07_c11", # Selector switch NORMAL [K4 Верхний пульт] [Верхний пульт] [11 - 12 - 13 WINDSHEILD HEAT - PILOT HEAT - PAX OXYGEN]
    "pax_oxygen_oride": "I07_c12", # Selector switch O'RIDE [K4 Верхний пульт] [Верхний пульт] [11 - 12 - 13 WINDSHEILD HEAT - PILOT HEAT - PAX OXYGEN]
    "el_landing_rh_off": "I07_c28", # SWITCH LANDING 1 OFF [K4 Верхний пульт] [Верхний пульт] [15 EXTERIOR LIGHTS + RAIN RPLNT LH]
    "el_landing_rh_on": "I07_c29", # SWITCH LANDING 1 ON [K4 Верхний пульт] [Верхний пульт] [15 EXTERIOR LIGHTS + RAIN RPLNT LH]
    "el_landing_rh_pulse": "I07_c30", # SWITCH LANDING 1 PULSE [K4 Верхний пульт] [Верхний пульт] [15 EXTERIOR LIGHTS + RAIN RPLNT LH]
    "el_landing_lh_off": "I07_c31", # SWITCH LANDING 2 OFF [K4 Верхний пульт] [Верхний пульт] [15 EXTERIOR LIGHTS + RAIN RPLNT LH]
    "el_landing_lh_on": "I07_c32", # SWITCH LANDING 2 ON [K4 Верхний пульт] [Верхний пульт] [15 EXTERIOR LIGHTS + RAIN RPLNT LH]
    "el_landing_lh_pulse": "I08_a01", # SWITCH LANDING 2 PULSE [K4 Верхний пульт] [Верхний пульт] [15 EXTERIOR LIGHTS + RAIN RPLNT LH]
    "il_emerge_lights_arm": "I08_a08", # SWITCH ARM [K4 Верхний пульт] [Верхний пульт] [16 - 17 COCKPIT LIGHTS - INTERIOR LIGHTS + RAIN RPLNT RH]
    "il_emerge_lights_off": "I08_a09", #  SWITCH OFF [K4 Верхний пульт] [Верхний пульт] [16 - 17 COCKPIT LIGHTS - INTERIOR LIGHTS + RAIN RPLNT RH]
    "il_emerge_lights_on": "I08_a10", # SWITCH ON [K4 Верхний пульт] [Верхний пульт] [16 - 17 COCKPIT LIGHTS - INTERIOR LIGHTS + RAIN RPLNT RH]
	"fire_test": "I07_a09", # FIRE TEST [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
    "tb_reserv_lh": "I08_a16", # TrackBall io [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [08 Пульт трэкбола левый (Trackball)]
    "tb_reserv_rh": "I08_a21", # TrackBall io [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [07 Пульт трэкбола правый (Trackball)] 
    "wc_backup_slats": "I03_b02", # BACK-UP SLATS [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [06 Пульт управления механизацией крыла]
    "apu_master": "I07_a18", # APU Master [K4 Верхний пульт] [Верхний пульт] [04 - 05 - 06 Engines Manual Start - APU control panel - HYDROLYCS]
    "ep_aural_warn_1": "I03_a22", # AURAL WARN 1 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [12  (Emergency Panel)]
    "ep_aural_warn_2": "I03_a23", # AURAL WARN 1 [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [12  (Emergency Panel)]
} # switches


uso_rotate_switch_receive_map = {
    "vhf_control_lh": "I06_b28", # second bit for rotate switch (IO) always comes next in uso packet so we dont need its index
    "baro_rot_lh": "I06_c01", # BARO IO left [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "fp_speed_kts_mach": "I06_c06", # CHG I0 [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "fp_hdg_trk": "I06_c12", # SYNK I0 [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "fp_vs_path": "I06_c16", # PATH VS I0 [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "fp_asel": "I06_c22", # HEIGHT 100 - 1000 I0 [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "vhf_control_rh": "I06_b18", # VHF IO 1 right [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "baro_rot_rh": "I06_b23", # BARO IO right [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [21Пульт автопилота]
    "sfd_set": "I06_b03",  # SET IO [K2 Средний пульт (Pedestal)] [Приборная доска] [33 Attitude Display]
    "tb_set_top_lh": "I08_a12",	# SET io [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [08 Пульт трэкбола левый (Trackball)]
    "tb_set_bottom_lh": "I08_a14", # SET io [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [08 Пульт трэкбола левый (Trackball)]
    "tb_set_top_rh": "I08_a17",	# SET io [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [07 Пульт трэкбола правый (Trackball)]
    "tb_set_bottom_rh": "I08_a19", # SET io [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [07 Пульт трэкбола правый (Trackball)]
}


uso_floats_receive_map = {
   "pc_bank_lh": "A001", # Левая БРУ крен
   "pc_pitch_lh": "A002", # Левая БРУ тангаж
   "pc_right_brake_lh": "A003", # Лев пед правый тормоз
   "pc_left_brake_lh": "A004", # Лев пед левый тормоз
#    "pc_heading_lh": "A005", # Лев пед  датчик перемещений
   "pc_heading_lh": "A008", # Лев пед  датчик перемещений
   "pc_right_brake_rh": "A006", # Прав пед правый тормоз
   "pc_left_brake_rh": "A007", # Прав пед левый тормоз
   "pc_heading_rh": "A008", # Прав пед  датчик перемещений
   "pc_bank_rh": "A009", # Правая БРУ крен
   "pc_pitch_rh": "A010", # Правая БРУ тангаж
   "pc_throttle_1": "A015", # 01 hand Левая ручка
   "pc_throttle_2": "A016", # 02 hand Средняя ручка
   "pc_throttle_3": "A018", # 03 hand Правая ручка
   "pc_thrust_reverse": "A017", # 02 hand ball Доп ручка
   "wc_sf": "A019", # switch SLATS/FLAPS SF 2
   "wc_ab": "A020", # switch AIRBRAKES AB 2
   "aft_temp": "A029", # PAX AFT TEMP ADC=
   "fwd_temp": "A030", # PAX FWD TEMP ADC=
   "crew_temp": "A031", # CREW TEMP ADC=
   "crew_ratio": "A032", # CREW RATIO ADC=
   "pc_gear_float": "A011", # 02 Рычаг ручного выпуска шасси (# Кран-шасси #)
   "pc_parkbrake_half": "A012", # SWITCH BREAK PARK [K2 Средний пульт (Pedestal)] [Приборная доска] [03 - 15 Рукоятка аварийного/стояночного тормоза (#--#) - Кнопка-переключатель 115/220]
   "pc_parkbrake_full": "A013", # SWITCH BREAK PARK [K2 Средний пульт (Pedestal)] [Приборная доска] [03 - 15 Рукоятка аварийного/стояночного тормоза (#--#) - Кнопка-переключатель 115/220]
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
