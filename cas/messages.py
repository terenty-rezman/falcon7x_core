all_mssgs = {
    
}


def register(cls):
    all_mssgs[cls.text] = cls
    return cls


class Custom(type):
    def __str__(self):
       return self.text


class CASmssg(metaclass=Custom):
    isread = None
    text = None
    color = None
    park = None
    taxi = None
    cruise = None
    TO = None
    land = None


@register
class AVC_AGM_FAIL(CASmssg): 
    isread = False
    text = "AVC: AGM #+#+# FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False


@register
class AVC_ASCB_FAULT(CASmssg): 
    isread = False
    text = "AVC: ASCB FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False
    

@register
class AVC_APM_1_2_3_4_FAIL(CASmssg): 
    isread = False
    text = "AVC: APM 1+2+3+4 FAIL"
    color = "A"
    park = True
    taxi = False
    cruise = False
    TO = False
    land = False

@register
class AVC_APM_MISCOMPARE(CASmssg): 
    isread = False
    text = "AVC: APM MISCOMPARE"
    color = "A"
    park = True
    taxi = False
    cruise = False
    TO = False
    land = False

@register
class AVC_AURAL_WARN_1_2_FAIL(CASmssg): 
    isread = False
    text = "AVC: AURAL WARN 1+2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class AVC_CONFIG_MONITOR_1_2_FAIL(CASmssg): 
    isread = False
    text = "AVC: CONFIG MONITOR 1+2 FAIL"
    color = "A"
    park = True
    taxi = False
    cruise = False
    TO = False
    land = False

@register
class AVC_CONTROL_IO_1_2_FAIL(CASmssg): 
    isread = False
    text = "AVC: CONTROL IO 1+2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class AVC_DU_LH_UP_HI_TEMP(CASmssg): 
    isread = False
    text = "AVC: DU LH+UP HI TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class AVC_DU_LW_RH_HI_TEMP(CASmssg): 
    isread = False
    text = "AVC: DU LW+RH HI TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class AVC_GEN_IO_1_2_3_4_5_FAIL(CASmssg): 
    isread = False
    text = "AVC: GEN IO 1+2+3+4+5 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class AVC_LH_RH_CCD_CLC_FAULT(CASmssg): 
    isread = False
    text = "AVC: LH+RH CCD+CLC FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class AVC_LH_UP_LW_RH_DU_FAULT(CASmssg): 
    isread = False
    text = "AVC: LH+UP+LW+RH DU FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class AVC_MAU_F(CASmssg): 
    isread = False
    text = "AVC: MAU #+#+# F"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class AVC_MAU_1A_1B_HI_TEMP(CASmssg): 
    isread = False
    text = "AVC: MAU 1A+1B HI TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class AVC_MAU_2A_2B_HI_TEMP(CASmssg): 
    isread = False
    text = "AVC: MAU 2A+2B HI TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class AVC_MONIT_WARN_1_2_3_FAIL(CASmssg): 
    isread = False
    text = "AVC: MONIT WARN 1+2+3 FAIL"
    color = "A"
    park = True
    taxi = False
    cruise = False
    TO = False
    land = False

@register
class AVC_SYSTEM_CONFIG_ABNORM(CASmssg): 
    isread = False
    text = "AVC: SYSTEM CONFIG ABNORM"
    color = "A"
    park = True
    taxi = False
    cruise = False
    TO = False
    land = False

@register
class AVC_WEATHER_RADAR_FAIL(CASmssg): 
    isread = False
    text = "AVC: WEATHER RADAR FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class CHECK_STATUS(CASmssg): 
    isread = False
    text = "CHECK STATUS"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class IRS_ALIGNING_MOTION_DETECT(CASmssg): 
    isread = False
    text = "IRS ALIGNING MOTION DETECT"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class IRS_1_2_3_ADS_INPUT_FAULT(CASmssg): 
    isread = False
    text = "IRS 1+2+3: ADS INPUT FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class IRS_1_2_3_FAIL(CASmssg): 
    isread = False
    text = "IRS 1+2+3 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class IRS_1_2_3_POS_ENTRY_FAULT(CASmssg): 
    isread = False
    text = "IRS 1+2+3 POS ENTRY FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class NAV_FMS_1_2_3_FAIL(CASmssg): 
    isread = False
    text = "NAV: FMS 1+2+3 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class NAV_FMS_GPS_1_2_POS_MISC(CASmssg): 
    isread = False
    text = "NAV: FMS #/GPS 1+2 POS MISC"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class NAV_FMS_GPS_1_2_MONITOR(CASmssg): 
    isread = False
    text = "NAV: FMS/GPS 1+2 MONITOR"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class NAV_GPS_1_2_FAIL(CASmssg): 
    isread = False
    text = "NAV: GPS 1+2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class AVC_AURAL_WARN_1_2_INHIBIT(CASmssg): 
    isread = False
    text = "AVC AURAL WARN 1+2 INHIBIT"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class AVC_VALIDATE_CONFIG(CASmssg): 
    isread = False
    text = "AVC: VALIDATE CONFIG"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

# такой же есть для желтого цвета
@register
class CHECK_STATUS(CASmssg): 
    isread = False
    text = "CHECK STATUS"
    color = "W"
    park = False
    taxi = False
    cruise = True
    TO = False
    land = False

@register
class CIRS_1_2_3_NO_POS_ENTRY(CASmssg): 
    isread = False
    text = "IRS 1+2+3 NO POS ENTRY"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class AVC_RADIO_CAB_1_2_FAIL(CASmssg): 
    isread = False
    text = "AVC: RADIO CAB 1+2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class AVC_RADIO_CAB_1_2_FAN_FAIL(CASmssg): 
    isread = False
    text = "AVC: RADIO CAB 1+2 FAN FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class AVC_RADIO_CAB_1_2_HI_TEMP(CASmssg): 
    isread = False
    text = "AVC: RADIO CAB 1+2 HI TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COM_AUDIO_1_2_FAIL(CASmssg): 
    isread = False
    text = "COM: AUDIO 1+2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COM_HF_1_2_FAIL(CASmssg): 
    isread = False
    text = "COM: HF 1+2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COM_SATCOM_FAIL(CASmssg): 
    isread = False
    text = "COM: SATCOM FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COM_VHF_1_2_FAIL(CASmssg): 
    isread = False
    text = "COM: VHF 1+2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COM_VHF_1_2_3_FAIL(CASmssg): 
    isread = False
    text = "COM: VHF 1+2+3 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COM_VHF_1_2_3_HI_TEMP(CASmssg): 
    isread = False
    text = "COM: VHF 1+2+3 HI TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COM_XPDR_1_2_FAIL(CASmssg): 
    isread = False
    text = "COM: XPDR 1+2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class NAV_ADF_1_2_FAIL(CASmssg): 
    isread = False
    text = "NAV: ADF 1+2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class NAV_DME_1_2_FAIL(CASmssg): 
    isread = False
    text = "NAV: DME 1+2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False


@register
class NAV_RADALT_1_2_FAIL(CASmssg): 
    isread = False
    text = "NAV: RADALT 1+2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class NAV_VOR_LOC_1_2_FAIL(CASmssg): 
    isread = False
    text = "NAV: VOR/LOC 1+2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COM_HF_SELCAL(CASmssg): 
    isread = False
    text = "COM: HF# SELCAL"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COM_VHF_SELCAL(CASmssg): 
    isread = False
    text = "COM: VHF# SELCAL"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class AFCS_ADS_ALL_MISCOMPARE(CASmssg): 
    isread = False
    text = "AFCS: ADS ALL MISCOMPARE"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class AFCS_ADS_MISCOMPARE(CASmssg): 
    isread = False
    text = "AFCS: ADS # MISCCOMPARE"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class AFCS_AP_FAIL(CASmssg): 
    isread = False
    text = "AFCS: AP FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class AFCS_IRS_ALL_MISCCOMPARE(CASmssg): 
    isread = False
    text = "AFCS: IRS ALL MISCCOMPARE"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class AFCS_IRS_MISCOMPARE(CASmssg): 
    isread = False
    text = "AFCS: IRS # MISCOMPARE"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class AFCS_FD_GA_DEGRADED_MODE(CASmssg): 
    isread = False
    text = "AFCS: FD GA DEGRADED MODE"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class AFCS_FD_TO_MODE_INHIBITED(CASmssg): 
    isread = False
    text = "AFCS: FD TO MODE INHIBITED"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class AVC_TCAS_FAIL(CASmssg): 
    isread = False
    text = "AVC: TCAS FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class TAWS_EGPWS_1_FAIL(CASmssg): 
    isread = False
    text = "TAWS: EGPWS 1 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class TAWS_EGPWS_1_2_FAIL(CASmssg): 
    isread = False
    text = "TAWS: EGPWS 1+2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class TAWS_GND_PROX_1_FAIL(CASmssg): 
    isread = False
    text = "TAWS: GND PROX 1 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class TAWS_GND_PROX_1_2_FAIL(CASmssg): 
    isread = False
    text = "TAWS: GND PROX 1+2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class TAWS_TERR_1_FAIL(CASmssg): 
    isread = False
    text = "TAWS: TERR 1 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class TAWS_TERR_1_2_FAIL(CASmssg): 
    isread = False
    text = "TAWS: TERR 1+2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class TAWS_WINDSHEAR_1_FAIL(CASmssg): 
    isread = False
    text = "TAWS: WINDSHEAR 1 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class TAWS_WINDSHEAR_1_2_FAIL(CASmssg): 
    isread = False
    text = "TAWS: WINDSHEAR 1+2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class TAWS_FLAPS_OVERRIDE(CASmssg): 
    isread = False
    text = "TAWS: FLAPS OVERRIDE"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class TAWS_G_S_INHIBIT(CASmssg): 
    isread = False
    text = "TAWS: G/S INHIBIT"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class TAWS_TERRAIN_INHIBIT(CASmssg): 
    isread = False
    text = "TAWS: TERRAIN INHIBIT"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class CABIN_AFT_CAB_CALL(CASmssg): 
    isread = False
    text = "CABIN: AFT CAB CALL"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class CABIN_AFT_LAV_CALL(CASmssg): 
    isread = False
    text = "CABIN: AFT LAV CALL"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class CABIN_FWD_CAB_CALL(CASmssg): 
    isread = False
    text = "CABIN: FWD CAB CALL"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class CABIN_FWD_LAV_CALL(CASmssg): 
    isread = False
    text = "CABIN: FWD LAV CALL"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class CABIN_MID_CAB_CALL(CASmssg): 
    isread = False
    text = "CABIN: MID CAB CALL"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FONE_INCOMING_CALL(CASmssg): 
    isread = False
    text = "FONE: INCOMING CALL"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class HUD_HUD_2_3_NOT_AVAILABLE(CASmssg): 
    isread = False
    text = "HUD: HUD2/3 NOT AVAILABLE"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class HUD_SYSTEM_FAIL(CASmssg): 
    isread = False
    text = "HUD: SYSTEM FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class HUD_LVTO_NOT_AVAILABLE(CASmssg): 
    isread = False
    text = "HUD: LVTO NOT AVAILABLE"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class APP_CAT_2_NOT_AVAILABLE(CASmssg): 
    isread = False
    text = "APP: CAT 2 NOT AVAILABLE"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class APP_CHECK_ADS_SOURCE(CASmssg): 
    isread = False
    text = "APP: CHECK ADS SOURCE"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class APP_CHECK_BARO_SETTING(CASmssg): 
    isread = False
    text = "APP: CHECK BARO SETTING"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class APP_CHECK_RH_NAV(CASmssg): 
    isread = False
    text = "APP: CHECK RH NAV"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class APP_CHECK_COURSE(CASmssg): 
    isread = False
    text = "APP: CHECK COURSE"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class APP_CHECK_DUAL_COUPLE(CASmssg): 
    isread = False
    text = "APP: CHECK DUAL COUPLE"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class APP_CHECK_ILS_FREQ(CASmssg): 
    isread = False
    text = "APP: CHECK ILS FREQ"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class APP_CHECK_IRS_SOURCE(CASmssg): 
    isread = False
    text = "APP: CHECK IRS SOURCE"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class APP_CHECK_LH_NAV(CASmssg): 
    isread = False
    text = "APP: CHECK LH NAV"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class APP_CHECK_RA_SOURCE(CASmssg): 
    isread = False
    text = "APP: CHECK RA SOURCE"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class APP_ENGAGE_AP(CASmssg): 
    isread = False
    text = "APP: ENGAGE AP"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class APP_G_S_NOT_CAPTURED(CASmssg): 
    isread = False
    text = "APP: G/S NOT CAPTURED"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class APP_G_S_NOT_RECEIVED(CASmssg): 
    isread = False
    text = "APP: G/S NOT RECEIVED"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class APP_LOC_NOT_RECEIVED(CASmssg): 
    isread = False
    text = "APP: LOC NOT RECEIVED"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class APP_RA_NOT_RECEIVED(CASmssg): 
    isread = False
    text = "APP: RA NOT RECEIVED"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class APP_REVERT_IRSX(CASmssg): 
    isread = False
    text = "APP: REVERT IRSX"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class APP_REVERT_RAD_ALT(CASmssg): 
    isread = False
    text = "APP: REVERT RAD ALT"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class HUD_CONFIRM_RUNWAY_DATA(CASmssg): 
    isread = False
    text = "HUD: CONFIRM RUNWAY DATA"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class HUD_COMBINER_NOT_ALIGNED(CASmssg): 
    isread = False
    text = "HUD: COMBINER NOT ALIGNED"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class HUD_HUD3_DISENGAGE_AP(CASmssg): 
    isread = False
    text = "HUD: HUD3 DISENGAGE AP"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class COND_AFT_FCS_BOX_OVHT(CASmssg): 
    isread = False
    text = "15 COND: AFT FCS BOX OVHT"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class PRESS_CABIN_ALT_TOO_HI(CASmssg): 
    isread = False
    text = "90 PRESS: CABIN ALT TOO HI"
    color = "R"
    park = False
    taxi = False
    cruise = True
    TO = False
    land = True

@register
class COND_BAG_COMP_HI_TEMP(CASmssg): 
    isread = False
    text = "COND: BAG COMP HI TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COND_BAG_FAN_FAULT(CASmssg): 
    isread = False
    text = "COND: BAG FAN FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COND_BAG_ISOL_FAULT(CASmssg): 
    isread = False
    text = "COND: BAG ISOL FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COND_CREW_SUPPLY_FAIL(CASmssg): 
    isread = False
    text = "COND: CREW SUPPLY FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COND_CREW_TEMP_MODE_FAULT(CASmssg): 
    isread = False
    text = "COND: CREW TEMP MODE FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COND_EMERG_PACK_HI_TEMP(CASmssg): 
    isread = False
    text = "COND: EMERG PACK HI TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COND_GASPER_SENSOR_FAIL(CASmssg): 
    isread = False
    text = "COND: GASPER SENSOR FAIL"
    color = "A"
    park = True
    taxi = False
    cruise = False
    TO = False
    land = False

@register
class COND_GROUND_VENT_FAULT(CASmssg): 
    isread = False
    text = "COND: GROUND VENT FAULT"
    color = "A"
    park = False
    taxi = False
    cruise = True
    TO = False
    land = True

@register
class COND_LEAK_MONIT_FAIL(CASmssg): 
    isread = False
    text = "COND: LEAK MONIT FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COND_NORM_PACK_DEGRAD(CASmssg): 
    isread = False
    text = "COND: NORM PACK DEGRAD"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COND_NORM_PACK_FAIL(CASmssg): 
    isread = False
    text = "COND: NORM PACK FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COND_NOSE_CONE_HI_TEMP(CASmssg): 
    isread = False
    text = "COND: NOSE CONE HI TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COND_PAX_SUPPLY_LEAK(CASmssg): 
    isread = False
    text = "COND: PAX SUPPLY LEAK"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COND_PAX_SUPPLY_FAIL(CASmssg): 
    isread = False
    text = "COND: PAX SUPPLY FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COND_PAX_TEMP_MODE_FAULT(CASmssg): 
    isread = False
    text = "COND: PAX TEMP MODE FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class COND_RECIRCULATION_FAULT(CASmssg): 
    isread = False
    text = "COND: RECIRCULATION FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

# В пдф третий столбец с минусом, но отмечен цветом
@register
class COND_TEST_FAIL(CASmssg): 
    isread = False
    text = "COND: TEST FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class COND_XBLEED_ECS_FAULT(CASmssg): 
    isread = False
    text = "COND: XBLEED ECS FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class HUMID_AIR_LEAK(CASmssg): 
    isread = False
    text = "HUMID: AIR LEAK"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = True
    land = False

@register
class HUMID_LEAK_MONIT_FAIL(CASmssg): 
    isread = False
    text = "HUMID: LEAK MONIT FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class HUMIDIFIER_FAIL(CASmssg): 
    isread = False
    text = "HUMIDIFIER: FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class HUMIDIFIER_FAIL(CASmssg): 
    isread = False
    text = "HUMIDIFIER: FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class PRESS_AUTO_MODE_FAIL(CASmssg): 
    isread = False
    text = "PRESS: AUTO MODE FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class PRESS_BAG_VENT_LO(CASmssg): 
    isread = False
    text = "PRESS: BAG VENT LO"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class PRESS_BAG_VENT_HI(CASmssg): 
    isread = False
    text = "PRESS: BAG VENT HI"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class PRESS_CABIN_ALT_ABNORMAL(CASmssg): 
    isread = False
    text = "PRESS: CABIN ALT ABNORMAL"
    color = "A"
    park = False
    taxi = False
    cruise = True
    TO = False
    land = False

@register
class PRESS_CABIN_RATE_ABNORMAL(CASmssg): 
    isread = False
    text = "PRESS: CABIN RATE ABNORMAL"
    color = "A"
    park = False
    taxi = False
    cruise = True
    TO = False
    land = False

@register
class PRESS_DIFF_PRESS_HI(CASmssg): 
    isread = False
    text = "PRESS: DIFF PRESS HI"
    color = "A"
    park = False
    taxi = False
    cruise = True
    TO = False
    land = True

@register
class PRESS_LAND_ELEV_UNKNOWN(CASmssg): 
    isread = False
    text = "PRESS: LAND ELEV UNKNOWN"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class COND_TEST_IN_PROGRESS(CASmssg): 
    isread = False
    text = "COND: TEST IN PROGRESS"
    color = "W"
    park = True
    taxi = False
    cruise = False
    TO = False
    land = False

@register
class COND_TEST_WAITING_EMERG(CASmssg): 
    isread = False
    text = "COND: TEST WAITING EMERG"
    color = "W"
    park = True
    taxi = False
    cruise = False
    TO = False
    land = False

@register
class COND_TEST_WAITING_NORM(CASmssg): 
    isread = False
    text = "COND: TEST WAITING NORM"
    color = "W"
    park = True
    taxi = False
    cruise = False
    TO = False
    land = False

@register
class HUMID_FAULT(CASmssg): 
    isread = False
    text = "HUMID: FAULT"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class HUMID_WATER_LEAK(CASmssg): 
    isread = False
    text = "HUMID: WATER LEAK"
    color = "W"
    park = True
    taxi = True
    cruise = False
    TO = True
    land = False

@register
class PRESS_ALTITUDE_LIMIT(CASmssg): 
    isread = False
    text = "PRESS: ALTITUDE LIMIT"
    color = "W"
    park = False
    taxi = False
    cruise = True
    TO = False
    land = True

@register
class PRESS_HIGH_AIRFIELD_OPS(CASmssg): 
    isread = False
    text = "PRESS: HIGH AIRFIELD OPS"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class ELEC_AFT_DIST_BOX_OVHT(CASmssg): 
    isread = False
    text = "26 ELEC: AFT DIST BOX OVHT"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_BAT_1_OVHT(CASmssg): 
    isread = False
    text = "30 ELEC: BAT 1 OVHT"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_BAT_2_OVHT(CASmssg): 
    isread = False
    text = "31 ELEC: BAT 2 OVHT"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_BAT_1_2_OVHT(CASmssg): 
    isread = False
    text = "32 ELEC: BAT 1+2 OVHT"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_LH_RH_ESS_PWR_LO(CASmssg): 
    isread = False
    text = "36 ELEC: LH + RH ESS PWR LO"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_GEN_1_2_3_FAULT(CASmssg): 
    isread = False
    text = "38 ELEC: GEN 1+2+3 FAULT"
    color = "R"
    park = False
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_RAT_GEN_FAULT(CASmssg): 
    isread = False
    text = "40 ELEC: RAT GEN FAULT"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_AFT_DIST_BOX_HI_TEMP(CASmssg): 
    isread = False
    text = "ELEC: AFT DIST BOX HI TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class ELEC_APU_GEN_FAULT(CASmssg): 
    isread = False
    text = "ELEC: APU GEN FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class ELEC_BAT_1_2_HI_TEMP(CASmssg): 
    isread = False
    text = "ELEC: BAT 1+2 HI TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class ELEC_BAT_1_2_OFF(CASmssg): 
    isread = False
    text = "ELEC: BAT 1+2 OFF"
    color = "A"
    park = False
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_BAT_1_2_TEMP_IND_INOP(CASmssg): 
    isread = False
    text = "ELEC BAT 1+2 TEMP IND INOP"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class ELEC_BUS_MISCONFIG_TIED(CASmssg): 
    isread = False
    text = "ELEC: BUS MISCONFIG TIED"
    color = "A"
    park = False
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class ELEC_BUS_TIE_FAIL(CASmssg): 
    isread = False
    text = "ELEC: BUS TIE FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class ELEC_GEN_FAULT(CASmssg): 
    isread = False
    text = "ELEC: GEN # FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class ELEC_LH_AUTO_SHED_ACTIVE(CASmssg): 
    isread = False
    text = "ELEC: LH AUTO SHED ACTIVE"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class ELEC_LH_CONF_NOT_CHECKED(CASmssg): 
    isread = False
    text = "ELEC: LH CONF NOT CHECKED"
    color = "A"
    park = True
    taxi = False
    cruise = False
    TO = False
    land = False

@register
class ELEC_LH_ESS_FAULT(CASmssg): 
    isread = False
    text = "ELEC: LH ESS FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_LH_ESS_NO_PWR(CASmssg): 
    isread = False
    text = "ELEC: LH ESS NO PWR"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_LH_ESS_PWR_LO(CASmssg): 
    isread = False
    text = "ELEC: LH ESS PWR LO"
    color = "A"
    park = False
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class ELEC_LH_FRONT_ESS_FAIL(CASmssg): 
    isread = False
    text = "ELEC: LH FRONT ESS FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_LH_FRONT_MAIN_FAIL(CASmssg): 
    isread = False
    text = "ELEC: LH FRONT MAIN FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_LH_MAIN_FAULT(CASmssg): 
    isread = False
    text = "ELEC: LH MAIN FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_LH_MAIN_NO_PWR(CASmssg): 
    isread = False
    text = "ELEC: LH MAIN NO PWR"
    color = "A"
    park = False
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_LH_REAR_ESS_FAIL(CASmssg): 
    isread = False
    text = "ELEC: LH REAR ESS FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = True
    land = False

@register
class ELEC_LH_REAR_MAIN_FAIL(CASmssg): 
    isread = False
    text = "ELEC: LH REAR MAIN FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_OP_FAIL(CASmssg): 
    isread = False
    text = "ELEC: OP FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class ELEC_RAT_GCU_TEST_FAIL(CASmssg): 
    isread = False
    text = "ELEC: RAT GCU TEST FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_RAT_HEATER_TEST_FAIL(CASmssg): 
    isread = False
    text = "ELEC: RAT HEATER TEST FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_RH_AUTO_SHED_ACTIVE(CASmssg): 
    isread = False
    text = "ELEC: RH AUTO SHED ACTIVE"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class ELEC_RH_CONF_NOT_CHECKED(CASmssg): 
    isread = False
    text = "ELEC: RH CONF NOT CHECKED"
    color = "A"
    park = True
    taxi = False
    cruise = False
    TO = False
    land = False

@register
class ELEC_RH_ESS_FAULT(CASmssg): 
    isread = False
    text = "ELEC: RH ESS FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_RH_ESS_NO_PWR(CASmssg): 
    isread = False
    text = "ELEC: RH ESS NO PWR"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_RH_ESS_PWR_LO(CASmssg): 
    isread = False
    text = "ELEC: RH ESS PWR LO"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class ELEC_RH_FRONT_ESS_FAIL(CASmssg): 
    isread = False
    text = "ELEC: RH FRONT ESS FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_RH_FRONT_MAIN_FAIL(CASmssg): 
    isread = False
    text = "ELEC: RH FRONT MAIN FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_RH_MAIN_FAULT(CASmssg): 
    isread = False
    text = "ELEC: RH MAIN FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_RH_MAIN_NO_PWR(CASmssg): 
    isread = False
    text = "ELEC: RH MAIN NO PWR"
    color = "A"
    park = False
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_RH_REAR_ESS_FAIL(CASmssg): 
    isread = False
    text = "ELEC: RH REAR ESS FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_RH_REAR_MAIN_FAIL(CASmssg): 
    isread = False
    text = "ELEC: RH REAR MAIN FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = True
    land = False

@register
class ELEC_BUS_MISCONFIG_UNTIED(CASmssg): 
    isread = False
    text = "ELEC: BUS MISCONFIG UNTIED"
    color = "W"
    park = True
    taxi = False
    cruise = False
    TO = False
    land = False

@register
class ELEC_RAT_TEST_IN_PROGRESS(CASmssg): 
    isread = False
    text = "ELEC: RAT TEST IN PROGRESS"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ELEC_RAT_AUTO_INHIBIT(CASmssg): 
    isread = False
    text = "ELEC: RAT AUTO INHIBIT"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class ELEC_RH_ESS_ISOL(CASmssg): 
    isread = False
    text = "ELEC: RH ESS ISOL"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FIRE_APU(CASmssg): 
    isread = False
    text = "72 FIRE: APU"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FIRE_ENG_1(CASmssg): 
    isread = False
    text = "74 FIRE: ENG 1"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FIRE_ENG_2(CASmssg): 
    isread = False
    text = "75 FIRE: ENG 2"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FIRE_ENG_3(CASmssg): 
    isread = False
    text = "76 FIRE: ENG 3"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FIRE_REAR_COMP(CASmssg): 
    isread = False
    text = "78 FIRE: REAR COMP"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FIRE_LH_RH_WHEEL_OVHT(CASmssg): 
    isread = False
    text = "80 FIRE: LH+RH WHEEL OVHT"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class SMOKE_AFT_CAB(CASmssg): 
    isread = False
    text = "95 SMOKE: AFT CAB"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class SMOKE_BAG_COMP(CASmssg): 
    isread = False
    text = "96 SMOKE: BAG COMP"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class SMOKE_AFT_LAV(CASmssg): 
    isread = False
    text = "98 SMOKE: AFT LAV"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class SMOKE_FWD_LAV(CASmssg): 
    isread = False
    text = "98 SMOKE: FWD LAV"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class SMOKE_CREW_REST(CASmssg): 
    isread = False
    text = "98 SMOKE: CREW REST"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FIRE_APU_DETECT_FAIL(CASmssg): 
    isread = False
    text = "FIRE APU DETECT FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FIRE_ENG_1_2_3_DETECT_FAIL(CASmssg): 
    isread = False
    text = "FIRE ENG 1+2+3 DETECT FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FIRE_REAR_COMP_DETECT_FAIL(CASmssg): 
    isread = False
    text = "FIRE REAR COMP DETECT FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FIRE_WHEEL_DETECT_FAIL(CASmssg): 
    isread = False
    text = "FIRE WHEEL DETECT FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FIRE_TEST_FAIL(CASmssg): 
    isread = False
    text = "FIRE TEST FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class SMOKE_AFT_CAB_DETECT_FAIL(CASmssg): 
    isread = False
    text = "SMOKE: AFT CAB DETECT FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class SMOKE_AFT_LAV_DETECT_FAIL(CASmssg): 
    isread = False
    text = "SMOKE: AFT LAV DETECT FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class SMOKE_BAG_COMP_DETECT_FAIL(CASmssg): 
    isread = False
    text = "SMOKE BAG COMP DETECT FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

# В пдф в четвертом столбце стоит А, но не отмечена цветом
@register
class SMOKE_CREW_REST_DETECT_FAIL(CASmssg): 
    isread = False
    text = "SMOKE: CREW REST DETECT FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = False

@register
class SMOKE_FWD_LAV_DETECT_FAIL(CASmssg): 
    isread = False
    text = "SMOKE: FWD LAV DETECT FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FIRE_TEST_IN_PROGRESS(CASmssg): 
    isread = False
    text = "FIRE: TEST IN PROGRESS"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_BACK_UP_ACTIVE(CASmssg): 
    isread = False
    text = "60 FCS: BACK-UP ACTIVE"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_DIRECT_LAWS_ACTIVE(CASmssg): 
    isread = False
    text = "66 FCS: DIRECT LAWS ACTIVE"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_THS_PROT_FAIL(CASmssg): 
    isread = False
    text = "69 FCS: THS PROT FAIL"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_A_B_AUTO_EXTEND_FAIL(CASmssg): 
    isread = False
    text = "FCS: A/B AUTO EXTEND FAIL"
    color = "R"
    park = False
    taxi = True
    cruise = False
    TO = True
    land = True

@register
class FCS_A_B_AUTO_RETRACT_FAIL(CASmssg): 
    isread = False
    text = "FCS: A/B AUTO RETRACT FAIL"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_CONTROL_SURFACE_JAM(CASmssg): 
    isread = False
    text = "FCS: CONTROL SURFACE JAM"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_LH_SIDESTICKS_FAIL(CASmssg): 
    isread = False
    text = "FCS: LH SIDESTICKS FAIL"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_RH_SIDESTICKS_FAIL(CASmssg): 
    isread = False
    text = "FCS: RH SIDESTICKS FAIL"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class NO_TAKE_OFF(CASmssg): 
    isread = False
    text = "NO TAKE OFF"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class A_I_STALL_WARNING_OFFSET(CASmssg): 
    isread = False
    text = "A/I: STALL WARNING OFFSET"
    color = "A"
    park = False
    taxi = False
    cruise = True
    TO = False
    land = False

@register
class FCS_A_B_1_2_EXTEND_FAIL(CASmssg): 
    isread = False
    text = "FCS: A/B 1+2 EXTEND FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_A_B_1_2_RETRACT_FAIL(CASmssg): 
    isread = False
    text = "FCS: A/B 1+2 RETRACT FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_ALTN_LAWS_ACTIVE(CASmssg): 
    isread = False
    text = "FCS: ALTN LAWS ACTIVE"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_AILERON_DEGRAD(CASmssg): 
    isread = False
    text = "FCS: AILERON DEGRAD"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_BOTH_AILERONS_FAIL(CASmssg): 
    isread = False
    text = "FCS: BOTH AILERONS FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_BOTH_ELEVATORS_FAIL(CASmssg): 
    isread = False
    text = "FCS: BOTH ELEVATORS FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_E1_E2_MAINT_MODE(CASmssg): 
    isread = False
    text = "FCS: E1+E2 MAINT MODE"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FCS_ELEVATOR_DEGRAD(CASmssg): 
    isread = False
    text = "FCS: ELEVATOR DEGRAD"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_FLAP_ASYM(CASmssg): 
    isread = False
    text = "FCS: FLAP ASYM"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_FLAP_FAIL(CASmssg): 
    isread = False
    text = "FCS: FLAP FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_LH_SIDESTICK_DEGRAD(CASmssg): 
    isread = False
    text = "FCS: LH SIDESTICK DEGRAD"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_MFCC_FAULT(CASmssg): 
    isread = False
    text = "FCS: MFCC FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_NO_DISPATCH(CASmssg): 
    isread = False
    text = "FCS: NO DISPATCH"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class FCS_ONE_AILERON_FAIL(CASmssg): 
    isread = False
    text = "FCS: ONE AILERON FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_ONE_ELEVATOR_FAIL(CASmssg): 
    isread = False
    text = "FCS: ONE ELEVATOR FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_PITCH_AUTOTRIM_INOP(CASmssg): 
    isread = False
    text = "FCS: PITCH AUTOTRIM INOP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_PITCH_MAN_TRIM_FAIL(CASmssg): 
    isread = False
    text = "FCS: PITCH MAN TRIM FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class FCS_RH_SIDESTICK_DEGRAD(CASmssg): 
    isread = False
    text = "FCS: RH SIDESTICK DEGRAD"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_ROLL_MAN_TRIM_FAIL(CASmssg): 
    isread = False
    text = "FCS: ROLL MAN TRIM FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class FCS_RUDDER_DEGRAD(CASmssg): 
    isread = False
    text = "FCS: RUDDER DEGRAD"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FCS_RUDDER_FAIL(CASmssg): 
    isread = False
    text = "FCS: RUDDER FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_RUDDER_PEDAL_INOP(CASmssg): 
    isread = False
    text = "FCS: RUDDER PEDAL INOP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_SFCC_FAULT(CASmssg): 
    isread = False
    text = "FCS: SFCC FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class FCS_SLATS_INB_AUTO_FAIL(CASmssg): 
    isread = False
    text = "FCS: SLATS INB AUTO FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FCS_SLATS_INB_EXTEND_FAIL(CASmssg): 
    isread = False
    text = "FCS: SLATS INB EXTEND FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_SLATS_M_O_AUTO_FAIL(CASmssg): 
    isread = False
    text = "FCS: SLATS M+O AUTO FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_SLATS_M_O_EXTEND_FAIL(CASmssg): 
    isread = False
    text = "FCS: SLATS M+O EXTEND FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_SLATS_M_O_RETRACT_FAIL(CASmssg): 
    isread = False
    text = "FCS SLATS M+O RETRACT FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_SPOILERS_FAIL(CASmssg): 
    isread = False
    text = "FCS: SPOILERS FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_TEST_FAIL(CASmssg): 
    isread = False
    text = "FCS: TEST FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

# В пдф в первом столбце -, но отмечено цветом
@register
class FCS_TEST_NOT_PERFORMED(CASmssg): 
    isread = False
    text = "FCS: TEST NOT PERFORMED"
    color = "A"
    park = False
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class FCS_THS_DEGRAD(CASmssg): 
    isread = False
    text = "FCS: THS DEGRAD"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_TRIM_LIMIT(CASmssg): 
    isread = False
    text = "FCS: TRIM LIMIT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FCS_YAW_MAN_TRIM_FAIL(CASmssg): 
    isread = False
    text = "FCS: YAW MAN TRIM FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class CONF_FLAPS_MISCONFIG_FULL(CASmssg): 
    isread = False
    text = "CONF: FLAPS MISCONFIG FULL"
    color = "W"
    park = False
    taxi = False
    cruise = True
    TO = True
    land = False

@register
class FCS_A_B_AUTO_EXTEND_OFF(CASmssg): 
    isread = False
    text = "FCS: A/B AUTO EXTEND OFF"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class LDG_CONF_FLAPS_NOT_FULL(CASmssg): 
    isread = False
    text = "LDG CONF:FLAPS NOT FULL"
    color = "W"
    park = False
    taxi = False
    cruise = True
    TO = False
    land = True

@register
class TO_CONF_AB_MISCONFIG(CASmssg): 
    isread = False
    text = "TO CONF: AB MISCONFIG"
    color = "W"
    park = False
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class TO_CONF_FLAPS_MISCONFIG(CASmssg): 
    isread = False
    text = "TO CONF: FLAPS MISCONFIG"
    color = "W"
    park = False
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class FUEL_ENG_1_2_3_LO_PRESS(CASmssg): 
    isread = False
    text = "FUEL: ENG 1+2+3 LO PRESS"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FUEL_GAUGING_DEGRAD(CASmssg): 
    isread = False
    text = "FUEL: GAUGING DEGRAD"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FUEL_LO_TEMP(CASmssg): 
    isread = False
    text = "FUEL: LO TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FUEL_PRESS_VALVE_FAULT(CASmssg): 
    isread = False
    text = "FUEL: PRESS VALVE FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FUEL_TK_1_2_3_LO_LVL(CASmssg): 
    isread = False
    text = "FUEL: TK 1+2+3 LO LVL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class FUEL_TKS_LVL_MISCONFIG(CASmssg): 
    isread = False
    text = "FUEL: TKS LVL MISCONFIG"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FUEL_X_BP_1_3_B_U_FAIL(CASmssg): 
    isread = False
    text = "FUEL: X-BP 1-3 B/U FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FUEL_X_BP_1_2_FAIL(CASmssg): 
    isread = False
    text = "FUEL: X-BP 1-2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FUEL_X_BP_2_3_FAIL(CASmssg): 
    isread = False
    text = "FUEL: X-BP 2-3 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FUEL_X_BP_1_3_FAULT(CASmssg): 
    isread = False
    text = "FUEL: X-BP 1-3 FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

# в пдф повторяется 
# возможно там не 1-3, а 3-1 как в следующих двух строках
@register
class FUEL_X_BP_1_3_FAULT(CASmssg): 
    isread = False
    text = "FUEL: X-BP 1-3 FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FUEL_X_TK_1_3_B_U_FAIL(CASmssg): 
    isread = False
    text = "FUEL: X-TK 1-3 B/U FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FUEL_X_TK_3_1_B_U_FAIL(CASmssg): 
    isread = False
    text = "FUEL: X-TK 3-1 B/U FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FUEL_X_TK_1_2_FAIL(CASmssg): 
    isread = False
    text = "FUEL: X-TK 1-2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FUEL_X_TK_2_1_FAIL(CASmssg): 
    isread = False
    text = "FUEL: X-TK 2-1 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FUEL_X_TK_3_2_FAIL(CASmssg): 
    isread = False
    text = "FUEL: X-TK 3-2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FUEL_X_TK_2_3_FAIL(CASmssg): 
    isread = False
    text = "FUEL: X-TK 2-3 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FUEL_X_TK_1_3_FAULT(CASmssg): 
    isread = False
    text = "FUEL: X-TK 1-3 FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FUEL_X_TK_3_1_FAULT(CASmssg): 
    isread = False
    text = "FUEL: X-TK 3-1 FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FUEL_WINGS_QTY_MISMATCH(CASmssg): 
    isread = False
    text = "FUEL: WINGS QTY MISMATCH"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FUEL_VENT_VALVE_FAULT(CASmssg): 
    isread = False
    text = "FUEL: VENT VALVE FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class DOOR_FUEL_NOT_CLOSED(CASmssg): 
    isread = False
    text = "DOOR: FUEL NOT CLOSED"
    color = "W"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class FUEL_TK_1_2_3_LO_LVL(CASmssg): 
    isread = False
    text = "FUEL: TK 1+2+3 LO LVL"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class FUEL_TK_1_2_3_LVL(CASmssg): 
    isread = False
    text = "FUEL: TK 1+2+3 LVL"
    color = "W"
    park = True
    taxi = True
    cruise = False
    TO = True
    land = False

@register
class FUEL_X_CMD_INVALID_INPUTS(CASmssg): 
    isread = False
    text = "FUEL: X-CMD INVALID INPUTS"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class HYD_A_OVHT(CASmssg): 
    isread = False
    text = "84 HYD: A OVHT"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class HYD_B_OVHT(CASmssg): 
    isread = False
    text = "85 HYD: B OVHT"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class HYD_C_OVHT(CASmssg): 
    isread = False
    text = "86 HYD: C OVHT"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class HYD_A_B_C_LO_PRESS(CASmssg): 
    isread = False
    text = "HYD: A+B+C LO PRESS"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class HYD_A_B_C_LO_QTY(CASmssg): 
    isread = False
    text = "HYD: A+B+C LO QTY"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class HYD_A_B_C_HI_TEMP(CASmssg): 
    isread = False
    text = "HYD: A+B+C HI TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class HYD_BACKUP_PUMP_HI_TEMP(CASmssg): 
    isread = False
    text = "HYD: BACKUP PUMP HI TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class HYD_BACKUP_PUMP_ON_A(CASmssg): 
    isread = False
    text = "HYD: BACKUP PUMP ON A"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class HYD_PUMP_A1_A3_FAIL(CASmssg): 
    isread = False
    text = "HYD: PUMP A1+A3 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class HYD_PUMP_A3_D_PRESS_FAIL(CASmssg): 
    isread = False
    text = "HYD: PUMP A3 D-PRESS FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class HYD_PUMP_B2_B3_FAIL(CASmssg): 
    isread = False
    text = "HYD: PUMP B2+B3 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class HYD_PUMP_B2_D_PRESS_FAIL(CASmssg): 
    isread = False
    text = "HYD: PUMP B2 D-PRESS FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class HYD_SHUT_OFF_A_FAIL(CASmssg): 
    isread = False
    text = "HYD: SHUT OFF A# FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class HYD_SHUT_OFF_B_FAIL(CASmssg): 
    isread = False
    text = "HYD: SHUT OFF B# FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class HYD_SHUT_OFF_C2_FAIL(CASmssg): 
    isread = False
    text = "HYD: SHUT OFF C2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class A_I_BRAKE_HEATING_FAIL(CASmssg): 
    isread = False
    text = "A/I: BRAKE HEATING FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class A_I_ENG_1_2_3_LO_PRESS(CASmssg): 
    isread = False
    text = "A/I: ENG 1+2+3 LO PRESS"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class A_I_ENG_1_2_3_HI_PRESS(CASmssg): 
    isread = False
    text = "A/I: ENG 1+2+3 HI PRESS"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class A_I_ENG_1_2_3_RESID_PRESS(CASmssg): 
    isread = False
    text = "A/I: ENG 1+2+3 RESID PRESS"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class A_I_ENG_1_2_3_RESID_PRESS(CASmssg): 
    isread = False
    text = "A/I: ENG 1+2+3 RESID PRESS"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class A_I_ICE_DETECTED_1_2(CASmssg): 
    isread = False
    text = "A/I: ICE DETECTED 1+2"
    color = "A"
    park = True
    taxi = False
    cruise = True
    TO = False
    land = True

@register
class A_I_ICE_DETECT_1_2_FAIL(CASmssg): 
    isread = False
    text = "A/I: ICE DETECT 1+2 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class A_I_S_DUCT_FAULT(CASmssg): 
    isread = False
    text = "A/I: S-DUCT FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class A_I_S_DUCT_HI_TEMP(CASmssg): 
    isread = False
    text = "A/I: S-DUCT HI TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class A_I_S_DUCT_LO_PWR(CASmssg): 
    isread = False
    text = "A/I: S-DUCT LO PWR"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class A_I_TAT_TOO_HIGH(CASmssg): 
    isread = False
    text = "A/I: TAT TOO HIGH"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class A_I_WINGS_FAULT(CASmssg): 
    isread = False
    text = "A/I: WINGS FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class A_I_WINGS_LEAK(CASmssg): 
    isread = False
    text = "A/I: WINGS LEAK"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class A_I_WINGS_LO_PWR(CASmssg): 
    isread = False
    text = "A/I: WINGS LO PWR"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class A_I_WINGS_HI_TEMP(CASmssg): 
    isread = False
    text = "A/I: WINGS HI TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class A_I_ENG_1_2_3_MISCONFIG_ON(CASmssg): 
    isread = False
    text = "A/I ENG 1+2+3 MISCONFIG ON"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class A_I_ICE_DETECTED_1_2(CASmssg): 
    isread = False
    text = "A/I: ICE DETECTED 1+2"
    color = "W"
    park = True
    taxi = False
    cruise = True
    TO = False
    land = True

@register
class BRAKE_BOTH_SYSTEMS_FAIL(CASmssg): 
    isread = False
    text = "BRAKE: BOTH SYSTEMS FAIL"
    color = "R"
    park = False
    taxi = True
    cruise = False
    TO = False
    land = True

@register
class BRAKE_ACCU_LO_PRESS(CASmssg): 
    isread = False
    text = "BRAKE: ACCU LO PRESS"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class BRAKE_ANTISKID_FAIL(CASmssg): 
    isread = False
    text = "BRAKE: ANTISKID FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class BRAKE_BOTH_SYSTEMS_FAIL(CASmssg): 
    isread = False
    text = "BRAKE: BOTH SYSTEMS FAIL"
    color = "A"
    park = True
    taxi = False
    cruise = True
    TO = False
    land = False

@register
class BRAKE_LH_SEAT_PEDALS_FAIL(CASmssg): 
    isread = False
    text = "BRAKE: LH SEAT PEDALS FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class BRAKE_RH_SEAT_PEDALS_FAIL(CASmssg): 
    isread = False
    text = "BRAKE: RH SEAT PEDALS FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class BRAKE_ONE_SYSTEM_FAIL(CASmssg): 
    isread = False
    text = "BRAKE: ONE SYSTEM FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class BRAKE_RESIDUAL_PRESS(CASmssg): 
    isread = False
    text = "BRAKE: RESIDUAL PRESS"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class GEAR_DOOR_NOT_CLOSED(CASmssg): 
    isread = False
    text = "GEAR: DOOR NOT CLOSED"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class GEAR_EXTEND_FAULT(CASmssg): 
    isread = False
    text = "GEAR: EXTEND FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class GEAR_SYSTEM_FAULT(CASmssg): 
    isread = False
    text = "GEAR: SYSTEM FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class NWS_AUTHORITY_DEGRADED(CASmssg): 
    isread = False
    text = "NWS: AUTHORITY DEGRADED"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class NWS_FAIL(CASmssg): 
    isread = False
    text = "NWS: FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class TIRE_LO_PRESS(CASmssg): 
    isread = False
    text = "TIRE: LO PRESS"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class CONF_GEAR_NOT_UP(CASmssg): 
    isread = False
    text = "CONF: GEAR NOT UP"
    color = "W"
    park = False
    taxi = False
    cruise = True
    TO = True
    land = False

@register
class LDG_CONF_GEAR_NOT_DOWN(CASmssg): 
    isread = False
    text = "LDG CONF: GEAR NOT DOWN"
    color = "W"
    park = False
    taxi = False
    cruise = True
    TO = False
    land = True

@register
class NWS_OFF(CASmssg): 
    isread = False
    text = "NWS: OFF"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class PARK_BRAKE_ON(CASmssg): 
    isread = False
    text = "PARK BRAKE ON"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ADS_1_2_3_4_FAIL(CASmssg): 
    isread = False
    text = "ADS: 1+2+3+4 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ADS_1_2_3_4_NO_SLIP_COMP(CASmssg): 
    isread = False
    text = "ADS: 1+2+3+4 NO SLIP COMP"
    color = "A"
    park = False
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ADS_X_X_X_PROBE_HEAT_OFF(CASmssg): 
    isread = False
    text = "ADS: X+X+X PROBE HEAT OFF"
    color = "A"
    park = False
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ADS_X_X_X_PROBE_HEAT_FAIL(CASmssg): 
    isread = False
    text = "ADS: X+X+X PROBE HEAT FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ADS_ALL_PROBE_HEAT_OFF(CASmssg): 
    isread = False
    text = "ADS: ALL PROBE HEAT OFF"
    color = "A"
    park = False
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class OXY_PAX_SUPPLY_FAIL(CASmssg): 
    isread = False
    text = "OXY: PAX SUPPLY FAIL"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class OXY_LO_QTY(CASmssg): 
    isread = False
    text = "OXY: LO QTY"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class OXY_LH_MASK_NORMAL_FAIL(CASmssg): 
    isread = False
    text = "OXY: LH MASK NORMAL FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class OXY_RH_MASK_NORMAL_FAIL(CASmssg): 
    isread = False
    text = "OXY: RH MASK NORMAL FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class OXY_3RD_MASK_NORMAL_FAIL(CASmssg): 
    isread = False
    text = "OXY: 3RD MASK NORMAL FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class OXY_PAX_SUPPLY_FAIL(CASmssg): 
    isread = False
    text = "OXY: PAX SUPPLY FAIL"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class BLEED_1_OVHT(CASmssg): 
    isread = False
    text = "08 BLEED: 1 OVHT"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class BLEED_2_OVHT(CASmssg): 
    isread = False
    text = "09 BLEED: 2 OVHT"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class BLEED_3_OVHT(CASmssg): 
    isread = False
    text = "10 BLEED: 3 OVHT"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class BLEED_1_2_OVHT(CASmssg): 
    isread = False
    text = "11 BLEED: 1+2 OVHT"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class BLEED_1_3_OVHT(CASmssg): 
    isread = False
    text = "12 BLEED: 1+3 OVHT"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class BLEED_2_3_OVHT(CASmssg): 
    isread = False
    text = "13 BLEED: 2+3 OVHT"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class BLEED_1_2_3_OVHT(CASmssg): 
    isread = False
    text = "14 BLEED: 1+2+3 OVHT"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class BLEED_APU_FAULT(CASmssg): 
    isread = False
    text = "BLEED: APU FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class BLEED_1_2_3_FAIL(CASmssg): 
    isread = False
    text = "BLEED: 1+2+3 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class BLEED_HP_1_2_3_FAIL(CASmssg): 
    isread = False
    text = "BLEED: HP 1+2+3 FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class BLEED_XBLEED_FAULT(CASmssg): 
    isread = False
    text = "BLEED: XBLEED FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class BLEED_PYLON_1_3_HI_TEMP(CASmssg): 
    isread = False
    text = "BLEED: PYLON 1+3 HI TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class BLEED_PYLON_1_3_MONIT_FAIL(CASmssg): 
    isread = False
    text = "BLEED PYLON 1+3 MONIT FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class BLEED_1_2_3_HI_TEMP(CASmssg): 
    isread = False
    text = "BLEED: 1+2+3 HI TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class BLEED_1_2_3_LO_TEMP(CASmssg): 
    isread = False
    text = "BLEED: 1+2+3 LO TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class BLEED_LEAK(CASmssg): 
    isread = False
    text = "BLEED: LEAK"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class WATER_AFT_HEATER_HI_TEMP(CASmssg): 
    isread = False
    text = "WATER: AFT HEATER HI TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class WATER_FWD_HEATER_HI_TEMP(CASmssg): 
    isread = False
    text = "WATER: FWD HEATER HI TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class WATER_TANK_DRAIN_OPEN(CASmssg): 
    isread = False
    text = "WATER TANK DRAIN OPEN"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class APU_AUTO_SHUTDOWN(CASmssg): 
    isread = False
    text = "APU: AUTO SHUTDOWN"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class APU_BLEED_FAIL(CASmssg): 
    isread = False
    text = "APU: BLEED FAIL"
    color = "A"
    park = True
    taxi = False
    cruise = False
    TO = False
    land = False

@register
class DOOR_PAX___BAG(CASmssg): 
    isread = False
    text = "18 DOOR: PAX + BAG"
    color = "R"
    park = False
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ENG_2_DUCT_DOOR_OPEN(CASmssg): 
    isread = False
    text = "50 ENG 2 DUCT DOOR OPEN"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class DOOR_BAG_ACCESS_OPEN(CASmssg): 
    isread = False
    text = "DOOR: BAG ACCESS OPEN"
    color = "A"
    park = False
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class DOOR_GPU_NOT_CLOSED(CASmssg): 
    isread = False
    text = "DOOR: GPU NOT CLOSED"
    color = "A"
    park = False
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class DOOR_FWD_SERV_NOT_CLOSED(CASmssg): 
    isread = False
    text = "DOOR: FWD SERV NOT CLOSED"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class DOOR_REAR_COMP_NOT_CLOSED(CASmssg): 
    isread = False
    text = "DOOR: REAR COMP NOT CLOSED"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class DOOR_BAG_NOT_SECURED(CASmssg): 
    isread = False
    text = "DOOR: BAG NOT SECURED"
    color = "A"
    park = False
    taxi = False
    cruise = True
    TO = True
    land = True

@register
class DOOR_BAG_SENS_FAIL(CASmssg): 
    isread = False
    text = "DOOR: BAG SENS FAIL"
    color = "A"
    park = True
    taxi = False
    cruise = False
    TO = False
    land = False

@register
class DOOR_EMERG_NOT_SECURED(CASmssg): 
    isread = False
    text = "DOOR: EMERG NOT SECURED"
    color = "A"
    park = True
    taxi = False
    cruise = False
    TO = False
    land = False

@register
class DOOR_PAX_NOT_SECURED(CASmssg): 
    isread = False
    text = "DOOR: PAX NOT SECURED"
    color = "A"
    park = False
    taxi = False
    cruise = True
    TO = True
    land = True

@register
class DOOR_PAX_SENS_FAIL(CASmssg): 
    isread = False
    text = "DOOR: PAX SENS FAIL"
    color = "A"
    park = True
    taxi = False
    cruise = False
    TO = False
    land = False

@register
class DOOR_WATER_FEED_NOT_CLOSED(CASmssg): 
    isread = False
    text = "DOOR: WATER FEED NOT CLOSED"
    color = "A"
    park = False
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class CABIN_DOOR_NOT_LOCKED_OPEN(CASmssg): 
    isread = False
    text = "CABIN DOOR NOT LOCKED OPEN"
    color = "W"
    park = False
    taxi = True
    cruise = False
    TO = True
    land = True

@register
class DOOR_GPU_NOT_CLOSED(CASmssg): 
    isread = False
    text = "DOOR: GPU NOT CLOSED"
    color = "W"
    park = True
    taxi = False
    cruise = False
    TO = True
    land = True

@register
class DOOR_PAX_BAG_NOT_SECURED(CASmssg): 
    isread = False
    text = "DOOR PAX + BAG NOT SECURED"
    color = "W"
    park = True
    taxi = False
    cruise = False
    TO = True
    land = True

@register
class DOOR_WATER_FEED_NOT_CLOSED(CASmssg): 
    isread = False
    text = "DOOR: WATER FEED NOT CLOSED"
    color = "W"
    park = True
    taxi = False
    cruise = False
    TO = True
    land = True

@register
class WSHIELDS_ALL_FAIL(CASmssg): 
    isread = False
    text = "WSHIELDS ALL FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class WSHIELD_B_U_TEST_FAIL(CASmssg): 
    isread = False
    text = "WSHIELD B/U TEST FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class WSHIELD_LH_B_U_FAIL(CASmssg): 
    isread = False
    text = "WSHIELD LH B/U FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class WSHIELD_LH_HEAT_FAULT(CASmssg): 
    isread = False
    text = "WSHIELD: LH HEAT FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class WSHIELD_LH_TEST_FAIL(CASmssg): 
    isread = False
    text = "WSHIELD LH TEST FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class WSHIELD_RH_B_U_FAIL(CASmssg): 
    isread = False
    text = "WSHIELD RH B/U FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class WSHIELD_RH_HEAT_FAULT(CASmssg): 
    isread = False
    text = "WSHIELD: RH HEAT FAULT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = True

@register
class WSHIELD_RH_TEST_FAIL(CASmssg): 
    isread = False
    text = "WSHIELD RH TEST FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class WSHIELD_TEST_IN_PROGRESS(CASmssg): 
    isread = False
    text = "WSHIELD TEST IN PROGRESS"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ENG_1_2_3_FAIL(CASmssg): 
    isread = False
    text = "52 ENG 1+2+3: FAIL"
    color = "R"
    park = False
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ENG_ALL_OUT(CASmssg): 
    isread = False
    text = "46 ENG: ALL OUT"
    color = "R"
    park = False
    taxi = False
    cruise = True
    TO = True
    land = True

@register
class ENG_1_OIL_TOO_LO_PRESS(CASmssg): 
    isread = False
    text = "54 ENG 1 OIL TOO LO PRESS"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ENG_2_OIL_TOO_LO_PRESS(CASmssg): 
    isread = False
    text = "55 ENG 2 OIL TOO LO PRESS"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ENG_3_OIL_TOO_LO_PRESS(CASmssg): 
    isread = False
    text = "56 ENG 3 OIL TOO LO PRESS"
    color = "R"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ENG_OUT(CASmssg): 
    isread = False
    text = "ENG #: OUT"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class ENG_1_2_3_AUTO_SHUTDOWN(CASmssg): 
    isread = False
    text = "ENG 1+2+3: AUTO SHUTDOWN"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class ENG_1_2_3_FUEL_FILT_BYPASS(CASmssg): 
    isread = False
    text = "ENG 1+2+3: FUEL FILT BYPASS"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ENG_1_2_3_FUEL_FILT_IMPEND(CASmssg): 
    isread = False
    text = "ENG 1+2+3 FUEL FILT IMPEND"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class ENG_1_2_3_GO_IF_DISPATCH(CASmssg): 
    isread = False
    text = "ENG 1+2+3: GO IF DISPATCH"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class ENG_1_2_3_HI_VIBRATION(CASmssg): 
    isread = False
    text = "ENG 1+2+3: HI VIBRATION"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class ENG_1_2_3_LONG_DISPATCH(CASmssg): 
    isread = False
    text = "ENG 1+2+3: LONG DISPATCH"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class ENG_1_2_3_NO_DISPATCH(CASmssg): 
    isread = False
    text = "ENG 1+2+3: NO DISPATCH"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class ENG_1_2_3_OIL_PARAM_ABNORM(CASmssg): 
    isread = False
    text = "ENG 1+2+3 OIL PARAM ABNORM"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class ENG_1_2_3_PARAM_EXCEED(CASmssg): 
    isread = False
    text = "ENG 1+2+3 PARAM EXCEED"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class ENG_1_2_3_SHORT_DISPATCH(CASmssg): 
    isread = False
    text = "ENG 1+2+3: SHORT DISPATCH"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class ENG_1_2_3_START_CMD_INOP(CASmssg): 
    isread = False
    text = "ENG 1+2+3: START CMD INOP"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class ENG_1_2_3_STARTER_FAIL(CASmssg): 
    isread = False
    text = "ENG 1+2+3: STARTER FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class ENG_1_2_3_STARTER_HI_TEMP(CASmssg): 
    isread = False
    text = "ENG 1+2+3 STARTER HI TEMP"
    color = "A"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False

@register
class ENG_1_2_3_SURGE_PROT_FAIL(CASmssg): 
    isread = False
    text = "ENG 1+2+3: SURGE PROT FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class ENG_1_2_3_THROTTLE_INOP(CASmssg): 
    isread = False
    text = "ENG 1+2+3: THROTTLE INOP"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class ENG_MULTIPLE_START(CASmssg): 
    isread = False
    text = "ENG: MULTIPLE START"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class THRUST_REVERSER_FAIL(CASmssg): 
    isread = False
    text = "THRUST REVERSER: FAIL"
    color = "A"
    park = True
    taxi = True
    cruise = True
    TO = True
    land = True

@register
class NG_1_2_3_FUEL_FILT_IMPEND(CASmssg): 
    isread = False
    text = "NG 1+2+3 FUEL FILT IMPEND"
    color = "W"
    park = True
    taxi = True
    cruise = True
    TO = False
    land = False

@register
class THRUST_REVERSER_INHIBITED(CASmssg): 
    isread = False
    text = "THRUST REVERSER INHIBITED"
    color = "W"
    park = True
    taxi = True
    cruise = False
    TO = False
    land = False
