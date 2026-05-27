import datetime
import streamlit as st
import swisseph as swe

# --- 1. CONFIG ---
st.set_page_config(page_title="Acharya Astro", layout="wide")

RASHIS = ["మేషం", "వృషభం", "మిథునం", "కర్కాటకం", "సింహం", "కన్య", "తుల", "వృశ్చికం", "ధనుస్సు", "మకరం", "కుంభం", "మీనం"]
NAKSHATRAS = ["అశ్విని", "భరణి", "కృత్తిక", "రోహిణి", "మృగశిర", "ఆరుద్ర", "పునర్వసు", "పుష్యమి", "ఆశ్లేష", "మఖ", "పూర ఫాల్గుణి", "ఉత్తర ఫాల్గుణి", "హస్త", "చిత్ర", "స్వాతి", "విశాఖ", "అనూరాధ", "జ్యేష్ఠ", "మూల", "పూర్వాషాఢ", "ఉత్తరాషాఢ", "శ్రవణం", "ధనిష్ఠ", "శతభిషం", "పూర్వాభాద్ర", "ఉత్తరాభాద్ర", "రేవతి"]
GRAHAS = ["సూర్యుడు", "చంద్రుడు", "కుజుడు", "రాహువు", "గురువు", "శని", "బుధుడు", "కేతువు", "శుక్రుడు"]
DASHA_YEARS = [6, 10, 7, 18, 16, 19, 17, 7, 20]

# --- 2. CALCULATIONS ---
def calculate_horoscope(year, month, day, hour, minute, lat, lon):
    local_time = datetime.datetime(year, month, day, hour, minute)
    utc_time = local_time - datetime.timedelta(hours=5, minutes=30)
    jd = swe.julday(utc_time.year, utc_time.month, utc_time.day, utc_time.hour + utc_time.minute/60.0)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)
    lagna_idx = int(ascmc[0] / 30) % 12
    
    tags = {"సూర్యుడు": swe.SUN, "చంద్రుడు": swe.MOON, "బుధుడు": swe.MERCURY, "శుక్రుడు": swe.VENUS, "కుజుడు": swe.MARS, "గురువు": swe.JUPITER, "శని": swe.SATURN, "రాహువు": swe.MEAN_NODE}
    positions = {}
    for p, t in tags.items():
        res, ret = swe.calc_ut(jd, t, swe.FLG_SIDEREAL)
        positions[p] = res[0]
    positions["కేతువు"] = (positions["రాహువు"] + 180) % 360
    
    chart = {i: [] for i in range(12)}
    chart[lagna_idx].append("లగ్నం")
    for p, deg in positions.items():
        chart[int(deg / 30) % 12].append(p)
        
    moon_deg = positions["చంద్రుడు"]
    rashi_idx = int(moon_deg / 30) % 12
    nak_pos = moon_deg / (360 / 27)
    nak_idx = int(nak_pos) % 27
    pada = int((nak_pos - nak_idx) * 4) + 1
    
    start_idx = nak_idx % 9
    rem_years = (1.0 - (nak_pos - nak_idx)) * DASHA_YEARS[start_idx]
    
    curr = local_time + datetime.timedelta(days=int(rem_years * 365.25))
    timeline = [{"Dasha": GRAHAS[start_idx], "End Date": curr.strftime("%d-%m-%Y")}]
    
    idx = start_idx
    for _ in range(4):
        idx = (idx + 1) % 9
        curr += datetime.timedelta(days=int(DASHA_YEARS[idx] * 365.25))
        timeline.append({"Dasha": GRAHAS[idx], "End Date": curr.strftime("%d-%m-%Y")})
        
    return {"lagna": RASHIS
