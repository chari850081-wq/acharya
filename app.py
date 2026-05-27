import datetime
import streamlit as st
import swisseph as swe
from geopy.geocoders import Nominatim
from PIL import Image

# --- 1. CONFIG & DATA ---
st.set_page_config(
    page_title="ఆచార్య అడ్వాన్స్డ్ ఆల్ ఇన్ వన్ ఆస్ట్రో", 
    layout="wide",
    initial_sidebar_state="expanded"
)

RASHIS = ["మేషం", "వృషభం", "మిథునం", "కర్కాటకం", "సింహం", "కన్య", "తుల", "వృశ్చికం", "ధనుస్సు", "మకరం", "కుంభం", "మీనం"]
NAKSHATRAS = ["అశ్విని", "భరణి", "కృత్తిక", "రోహిణి", "మృగశిర", "ఆరుద్ర", "పునర్వసు", "పుష్యమి", "ఆశ్లేష", "మఖ", "పూర ఫాల్గుణి", "ఉత్తర ఫాల్గుణి", "హస్త", "చిత్ర", "స్వాతి", "విశాఖ", "అనూరాధ", "జ్యేష్ఠ", "మూల", "పూర్వాషాఢ", "ఉత్తరాషాఢ", "శ్రవణం", "ధనిష్ఠ", "శతభిషం", "పూర్వాభాద్ర", "ఉత్తరాభాద్ర", "రేవతి"]
GRAHAS = ["సూర్యుడు", "చంద్రుడు", "కుజుడు", "రాహువు", "గురువు", "శని", "బుధుడు", "కేతువు", "శుక్రుడు"]
DASHA_YEARS = [6, 10, 7, 18, 16, 19, 17, 7, 20]
TOTAL_DASHA_CYCLE = 120

# 5 స్థాయిల వింశోత్తరి దశల విభజన ఫంక్షన్
def get_detailed_dasha_hierarchy(birth_time, start_idx, rem_years):
    total_past_years = DASHA_YEARS[start_idx] - rem_years
    base_time = birth_time - datetime.timedelta(days=int(total_past_years * 365.25))
    
    current_time = base_time
    dasha_data = []
    
    idx1 = start_idx
    for _ in range(9):
        md_years = DASHA_YEARS[idx1]
        md_end = current_time + datetime.timedelta(days=int(md_years * 365.25))
        
        idx2 = idx1
        ad_start = current_time
        for _ in range(9):
            ad_years = md_years * (DASHA_YEARS[idx2] / TOTAL_DASHA_CYCLE)
            ad_end = ad_start + datetime.timedelta(days=int(ad_years * 365.25))
            
            idx3 = idx2
            pd_start = ad_start
            for _ in range(9):
                pd_years = ad_years * (DASHA_YEARS[idx3] / TOTAL_DASHA_CYCLE)
                pd_end = pd_start + datetime.timedelta(days=int(pd_years * 365.25))
                
                idx4 = idx3
                sd_start = pd_start
                for _ in range(9):
                    sd_years = pd_years * (DASHA_YEARS[idx4] / TOTAL_DASHA_CYCLE)
                    sd_end = sd_start + datetime.timedelta(days=int(sd_years * 365.25))
                    
                    idx5 = idx4
                    prd_start = sd_start
                    for _ in range(9):
                        prd_years = sd_years * (DASHA_YEARS[idx5] / TOTAL_DASHA_CYCLE)
                        prd_end = prd_start + datetime.timedelta(days=int(prd_years * 365.25))
                        
                        now = datetime.datetime.now()
                        if prd_start <= now <= prd_end:
                            dasha_data.append({
                                "మహాదశ (1)": GRAHAS[idx1],
                                "అంతర్దశ (2)": GRAHAS[idx2],
                                "ప్రత్యంతర్దశ/విదర్స్ (3)": GRAHAS[idx3],
                                "సూక్ష్మ దశ (4)": GRAHAS[idx4],
                                "సుసూక్ష్మ/ప్రాణ దశ (5)": GRAHAS[idx5],
                                "ప్రారంభం": prd_start.strftime("%d-%m-%Y %H:%M"),
                                "ముగింపు": prd_end.strftime("%d-%m-%Y %H:%M")
                            })
                        
                        prd_start = prd_end
                        idx5 = (idx5 + 1) % 9
                    sd_start = sd_end
                    idx4 = (idx4 + 1) % 9
                pd_start = pd_end
                idx3 = (idx3 + 1) % 9
            ad_start = ad_end
            idx2 = (idx2 + 1) % 9
        current_time = md_end
        idx1 = (idx1 + 1) % 9
        
    return dasha_data

# నవాంశ చక్రం (D9) గణన ఫంక్షన్
def calculate_navamsha(planet_total_deg):
    rashi_idx = int(planet_total_deg / 30) % 12
    deg_in_rashi = planet_total_deg % 30
    
    # నవాంశ లో ఏ విభాగం (1-9)
    nav_part = int(deg_in_rashi / (30 / 9)) # 0 to 8
    
    # ఎలిమెంట్ ప్రకారం స్టార్టింగ్ పాయింట్
    if rashi_idx in [0, 4, 8]: # అగ్ని తత్వ రాశులు (మేష, సింహ, ధనుస్సు) -> మేషం నుండి
        start_idx = 0
    elif rashi_idx in [1, 5, 9]: # భూ తత్వ రాశులు (వృషభ, కన్య, మకర) -> మకరం నుండి
        start_idx = 9
    elif rashi_idx in [2, 6, 10]: # వాయు తత్వ రాశులు (మిథున, తుల, కుంభ) -> తుల నుండి
        start_idx = 6
    else: # జల తత్వ రాశులు (కర్కాటక, వృశ్చిక, మీన) -> కర్కాటకం నుండి
        start_idx = 3
        
    nav_rashi_idx = (start_idx + nav_part) % 12
    return nav_rashi_idx

# --- 2. CALCULATIONS (ఆస్ట్రో గణనలు) ---
def calculate_horoscope(year, month, day, hour, minute, lat, lon):
    local_time = datetime.datetime(year, month, day, hour, minute)
    utc_time = local_time - datetime.timedelta(hours=5, minutes=30)
    
    jd = swe.julday(utc_time.year, utc_time.month, utc_time.day, utc_time.hour + utc_time.minute/60.0)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)
    lagna_total_deg = ascmc[0]
    lagna_idx = int(lagna_total_deg / 30) % 12
    
    tags = {
        "సూర్యుడు": swe.SUN, "చంద్రుడు": swe.MOON, "బుధుడు": swe.MERCURY, 
        "శుక్రుడు": swe.VENUS, "కుజుడు": swe.MARS, "గురువు": swe.JUPITER, 
        "శని": swe.SATURN, "రాహువు": swe.MEAN_NODE
    }
    
    positions = {}
    planet_details = []
    rashi_chart = {i: [] for i in range(12)}
    nav_chart = {i: [] for i in range(12)}
    
    # రాశి చార్ట్ కి లగ్నం యాడ్ చేయడం
    rashi_chart[lagna_idx].append("లగ్నం")
    # నవాంశ చార్ట్ కి లగ్నం యాడ్ చేయడం
    nav_chart[calculate_navamsha(lagna_total_deg)].append("లగ్నం")
    
    for p, t in tags.items():
        res, ret = swe.calc_ut(jd, t, swe.FLG_SIDEREAL)
        deg = res[0]
        speed = res[3]
        positions[p] = deg
        
        # రాశి చక్రం అమరిక
        r_idx = int(deg / 30) % 12
        rashi_chart[r_idx].append(p)
        
        # నవాంశ చక్రం అమరిక
        n_idx = calculate_navamsha(deg)
        nav_chart[n_idx].append(p)
        
        # గ్రహ బలాబలాల వివరాలు
        gati = "🔄 వక్రం (Retro)" if speed < 0 else "➡️ మార్గి (Direct)"
        if p in ["సూర్యుడు", "చంద్రుడు"]: gati = "➡️ మార్గి"
        
        planet_details.append({
            "గ్రహం": p, "రాశి": RASHIS[r_idx], "డిగ్రీ": f"{(deg % 30):.2f}°", "నక్షత్రం": NAKSHATRAS[int(deg / (360 / 27)) % 27], "స్థితి": gati
        })
        
    positions["కేతువు"] = (positions["రాహువు"] + 180) % 360
    k_deg = positions["కేతువు"]
    rashi_chart[int(k_deg/30)%12].append("కేతువు")
    nav_chart[calculate_navamsha(k_deg)].append("కేతువు")
    planet_details.append({
        "గ్రహం": "కేతువు", "రాశి": RASHIS[int(k_deg/30)%12], "డిగ్రీ": f"{(k_deg % 30):.2f}°", "నక్షత్రం": NAKSHATRAS[int(k_deg / (360 / 27)) % 27], "స్థితి": "🔄 వక్రం"
    })
    
    moon_deg = positions["చంద్రుడు"]
    rashi_idx = int(moon_deg / 30) % 12
    nak_pos = moon_deg / (360 / 27)
    nak_idx = int(nak_pos) % 27
    pada = int((nak_pos - nak_idx) * 4) + 1
    
    start_idx = nak_idx % 9
    rem_years = (1.0 - (nak_pos - nak_idx)) * DASHA_YEARS[start_idx]
    detailed_dasha = get_detailed_dasha_hierarchy(local_time, start_idx, rem_years)
    
    return {
        "lagna": RASHIS[lagna_idx], "rashi": RASHIS[rashi_idx], "nak": NAKSHATRAS[nak_idx], "pada": pada, 
        "rashi_chart": rashi_chart, "nav_chart": nav_chart, "detailed_dasha": detailed_dasha, "planet_details": planet_details
    }

# --- 3. UI LAYOUT ---
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🕉️ ఆచార్య అడ్వాన్స్డ్ ఆల్ ఇన్ వన్ ఆస్ట్రో</h1>", unsafe_html=True)
st.markdown("<p style='text-align: center;'>రాశి (D1), నవాంశ (D9), 5 స్థాయిల దశలు మరియు గ్రహ బలాల సంపూర్ణ విశ్లేషణ.</p>", unsafe_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("📝 జనన వివరాలు")
    name = st.text_input("👤 పేరు:", value="రాము")
    dob = st.date_input("📅 తేదీ:", datetime.date(1995, 8, 15))
    tob = st.time_input("⏰ సమయం:", datetime.time(10, 30))
    place = st.text_input("📍 ఊరు (English):", value="Hyderabad")

with col2:
    st.subheader("🖼️ ఫోటో అప్‌లోడ్")
    uploaded_file = st.file_uploader("చిత్రం అప్‌లోడ్ చేయండి:", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(Image.open(uploaded_file), width=250)

if st.button("🔮 జాతక ఫలితాలను గణించు", type="primary", use_container_width=True):
    try:
        with st.spinner("🔍 లొకేషన్ సర్చ్ & గ్రహాల నవాంశ గణిస్తున్నాము..."):
            geolocator = Nominatim(user_agent="acharya_full_astro")
            loc = geolocator.geocode(f"{place}, India")
            
            if not loc:
                st.error("ఊరి పేరు దొరకలేదు. దయచేసి స్పెల్లింగ్ సరిచూడండి.")
            else:
                res = calculate_horoscope(dob.year, dob.month, dob.day, tob.hour, tob.minute, loc.latitude, loc.longitude)
                st.success(f"📍 {place} ({loc.latitude:.2f} N, {loc.longitude:.2f} E) ఆధారంగా ఫలితాలు:")
                
                t1, t2, t3, t4 = st.tabs(["⏳ 5 స్థాయిల దశలు", "📊 చక్రాలు (D1 & D9)", "🪐 గ్రహ బలాలు", "📋 వివరాలు"])
                
                with t1:
                    st.subheader("⏱️ ప్రస్తుతం నడుస్తున్న పంచ-దశలు")
                    st.dataframe(res['detailed_dasha'], use_container_width=True, hide_index=True)
                
                with t2:
                    col_d1, col_d9 = st.columns(2)
                    grid_map = [[11, 0, 1, 2], [10, -1, -1, 3], [9, -1, -1, 4], [8, 7, 6, 5]]
                    
                    def draw_chart(title, chart_data):
                        st.markdown(f"<h3 style='text-align:center;'>{title}</h3>", unsafe_html=True)
                        for row in grid_map:
                            cols = st.columns(4)
                            for c_idx, r_idx in enumerate(row):
                                with cols[c_idx]:
                                    if r_idx != -1:
                                        planets = "<br>".join([f"• {p}" for p in chart_data[r_idx]]) if chart_data[r_idx] else ""
                                        st.markdown(f"<div style='border:1px solid #ff4b4b; padding:5px; text-align:center; min-height:80px; background:#fff9f9;'><b style='color:#ff4b4b;'>{RASHIS[r_idx]}</b><br><small>{planets}</small></div>", unsafe_html=True)
                                    else: st.write("")
                    
                    with col_d1: draw_chart("రాశి చక్రం (D1)", res['rashi_chart'])
                    with col_d9: draw_chart("నవాంశ చక్రం (D9)", res['nav_chart'])
                
                with t3:
                    st.subheader("🪐 గ్రహాల డిగ్రీలు & వక్ర గతి")
                    st.table(res['planet_details'])
                
                with t4:
                    st.subheader("✨ ముఖ్యమైన వివరాలు")
                    st.info(f"👤 పేరు: {name} | లగ్నం: {res['lagna']} | రాశి: {res['rashi']} | నక్షత్రం: {res['nak']} ({res['pada']} వ పాదం)")

    except Exception as e:
        st.error(f"Error: {e}")
