import datetime
import streamlit as st
import swisseph as swe

# --- 1. స్థిరమైన డేటా (తెలుగు పేర్లు) ---
RASHIS = [
    "మేషం", "వృషభం", "మిథునం", "కర్కాటకం", "సింహం", "కన్య",
    "తుల", "వృశ్చికం", "ధనుస్సు", "మకరం", "కుంభం", "మీనం"
]

NAKSHATRAS = [
    "అశ్విని", "భరణి", "కృత్తిక", "రోహిణి", "మృగశిర", "ఆరుద్ర", "పునర్వసు", "పుష్యమి", "ఆశ్లేష",
    "మఖ", "పూర ఫాల్గుణి", "ఉత్తర ఫాల్గుణి", "హస్త", "చిత్ర", "స్వాతి", "విశాఖ", "అనూరాధ", "జ్యేష్ఠ",
    "మూల", "పూర్వాషాఢ", "ఉత్తరాషాఢ", "శ్రవణం", "ధనిష్ఠ", "శతభిషం", "పూర్వాభాద్ర", "ఉత్తరాభాద్ర", "రేవతి"
]

GRAHAS = ["సూర్యుడు", "చంద్రుడు", "కుజుడు", "రాహువు", "గురువు", "శని", "బుధుడు", "కేతువు", "శుక్రుడు"]
DASHA_YEARS = [6, 10, 7, 18, 16, 19, 17, 7, 20]  # వింశోత్తరి దశల సంవత్సరాలు

# --- 2. జాతక గణనల మెయిన్ ఫంక్షన్ ---
def calculate_complete_horoscope(year, month, day, hour, minute, lat, lon):
    # IST నుండి UTC కి మార్చడం
    local_time = datetime.datetime(year, month, day, hour, minute)
    utc_time = local_time - datetime.timedelta(hours=5, minutes=30)
    utc_hour = utc_time.hour + utc_time.minute / 60.0
    
    jd = swe.julday(utc_time.year, utc_time.month, utc_time.day, utc_hour)
    swe.set_sid_mode(swe.SIDM_LAHIRI)  # లాహిరి అయనాంశ
    
    # లగ్నం లెక్కింపు
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)
    lagna_deg = ascmc[0]
    lagna_rashi_idx = int(lagna_deg / 30)
    
    # గ్రహాల స్థానాలు లెక్కించడం (ఇక్కడ తప్పులన్నీ పూర్తిగా సరిచేయబడ్డాయి)
    planet_tags = {
        "సూర్యుడు": swe.SUN, 
        "చంద్రుడు": swe.MOON, 
        "బుధుడు": swe.MERCURY, 
        "
