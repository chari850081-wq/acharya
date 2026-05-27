import datetime
import streamlit as st
import swisseph as swe

# --- 1. CONFIG ---
st.set_page_config(page_title="Acharya Astro", layout="wide")

RASHIS = ["Mesham", "Vrishabham", "Mithunam", "Karkatakam", "Simham", "Kanya", "Thula", "Vrishchikam", "Dhanussu", "Makaram", "Kumbham", "Meenam"]
NAKSHATRAS = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Arudra", "Punarvasu", "Pushyami", "Aslesha", "Makha", "Pubba", "Uttara", "Hastha", "Chitra", "Swathi", "Visakha", "Anuradha", "Jyeshta", "Moola", "Poorvashadha", "Uttarashadha", "Shravanam", "Dhanishta", "Sathabhisham", "Poorvabhadra", "Uttrabhadra", "Revathi"]
GRAHAS = ["Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus"]
DASHA_YEARS = [6, 10, 7, 18, 16, 19, 17, 7, 20]

# --- 2. CALCULATIONS ---
def calculate_horoscope(year, month, day, hour, minute, lat, lon):
    local_time = datetime.datetime(year, month, day, hour, minute)
    utc_time = local_time - datetime.timedelta(hours=5, minutes=30)
    jd = swe.julday(utc_time.year, utc_time.month, utc_time.day, utc_time.hour + utc_time.minute/60.0)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)
    lagna_idx = int(ascmc[0] / 30) % 12
    
    tags = {"Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY, "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN, "Rahu": swe.MEAN_NODE}
    positions = {}
    for p, t in tags.items():
        res, ret = swe.calc_ut(jd, t, swe.FLG_SIDEREAL)
        positions[p] = res[0]
    positions["Ketu"] = (positions["Rahu"] + 180) % 360
    
    chart = {i: [] for i in range(12)}
    chart[lagna_idx].append("Lagna")
    for p, deg in positions.items():
        chart[int(deg / 30) % 12].append(p)
        
    moon_deg = positions["Moon"]
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
        
    return {"lagna": RASHIS[lagna_idx], "rashi": RASHIS[rashi_idx], "nak": NAKSHATRAS[nak_idx], "pada": pada, "chart": chart, "dasha": timeline}

# --- 3. UI ---
st.title("🕉️ ఆచార్య అడ్వాన్స్డ్ ఆస్ట్రో యాప్")
st.write("ఇక్కడ మీ పూర్తి జాతక చక్రం మరియు వింశోత్తరి దశలను తెలుసుకోవచ్చు.")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("👤 పేరు (Name):")
    dob = st.date_input("📅 పుట్టిన తేదీ:", datetime.date(
