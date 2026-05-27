import datetime
import streamlit as st
import swisseph as swe

# --- 1. CONFIG & DATA ---
st.set_page_config(
    page_title="ఆచార్య అడ్వాన్స్డ్ ఆస్ట్రో యాప్", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# రాశులు, నక్షత్రాలు మరియు గ్రహాల వివరాలు
RASHIS = ["మేషం", "వృషభం", "మిథునం", "కర్కాటకం", "సింహం", "కన్య", "తుల", "వృశ్చికం", "ధనుస్సు", "మకరం", "కుంభం", "మీనం"]
NAKSHATRAS = ["అశ్విని", "భరణి", "కృత్తిక", "రోహిణి", "మృగశిర", "ఆరుద్ర", "పునర్వసు", "పుష్యమి", "ఆశ్లేష", "మఖ", "పూర ఫాల్గుణి", "ఉత్తర ఫాల్గుణి", "హస్త", "చిత్ర", "స్వాతి", "విశాఖ", "అనూరాధ", "జ్యేష్ఠ", "మూల", "పూర్వాషాఢ", "ఉత్తరాషాఢ", "శ్రవణం", "ధనిష్ఠ", "శతభిషం", "పూర్వాభాద్ర", "ఉత్తరాభాద్ర", "రేవతి"]
GRAHAS = ["సూర్యుడు", "చంద్రుడు", "కుజుడు", "రాహువు", "గురువు", "శని", "బుధుడు", "కేతువు", "శుక్రుడు"]
DASHA_YEARS = [6, 10, 7, 18, 16, 19, 17, 7, 20]

# --- 2. CALCULATIONS (ఆస్ట్రో గణనలు) ---
def calculate_horoscope(year, month, day, hour, minute, lat, lon):
    # స్థానిక సమయాన్ని UTC లోకి మార్చడం (IST = UTC + 5:30)
    local_time = datetime.datetime(year, month, day, hour, minute)
    utc_time = local_time - datetime.timedelta(hours=5, minutes=30)
    
    # జూలియన్ డే (Julian Day) గణన
    jd = swe.julday(utc_time.year, utc_time.month, utc_time.day, utc_time.hour + utc_time.minute/60.0)
    
    # లహిరి అయనాంశ సెట్ చేయడం (Sidereal/Nirayana)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    # లగ్న గణన
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)
    lagna_idx = int(ascmc[0] / 30) % 12
    
    # గ్రహాల స్థానాల గణన
    tags = {
        "సూర్యుడు": swe.SUN, "చంద్రుడు": swe.MOON, "బుధుడు": swe.MERCURY, 
        "శుక్రుడు": swe.VENUS, "కుజుడు": swe.MARS, "గురువు": swe.JUPITER, 
        "శని": swe.SATURN, "రాహువు": swe.MEAN_NODE
    }
    positions = {}
    for p, t in tags.items():
        res, ret = swe.calc_ut(jd, t, swe.FLG_SIDEREAL)
        positions[p] = res[0]
        
    # కేతువు ఎప్పుడూ రాహువుకి 180 డిగ్రీల ఎదురుగా ఉంటాడు
    positions["కేతువు"] = (positions["రాహువు"] + 180) % 360
    
    # చార్ట్ లోపల గ్రహాలను అమర్చడం
    chart = {i: [] for i in range(12)}
    chart[lagna_idx].append("లగ్నం")
    for p, deg in positions.items():
        chart[int(deg / 30) % 12].append(p)
        
    # రాశి మరియు నక్షత్ర పాదాల గణన (చంద్రుని స్థానాన్ని బట్టి)
    moon_deg = positions["చంద్రుడు"]
    rashi_idx = int(moon_deg / 30) % 12
    nak_pos = moon_deg / (360 / 27)
    nak_idx = int(nak_pos) % 27
    pada = int((nak_pos - nak_idx) * 4) + 1
    
    # వింశోత్తరి దశా గణనలు
    start_idx = nak_idx % 9
    rem_years = (1.0 - (nak_pos - nak_idx)) * DASHA_YEARS[start_idx]
    
    curr = local_time + datetime.timedelta(days=int(rem_years * 365.25))
    timeline = [{"మహాదశ (Dasha)": GRAHAS[start_idx], "ముగింపు తేదీ (End Date)": curr.strftime("%d-%m-%Y")}]
    
    idx = start_idx
    for _ in range(5): # రాబోయే 5 దశల కాలక్రమం
        idx = (idx + 1) % 9
        curr += datetime.timedelta(days=int(DASHA_YEARS[idx] * 365.25))
        timeline.append({"మహాదశ (Dasha)": GRAHAS[idx], "ముగింపు తేదీ (End Date)": curr.strftime("%d-%m-%Y")})
        
    return {
        "lagna": RASHIS[lagna_idx], 
        "rashi": RASHIS[rashi_idx], 
        "nak": NAKSHATRAS[nak_idx], 
        "pada": pada, 
        "chart": chart, 
        "dasha": timeline
    }

# --- 3. USER INTERFACE (యూజర్ ఇంటర్‌ఫేస్) ---
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🕉️ ఆచార్య అడ్వాన్స్డ్ ఆస్ట్రో యాప్</h1>", unsafe_html=True)
st.markdown("<p style='text-align: center;'>మీ ఖచ్చితమైన జనన వివరాలను నమోదు చేసి జాతక చక్రం మరియు దశా ఫలాలను తెలుసుకోండి.</p>", unsafe_html=True)
st.hr()

# ఇన్‌పుట్ ఫారమ్
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("👤 పేరు (Name):", value="రాము")
    dob = st.date_input("📅 పుట్టిన తేదీ (DOB):", datetime.date(1995, 8, 15))
    tob = st.time_input("⏰ పుట్టిన సమయం (TOB):", datetime.time(10, 30))
with col2:
    place = st.text_input("📍 పుట్టిన ఊరు (Place):", value="హైదరాబాద్")
    lat = st.number_input("🌐 అక్షాంశం (Latitude):", value=17.3850, format="%.4f")
    lon = st.number_input("🌐 రేఖాంశం (Longitude):", value=78.4867, format="%.4f")

st.write("")
calculate_btn = st.button("🔮 జాతక చక్రం గణించు", type="primary", use_container_width=True)

# లెక్కలు మరియు ఫలితాలు
if calculate_btn:
    if name and place:
        try:
            with st.spinner("⏳ గ్రహ స్థానాలను లెక్కిస్తున్నాము... దయచేసి వేచి ఉండండి..."):
                res = calculate_horoscope(dob.year, dob.month, dob.day, tob.hour, tob.minute, lat, lon)
            
            st.success("🎉 జాతక చక్ర గణన విజయవంతంగా పూర్తయింది!")
            
            # ట్యాబ్స్ లేఅవుట్
            t1, t2, t3 = st.tabs(["✨ జనన వివరాలు", "📊 జాతక చక్రం (Kundali)", "⏳ వింశోత్తరి దశలు"])
            
            with t1:
                st.subheader("📋 ముఖ్యమైన వివరాలు")
                st.info(f"👤 **పేరు:** {name} | 📍 **స్థలం:** {place}")
                
                info_col1, info_col2, info_col3 = st.columns(3)
                info_col1.metric(label="లగ్నం", value=res['lagna'])
                info_col2.metric(label="రాశి", value=res['rashi'])
                info_col3.metric(label="నక్షత్రం", value=f"{res['nak']} ({res['pada']} వ పాదం)")
            
            with t2:
                st.subheader("🗺️ దక్షిణ భారత పద్ధతి జాతక చక్రం")
                
                # సౌత్ ఇండియన్ స్టైల్ 4x4 గ్రిడ్ మ్యాపింగ్
                grid_map = [
                    [11, 0, 1, 2],   # మీనం, మేషం, వృషభం, మిథునం
                    [10, -1, -1, 3], # కుంభం, ఖాళీ, ఖాళీ, కర్కాటకం
                    [9, -1, -1, 4],  # మకరం, ఖాళీ, ఖాళీ, సింహం
                    [8, 7, 6, 5]     # ధనుస్సు, వృశ్చికం, తుల, కన్య
                ]
                
                # కుండలి గ్రిడ్ డిజైన్
                for row in grid_map:
                    cols = st.columns(4)
                    for col_idx, rashi_idx in enumerate(row):
                        with cols[col_idx]:
                            if rashi_idx != -1:
                                planets_list = res['chart'][rashi_idx]
                                planets_html = "<br>".join([f"• {p}" for p in planets_list]) if planets_list else "<span style='color:#aaa;'>ఖాళీ</span>"
                                
                                st.markdown(
                                    f"""
                                    <div style="border: 2px solid #ff4b4b; border-radius: 8px; padding: 12px; text-align: center; background-color: #fff9f9; min-height: 120px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
                                        <b style="color: #ff4b4b; font-size: 16px;">{RASHIS[rashi_idx]}</b>
                                        <hr style="margin: 6px 0; border-top: 1px solid #ffe0e0;">
                                        <div style="color: #2c3e50; font-size: 13px; font-weight: bold; text-align: left; padding-left: 10px;">
                                            {planets_html}
                                        </div>
                                    </div>
                                    """, 
                                    unsafe_html=True
                                )
                            else:
                                # మధ్యలో ఉండే ఖాళీ బాక్సుల డిజైన్
                                st.markdown(
                                    """
                                    <div style="min-height: 120px; display: flex; align-items: center; justify-content: center;">
                                    </div>
                                    """, 
                                    unsafe_html=True
                                )
                    st.write("") # రోల మధ్య స్పేస్ కోసం
                    
            with t3:
                st.subheader("⏳ ప్రస్తుత మరియు రాబోయే మహాదశలు")
                st.dataframe(res['dasha'], use_container_width=True, hide_index=True)
                st.caption("గమనిక: పైన పేర్కొన్న తేదీలతో ఆయా మహాదశలు ముగుస్తాయి.")
                
        except Exception as e:
            st.error(f"❌ గణన చేయడంలో లోపం తలెత్తింది. దయచేసి అక్షాంశ, రేఖాంశాల వాల్యూస్ సరిగ్గా ఉన్నాయో లేదో చూసుకోండి. Error: {e}")
    else:
        st.warning("⚠️ దయచేసి మీ పేరు మరియు పుట్టిన ఊరు వివరాలను నమోదు చేయండి.")
