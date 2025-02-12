from xplane.params import Params

class Subscribe:
    to_subscribe = [
        # (param, freq (for tcp it's accuracy, for udp its freq of time per sec), protocol)
        (Params["sim/time/total_running_time_sec"], 5, "udp"),
        (Params["sim/cockpit/electrical/night_vision_on"], None, "tcp"),
        (Params["sim/operation/override/override_joystick"], None, "tcp"),
        (Params["sim/joystick/yoke_pitch_ratio"], 2, "udp"),
        (Params["sim/joystick/yoke_roll_ratio"], 2, "udp"),
        (Params["sim/joystick/yoke_heading_ratio"], 2, "udp"),
        (Params["sim/flightmodel/position/elevation"], 2, "udp"),
        (Params["sim/weapons/warhead_type"], None, "tcp"),
        (Params["sim/cockpit2/engine/actuators/fire_extinguisher_on"], None, "tcp"),
        (Params["sim/cockpit2/annunciators/engine_fires"], None, "tcp"),
        (Params["sim/weapons/mis_thrust2"], None, "tcp"),
        (Params["sim/weapons/mis_thrust3"], None, "tcp"),
        (Params["sim/cockpit/engine/APU_switch"], None, "tcp"),

        (Params["sim/cockpit2/controls/speedbrake_ratio"], None, "tcp"), # flight control - airbrake auto
        (Params["sim/cockpit2/switches/artificial_stability_on"], None, "tcp"), # fcs engage norm
        (Params["sim/cockpit2/switches/yaw_damper_on"], None, "tcp"), # fcs engage stby
        (Params["sim/cockpit2/controls/nosewheel_steer_on"], None, "tcp"), # fcs steering

        (Params["sim/cockpit2/electrical/APU_generator_on"], None, "tcp"), # apu master
        (Params["sim/cockpit2/electrical/APU_N1_percent"], 2, "udp"), # apu start stop
        (Params["sim/cockpit2/electrical/APU_starter_switch"], None, "tcp"), # apu start stop

        (Params["sim/custom/7x/selecthyd"], None, "tcp"), # backup pump hydraulics

        (Params["sim/custom/7x/lhmaster"], None, "tcp"), # dc supply - lh_master
        (Params["sim/custom/7x/lhinit"], None, "tcp"), # dc supply - lh init
        (Params["sim/cockpit2/electrical/cross_tie"], None, "tcp"), # dc supply - bus tie
        (Params["sim/custom/7x/rhinit"], None, "tcp"), # dc supply - rh init
        (Params["sim/custom/7x/rhmaster"], None, "tcp"), # dc supply - rh_master
        (Params["sim/cockpit/electrical/gpu_on"], None, "tcp"), # dc supply - ext power
        (Params["sim/cockpit2/electrical/generator_on"], None, "tcp"), # dc supply - gen 1
        (Params["sim/custom/7x/lhisol"], None, "tcp"), # dc supply - lh isol
        (Params["sim/cockpit2/switches/ram_air_turbine_on"], None, "tcp"), # dc supply - rat reset
        (Params["sim/custom/7x/rhisol"], None, "tcp"), # dc supply - rh isol
        (Params["sim/cockpit2/electrical/battery_on"], None, "tcp"), # dc supply - bat 1

        (Params["sim/weapons/target_index"], None, "tcp"), # air condition - pack
        (Params["sim/custom/7x/fpump0"], None, "tcp"), # fuel - boost1
        (Params["sim/7x/bt1f3"], None, "tcp"), # fuel - xtk 1
        (Params["sim/7x/bt3f1"], None, "tcp"), # fuel - xtk 2
        (Params["sim/custom/7x/fpump2"], None, "tcp"), # fuel - boost 3
        (Params["sim/7x/bt1f2"], None, "tcp"), # fuel - xtk 3
        (Params["sim/7x/bt3f2"], None, "tcp"), # fuel - xtk 4
        (Params["sim/7x/bk13"], None, "tcp"), # fuel - backup 1_3
        (Params["sim/7x/bt2f1"], None, "tcp"), # fuel - xtk 5
        (Params["sim/custom/7x/fpump1"], None, "tcp"), # fuel - boost2 
        (Params["sim/7x/bt2f3"], None, "tcp"), # fuel - xtk 6

        (Params["sim/custom/7x/AIwingsel"], None, "tcp"), # anti ice - wings
        (Params["sim/cockpit2/ice/ice_inlet_heat_on_per_engine"], None, "tcp"), # anti ice - eng 1
        (Params["sim/custom/7x/AIengcentre"], None, "tcp"), # anti ice - eng 2

        (Params["sim/custom/7x/overAPUaction"], None, "tcp"), # bleed - bleed apu
        (Params["sim/cockpit2/pressurization/actuators/dump_to_altitude_on"], None, "tcp"), 

        (Params["sim/cockpit2/ice/ice_pitot_heat_on_pilot"], None, "tcp"), # pitot heat - probe 12 
        (Params["sim/cockpit2/ice/ice_pitot_heat_on_copilot"], None, "tcp"), # pitot heat - probe 3
        (Params["sim/cockpit2/ice/ice_AOA_heat_on"], None, "tcp"), # pitot heat - probe 4
        (Params["sim/cockpit2/ice/ice_AOA_heat_on_copilot"], None, "tcp"), # windshield heat - lh
        (Params["sim/cockpit2/ice/ice_window_heat_on"], None, "tcp"), # windshield heat - rh
        (Params["sim/cockpit2/ice/ice_auto_ignite_on"], None, "tcp"), # windshield heat - backup

        (Params["sim/custom/7x/lum1"], None, "tcp"), # exterior lights - nav
        (Params["sim/custom/7x/lum2"], None, "tcp"), # exterior lights - anticol
        (Params["sim/cockpit2/switches/spot_light_on"], None, "tcp"), # exterior lights - wing
        (Params["sim/cockpit2/switches/landing_lights_switch"], None, "tcp"), # exterior lights - langing lh
        (Params["sim/cockpit/electrical/taxi_light_on"], None, "tcp"), # exterior lights - taxi

        (Params["sim/cockpit2/switches/instrument_brightness_ratio"], None, "tcp"), # exterior lights - overhead

        (Params["sim/cockpit2/switches/generic_lights_switch"], None, "tcp"), # interiorl lights - emerge lights
        (Params["sim/cockpit2/switches/fasten_seat_belts"], None, "tcp"), # interior lights - fasten belts
        (Params["sim/cockpit2/switches/no_smoking"], None, "tcp"), # interior lights - no smoking
        (Params["sim/custom/7x/paxlum"], None, "tcp"), # interior lights - cabin

        (Params["sim/cockpit2/annunciators/master_warning"], None, "tcp"), # front panel - master warning
        (Params["sim/cockpit2/annunciators/plugin_master_warning"], None, "tcp"), # front panel - master warning
        (Params["sim/cockpit2/annunciators/master_caution"], None, "tcp"),
        (Params["sim/cockpit2/annunciators/plugin_master_caution"], None, "tcp"),

        (Params["sim/cockpit2/radios/actuators/com1_standby_frequency_hz_833"], None, "tcp"), # front panel - vhf control lh
        (Params["sim/cockpit2/gauges/actuators/barometer_setting_in_hg_pilot"], None, "tcp"), # front panel - baro
        (Params["sim/custom/7x/flydir"], None, "tcp"), # front panel - FD/TD
        (Params["sim/cockpit/radios/ap_src"], None, "tcp"), # front panel - pilot side
        (Params["sim/cockpit/autopilot/autopilot_mode"], None, "tcp"), # front panel - autopilot on/off
        (Params["sim/weapons/targ_h"], None, "tcp"), # front panel - vs path
        (Params["sim/cockpit2/autopilot/vvi_status"], None, "tcp"), # front panel - vs mode
        (Params["sim/cockpit2/autopilot/fms_vnav"], None, "tcp"), #  front panel - vnav
        (Params["sim/cockpit2/autopilot/altitude_dial_ft"], None, "tcp"), # front panel - asel
        (Params["sim/cockpit2/autopilot/altitude_hold_armed"], None, "tcp"), # front panel - alt
        (Params["sim/cockpit2/gauges/actuators/barometer_setting_in_hg_copilot"], None, "tcp"), # secondary flight display - std
        (Params["sim/multiplayer/controls/flap_request"], None, "tcp"), # pedestal - wings config - slats/flats sf

        (Params["sim/cockpit2/engine/indicators/N1_percent[0]"], 2, "udp"), # synoptic indicator - eng - N1
        (Params["sim/cockpit2/engine/indicators/N1_percent[1]"], 2, "udp"), # synoptic indicator - eng - N1
        (Params["sim/cockpit2/engine/indicators/N1_percent[2]"], 2, "udp"), # synoptic indicator - eng - N1

        # Failures
        (Params["sim/operation/failures/rel_engfir0"], None, "tcp"), # engine 1 fire

        (Params["sim/operation/failures/rel_engfir3"], None, "tcp"), # fire rear comp
        (Params["sim/operation/failures/rel_engfir4"], None, "tcp"), # fire bag comp

        (Params["sim/operation/failures/rel_engfla0"], None, "tcp"),
        (Params["sim/operation/failures/rel_apu_fire"], None, "tcp"), # apu fire

        (Params["sim/operation/failures/rel_genera1"], None, "tcp"), # gen 2 fault

        (Params["sim/cockpit2/engine/indicators/N2_percent"], 1, "udp"), # eng N2
        (Params["sim/7x/choixtcas"], None, "tcp"), # PDU show ENG TRM

        (Params["sim/cockpit2/autopilot/airspeed_dial_kts_mach"], None, "tcp"), # front panel - airspeed val
        (Params["sim/cockpit/autopilot/airspeed_is_mach"], None, "tcp"), # front panel - airspeed kts or mach
        (Params["sim/cockpit2/autopilot/autothrottle_enabled"], None, "tcp"), # front panel - AT auto throttle
        (Params["sim/cockpit2/autopilot/approach_status"], None, "tcp"), # front panel - approach
        (Params["sim/cockpit2/autopilot/nav_status"], None, "tcp"), # front panel - lnav  
        (Params["sim/cockpit/autopilot/heading_mag"], None, "tcp"), # fron panel - hdg/trk
        (Params["sim/cockpit2/autopilot/heading_mode"], None, "tcp"), # front panel - hdg/trk mode

        (Params["sim/cockpit2/controls/left_brake_ratio"], 0.01, "tcp"), # pedal brake left
        (Params["sim/cockpit2/controls/right_brake_ratio"], None, "tcp"), # pedal brake right
        (Params["sim/cockpit2/engine/actuators/throttle_ratio"], None, "tcp"), # throttle

        (Params["sim/cockpit/weapons/firing_rate"], None, "tcp"), # synoptic page

        # our custom datarefs
        (Params["sim/custom/7x/z_eng1_oil_press_override"], None, "tcp"), # custom eng1 oil pressure
        (Params["sim/custom/7x/z_eng1_oil_press"], None, "tcp"), # custom eng1 oil pressure

        (Params["sim/custom/7x/z_syn_eng_start1"], None, "tcp"), # synoptic eng 1 start indication
    ]


    # get name by index for native xplane udp protocol
    udp_params_list = []
    udp_params_set = set()


def update_udp_lists():
    Subscribe.udp_params_list.clear()
    Subscribe.udp_params_set.clear()

    for (p, _, proto) in Subscribe.to_subscribe:
        if proto == "udp":
            Subscribe.udp_params_list.append(p)
            Subscribe.udp_params_set.add(p)


update_udp_lists()


def set_subscribe_params(params):
    Subscribe.to_subscribe = params
    update_udp_lists()
