"""""
Xplane parameters, failures & commands
"""

from enum import Enum


def to_str(self):
    return self.name


Params = Enum('XplaneParams', [
    "sim/time/total_running_time_sec",
    "sim/cockpit/electrical/night_vision_on",
    "sim/operation/override/override_joystick",
    "sim/operation/override/override_gearbrake",
    "sim/joystick/yoke_pitch_ratio",
    "sim/joystick/yoke_pitch_ratio_copilot",
    "sim/joystick/yoke_roll_ratio",
    "sim/joystick/yoke_roll_ratio_copilot",
    "sim/joystick/yoke_heading_ratio",
    "sim/joystick/yoke_heading_ratio_copilot",
    "sim/cockpit2/gauges/indicators/roll_electric_deg_pilot",
    "sim/cockpit2/gauges/indicators/pitch_electric_deg_pilot",
    "sim/flightmodel/position/elevation",
    "sim/weapons/warhead_type",
    "sim/cockpit2/engine/actuators/fire_extinguisher_on",
    "sim/cockpit2/annunciators/engine_fires",
    "sim/weapons/mis_thrust2",
    "sim/weapons/mis_thrust3",
    "sim/cockpit/engine/APU_switch",

    "sim/cockpit2/controls/speedbrake_ratio", # flight control - airbrake auto
    "sim/cockpit2/switches/artificial_stability_on", # fcs engage norm
    "sim/cockpit2/switches/yaw_damper_on", # fcs engage stby
    "sim/cockpit2/controls/nosewheel_steer_on", # fcs steering

    "sim/cockpit2/electrical/APU_generator_on", # apu master
    "sim/cockpit2/electrical/APU_N1_percent", # apu start stop
    "sim/cockpit2/electrical/APU_starter_switch", # apu start stop

    "sim/custom/7x/selecthyd", # backup pump hydraulics

    "sim/custom/7x/lhmaster", # dc supply - lh_master
    "sim/custom/7x/lhinit", # dc supply - lh init
    "sim/cockpit2/electrical/cross_tie", # dc supply - bus tie
    "sim/custom/7x/rhinit", # dc supply - rh init
    "sim/custom/7x/rhmaster", # dc supply - rh_master
    "sim/cockpit/electrical/gpu_on", # dc supply - ext power
    "sim/cockpit2/electrical/generator_on", # dc supply - gen 1
    "sim/custom/7x/lhisol", # dc supply - lh isol
    "sim/cockpit2/switches/ram_air_turbine_on", # dc supply - rat reset
    "sim/custom/7x/rhisol", # dc supply - rh isol
    "sim/cockpit2/electrical/battery_on", # dc supply - bat 1

    "sim/weapons/target_index", # air condition - pack
    "sim/custom/7x/fpump0", # fuel - boost1
    "sim/7x/bt1f3", # fuel - xtk 1
    "sim/7x/bt3f1", # fuel - xtk 2
    "sim/custom/7x/fpump2", # fuel - boost 3
    "sim/7x/bt1f2", # fuel - xtk 3
    "sim/7x/bt3f2", # fuel - xtk 4
    "sim/7x/bk13", # fuel - backup 1_3
    "sim/7x/bt2f1", # fuel - xtk 5
    "sim/custom/7x/fpump1", # fuel - boost2 
    "sim/7x/bt2f3", # fuel - xtk 6

    "sim/custom/7x/AIwingsel", # anti ice - wings
    "sim/cockpit2/ice/ice_inlet_heat_on_per_engine", # anti ice - eng 1
    "sim/custom/7x/AIengcentre", # anti ice - eng 2

    "sim/custom/7x/overAPUaction", # bleed - bleed apu
    "sim/cockpit2/pressurization/actuators/dump_to_altitude_on", 

    "sim/cockpit2/ice/ice_pitot_heat_on_pilot", # pitot heat - probe 12 
    "sim/cockpit2/ice/ice_pitot_heat_on_copilot", # pitot heat - probe 3
    "sim/cockpit2/ice/ice_AOA_heat_on", # pitot heat - probe 4
    "sim/cockpit2/ice/ice_AOA_heat_on_copilot", # windshield heat - lh
    "sim/cockpit2/ice/ice_window_heat_on", # windshield heat - rh
    "sim/cockpit2/ice/ice_auto_ignite_on", # windshield heat - backup

    "sim/custom/7x/lum1", # exterior lights - nav
    "sim/custom/7x/lum2", # exterior lights - anticol
    "sim/cockpit2/switches/spot_light_on", # exterior lights - wing
    "sim/cockpit2/switches/landing_lights_switch", # exterior lights - langing lh
    "sim/cockpit/electrical/taxi_light_on", # exterior lights - taxi

    "sim/cockpit2/switches/instrument_brightness_ratio", # exterior lights - overhead

    "sim/cockpit2/switches/generic_lights_switch", # interiorl lights - emerge lights
    "sim/cockpit2/switches/fasten_seat_belts", # interior lights - fasten belts
    "sim/cockpit2/switches/no_smoking", # interior lights - no smoking
    "sim/custom/7x/paxlum", # interior lights - cabin

    "sim/cockpit2/annunciators/master_warning", # front panel - master warning
    "sim/cockpit2/annunciators/plugin_master_warning", # front panel - master warning
    "sim/cockpit2/annunciators/master_caution",
    "sim/cockpit2/annunciators/plugin_master_caution",

    "sim/cockpit2/radios/actuators/com1_standby_frequency_hz_833", # front panel - vhf control lh
    "sim/cockpit2/gauges/actuators/barometer_setting_in_hg_pilot", # front panel - baro
    "sim/custom/7x/flydir", # front panel - FD/TD
    "sim/cockpit/radios/ap_src", # front panel - pilot side
    "sim/cockpit/autopilot/autopilot_mode", # front panel - autopilot on/off
    "sim/weapons/targ_h", # front panel - vs path
    "sim/cockpit2/autopilot/vvi_status", # front panel - vs mode
    "sim/cockpit2/autopilot/fms_vnav", #  front panel - vnav
    "sim/cockpit2/autopilot/altitude_dial_ft", # front panel - asel
    "sim/cockpit2/autopilot/altitude_hold_armed", # front panel - alt
    "sim/cockpit2/gauges/actuators/barometer_setting_in_hg_copilot", # secondary flight display - std
    "sim/multiplayer/controls/flap_request", # pedestal - wings config - slats/flats sf

    # "sim/cockpit2/engine/indicators/N1_percent", # synoptic indicator - eng - N1
    "sim/cockpit2/engine/indicators/N1_percent[0]", # synoptic indicator - eng - N1
    "sim/cockpit2/engine/indicators/N1_percent[1]", # synoptic indicator - eng - N1
    "sim/cockpit2/engine/indicators/N1_percent[2]", # synoptic indicator - eng - N1

    "sim/cockpit2/engine/actuators/throttle_ratio[0]", # synoptic indicator - eng - throttle
    "sim/cockpit2/engine/actuators/throttle_ratio[1]",
    "sim/cockpit2/engine/actuators/throttle_ratio[2]",

    # Failures
    "sim/operation/failures/rel_engfir0", # engine 1 fire
    "sim/operation/failures/rel_engfir1", # engine 1 fire
    "sim/operation/failures/rel_engfir2", # engine 1 fire

    "sim/operation/failures/rel_engfir3", # fire rear comp
    "sim/operation/failures/rel_engfir4", # fire bag comp

    "sim/operation/failures/rel_engfla0",
    "sim/operation/failures/rel_apu_fire", # apu fire

    "sim/operation/failures/rel_genera1", # gen 2

    "sim/cockpit2/engine/indicators/N2_percent", # eng N2
    "sim/7x/choixtcas", # PDU show ENG TRM

    "sim/cockpit2/autopilot/airspeed_dial_kts_mach", # front panel - airspeed val
    "sim/cockpit/autopilot/airspeed_is_mach", # front panel - airspeed kts or mach
    "sim/cockpit2/autopilot/autothrottle_enabled", # front panel - AT auto throttle
    "sim/cockpit2/autopilot/approach_status", # front panel - approach
    "sim/cockpit2/autopilot/nav_status", # front panel - lnav  
    "sim/cockpit/autopilot/heading_mag", # fron panel - hdg/trk
    "sim/cockpit2/autopilot/heading_mode", # front panel - hdg/trk mode

    "sim/cockpit2/controls/left_brake_ratio", # pedal brake left
    "sim/cockpit2/controls/right_brake_ratio", # pedal brake right
    "sim/cockpit2/engine/actuators/throttle_ratio", # throttle

    "sim/cockpit/weapons/firing_rate", # synoptic page

    # our custom datarefs
    "sim/custom/7x/z_eng1_oil_press_override", # custom eng1 oil pressure
    "sim/custom/7x/z_eng1_oil_press", # custom eng1 oil pressure

    "sim/cockpit2/electrical/APU_EGT_c", # apu temp
    "sim/cockpit2/engine/indicators/ITT_deg_C[0]", # synoptic eng itt
    "sim/cockpit2/engine/indicators/ITT_deg_C[1]", # synoptic eng itt
    "sim/cockpit2/engine/indicators/ITT_deg_C[2]", # synoptic eng itt
    "sim/cockpit2/engine/indicators/N2_percent[0]", # synoptic eng n2
    "sim/cockpit2/engine/indicators/N2_percent[1]", # synoptic eng n2
    "sim/cockpit2/engine/indicators/N2_percent[2]", # synoptic eng n2
    "sim/cockpit2/engine/indicators/fuel_flow_kg_sec[0]", # synoptic eng ff
    "sim/cockpit2/engine/indicators/fuel_flow_kg_sec[1]", # synoptic eng ff
    "sim/cockpit2/engine/indicators/fuel_flow_kg_sec[2]", # synoptic eng ff
    "sim/cockpit2/engine/indicators/oil_pressure_psi[0]", # synoptic eng oil psi
    "sim/cockpit2/engine/indicators/oil_pressure_psi[1]",
    "sim/cockpit2/engine/indicators/oil_pressure_psi[2]",
    "sim/cockpit2/engine/indicators/oil_temperature_deg_C[0]", # synoptic eng oli temp
    "sim/cockpit2/engine/indicators/oil_temperature_deg_C[1]",
    "sim/cockpit2/engine/indicators/oil_temperature_deg_C[2]",

    "sim/custom/xap/maxin1", # synoptic eng n1 top digit

    "sim/custom/7x/z_syn_eng_start1", # synoptic eng - eng 1 START indication
    "sim/custom/7x/z_syn_eng_start2", # synoptic eng - eng 1 START indication
    "sim/custom/7x/z_syn_eng_start3", # synoptic eng - eng 1 START indication
    "sim/custom/7x/z_syn_eng_ign1", # synoptic eng - eng 1 IGN indication
    "sim/custom/7x/z_syn_eng_ign2", # synoptic eng - eng 1 IGN indication
    "sim/custom/7x/z_syn_eng_ign3", # synoptic eng - eng 1 IGN indication
    "sim/custom/7x/z_syn_eng_ab1", # synoptic eng - eng 1 A or B indication
    "sim/custom/7x/z_syn_eng_ab2", # synoptic eng - eng 1 A or B indication
    "sim/custom/7x/z_syn_eng_ab3", # synoptic eng - eng 1 A or B indication

    "sim/custom/7x/z_line_gen2_on", # synoptic elec - power line
    "sim/custom/7x/z_line_bat2_ratgen_on", # synoptic elec - power line
    "sim/custom/7x/z_line_apu_bat1_on", # synoptic elec - power line
    "sim/custom/7x/z_line_gen1_gen3_on", # synoptic elec - power line
    "sim/custom/7x/z_apu_startup_stage", # synoptic elec apu startup states

    "sim/flightmodel/controls/parkbrake", # park brake
    "sim/cockpit2/electrical/bus_volts[0]", # synoptic elec bus volts lh
    "sim/cockpit2/electrical/bus_volts[1]", # synoptic elec bus volts rh

    "sim/cockpit2/electrical/generator_amps[0]", # synoptic elec gen amps
    "sim/cockpit2/electrical/generator_amps[1]", # synoptic elec gen amps
    "sim/cockpit2/electrical/generator_amps[2]", # synoptic elec gen amps
    "sim/cockpit2/electrical/battery_amps[0]", # synopic elec bat amps
    "sim/cockpit2/electrical/battery_amps[1]",
    "sim/custom/7X/TBAT", # synoptic elec battery temp
    "sim/cockpit2/controls/gear_handle_down", # landing gear
    "sim/cockpit2/annunciators/gear_unsafe", # gear in transition
    "sim/cockpit2/electrical/APU_generator_amps", # synoptic elec apu amps

    "sim/custom/7x/z_oil_min_height_1", # synoptic eng oil min level
    "sim/custom/7x/z_oil_min_height_2", # synoptic eng oil min level
    "sim/custom/7x/z_oil_min_height_3", # synoptic eng oil min level

    "sim/custom/7x/z_left_black_screen" ,# pdu left
    "sim/custom/7x/z_right_black_screen", # pdu right
    "sim/custom/7x/z_middle_up_black_screen", # mdu up 
    "sim/custom/7x/z_middle_down_black_screen", # mdu down
    "sim/custom/7x/z_mini_black_screen", # aux screen
    "sim/custom/7x/z_fuel_digital_1", # disable fuel flow from python
    "sim/custom/7x/z_fuel_digital_2", # disable fuel flow from python
    "sim/custom/7x/z_fuel_digital_3", # disable fuel flow from python
    "sim/custom/7x/z_thrust_purple_max_deg_1", # max thrust degree of purple circle on synoptic indicator
    "sim/custom/7x/z_thrust_purple_max_deg_2", # max thrust degree of purple circle on synoptic indicator
    "sim/custom/7x/z_thrust_purple_max_deg_3", # max thrust degree of purple circle on synoptic indicator

    "sim/cockpit2/electrical/battery_on[0]", # bat 1
    "sim/cockpit2/annunciators/reverser_deployed", # thrust reverse deployed
    "sim/cockpit2/electrical/APU_running", # apu running
    "sim/flightmodel/position/y_agl", # altitude above ground
    "sim/cockpit2/gauges/indicators/altitude_ft_pilot",
    "sim/cockpit2/gauges/indicators/heading_AHARS_deg_mag_pilot", # heading
    "sim/cockpit2/gauges/indicators/airspeed_kts_pilot", # current airspeed
    "sim/cockpit2/clock_timer/local_time_hours", # utc time hours
    "sim/cockpit2/clock_timer/local_time_minutes", # utc time minutes
    "sim/cockpit2/gauges/indicators/vvi_fpm_pilot", # vertical speed ft per min adi
    "sim/flightmodel/position/true_airspeed", # true airspeed
    "sim/flightmodel2/position/groundspeed", # ground speed
    "sim/cockpit2/gauges/indicators/mach_pilot", # mach value on pilot side
    "sim/flightmodel/controls/elv_trim", # adi pitch indicator
])
Params.__str__ = to_str


Commands = Enum('XplaneCommands', [
    "sim/operation/toggle_main_menu",
    "sim/view/forward_with_nothing", # 1st person camera with nothing
    "sim/operation/reload_aircraft",
    "sim/operation/fix_all_systems",
    "sim/electrical/APU_start",
    "sim/electrical/APU_off",
    "sim/bleed_air/bleed_air_left", # bleed - bleed 1
    "sim/bleed_air/bleed_air_auto", # bleed - bleed 2
    "sim/bleed_air/bleed_air_right", # bleed - bleed 3
    "sim/pressurization/vvi_down", # pressurization - cabin alt
    "sim/pressurization/vvi_up", # pressurization - cabin alt
    "sim/annunciator/clear_master_warning", # front panel - master warning
    "sim/annunciator/clear_master_caution", # front panel - master caution
    "sim/autopilot/knots_mach_toggle", # front panel - speed mach or kts 
    "sim/autopilot/autothrottle_toggle", # front panel - auto throttle
    "sim/autopilot/approach", # front panel - change approach mode
    "sim/autopilot/NAV", # front panel - lnav
    "sim/autopilot/heading_sync", # front panel - hdg trk sync
    "sim/autopilot/heading", # front panel - hdg trk mode
    "sim/autopilot/vertical_speed", # front panel - vs mode
    "sim/autopilot/FMS", # front panel - vs mode
    "sim/autopilot/altitude_hold", # front panel - alt
    "sim/flight_controls/pitch_trim_up", # trim up
    "sim/flight_controls/rudder_trim_right", # rudder trim riguht
    "sim/flight_controls/rudder_trim_left",
    "sim/flight_controls/aileron_trim_right",
    "sim/flight_controls/aileron_trim_left",
    "sim/flight_controls/pitch_trim_down",
    "sim/engines/thrust_reverse_toggle",
    "sim/engines/thrust_reverse_hold",
    "sim/flight_controls/right_brake",
    "sim/flight_controls/left_brake",
])

Commands.__str__ = to_str
