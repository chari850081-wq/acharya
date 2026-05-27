import datetime
import streamlit as st
import swisseph as swe
# తెలుగు రాశులు మరియు నక్షత్రాల పేర్లు
RASHIS = [
    "మేషం", "వృషభం", "మిథునం", "కర్కాటకం", "సింహం", "కన్య",
    "తుల", "వృశ్చికం", "ధనుస్సు", "మకరం", "కుంభం", "మీనం"
]

NAKSHATRAS = [
    "అశ్విని", "భరణి", "కృత్తిక", "రోహిణి", "మృగశిర", "ఆరుద్ర", "పునర్వసు", "పుష్యమి", "ఆశ్లేష",
    "మఖ", "పూర ఫాల్గుణి (పుబ్బ)", "ఉత్తర ఫాల్గుణి (ఉత్తర)", "హస్త", "చిత్ర", "స్వాతి", "విశాఖ", "అనూరాధ", "జ్యేష్ఠ",
    "మూల", "పూర్వాషాఢ", "ఉత్తరాషాఢ", "శ్రవణం", "ధనిష్ఠ", "శతభిషం", "పూర్వాభాద్ర", "ఉత్తరాభాద్ర", "రేవతి"
]

def calculate_horoscope(year, month, day, hour, minute, lat, lon):
    # IST నుండి UTC కి మార్చడం (-5:30 గంటలు)
    local_time = datetime.datetime(year, month, day, hour, minute)
    utc_time = local_time - datetime.timedelta(hours=5, minutes=30)
    utc_hour = utc_time.hour + utc_time.minute / 60.0
    
    # జూలియన్ డే గణన
    jd = swe.julday(utc_time.year, utc_time.month, utc_time.day, utc_hour)
    swe.set_sid_mode(swe.SIDM_LAHIRI) # లాహిరి అయనాంశ
    
    # లగ్న గణన
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)
    lagna_idx = int(ascmc[0] / 30)
    
    # చంద్రుడి స్థానం (రాశి, నక్షత్రం)
    res, ret = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)
    moon_degree = res[0]
    
    rashi_idx = int(moon_degree / 30)
    nakshatra_pos = moon_degree / (360 / 27)
    nakshatra_idx = int(nakshatra_pos)
    pada = int((nakshatra_pos - nakshatra_idx) * 4) + 1
    
    return {
        "లగ్నం": RASHIS[lagna_idx],
        "రాశి": RASHIS[rashi_idx],
        "నక్షత్రం": NAKSHATRAS[nakshatra_idx],
        "పాదం": pada
    }
st.title("ఆచార్య అస్ట్రో యాప్")
st.write("మీ జాతక చక్రం మరియు జ్యోతిష్య వివరాల కోసం ఈ యాప్ ఉపయోగపడు
import datetime

# యాప్ టైటిల్ మరియు హెడర్
st.set_page_config(page_title="ఆచార్య ఆస్ట్రో యాప్", layout="centered")
st.title("🔮 ఆచార్య ఆస్ట్రో యాప్ (Acharya Astro App)")
st.write("మీ జాతక చక్రం, రాశి, నామాంశ మరియు దశల వివరాలు ఇక్కడ చూసుకోవచ్చు.")

st.markdown("---")

# వివరాలు నమోదు చేసే సెక్షన్
st.header("👤 మీ వివరాలు నమోదు చేయండి")

# పేరు, పుట్టిన తేదీ, సమయం ఇన్‌పుట్స్
name = st.text_input("మీ పేరు (Name):")
dob = st.date_input("పుట్టిన తేదీ (Date of Birth):", min_value=datetime.date(1900, 1, 1))
tob = st.time_input("పుట్టిన సమయం (Time of Birth):")
place = st.text_input("పుట్టిన ఊరు (Place of Birth):")

st.markdown("---")

# లెక్కించడానికి బటన్
if st.button("🌟 జాతక చక్రం మరియు దశల వివరాలు చూపించు"):
    if name:
        st.success(f"ధన్యవాదాలు {name} గారు! మీ వివరాలు విజయవంతంగా నమోదయ్యాయి.")
        
        # 1. జాతక చక్రం సెక్షన్
        st.subheader("📊 1. జాతక చక్రం (Horoscope Chart)")
        col1, col2 = st.columns(2)
        with col1:
            st.info("📌 రాశి చక్రం (Rasi Kundali)")
            st.write("• లగ్నం: [గణన జరుగుతోంది...]")
            st.write("• రాశి: [గణన జరుగుతోంది...]")
        with col2:
            st.info("📌 నామాంశ చక్రం (Navamsha Chart)")
            st.write("• నక్షత్రం: [గణన జరుగుతోంది...]")
            st.write("• పాదం: [గణన జరుగుతోంది...]")

        st.markdown("---")

        # 2. దశల సెక్షన్
        st.subheader("⏳ 2. దశల వీక్షణ (Dasha Details)")
        st.warning("ప్రస్తుత మరియు రాబోయే దశల వివరాలు:")
        
        # టేబుల్ రూపంలో దశల వివరాలు
        st.write("• మహాదశ (Maha Dasha): [గణన జరుగుతోంది...]")
        st.write("• అంతర్దశ (Antardasha): [గణన జరుగుతోంది...]")
        st.write("• విదశ / ప్రత్యంతర్దశ (Pratyantar Dasha): [గణన జరుగుతోంది...]")
        st.write("• సూక్ష్మ దశ (Sukshma Dasha): [గణన జరుగుతోంది...]")
        
# మీ యాప్‌లోని బటన్ కోడ్ లోపల ఇలా మార్చండి:
if st.button("జాతకం లెక్కించు"):
    with st.spinner("జాతక గణన జరుగుతోంది... దయచేసి వేచి ఉండండి..."):
        try:
            # ఇక్కడ మీ యాప్ లోని Input Variables (తేదీ, సమయం, Lat, Lon) పేర్లు ఇవ్వాలి
            # ఉదాహరణకు యూజర్ ఎంటర్ చేసిన వివరాలను ఈ ఫంక్షన్‌కి పంపుతున్నాం
            ఫలితాలు = calculate_horoscope(year, month, day, hour, minute, latitude, longitude)
            
            # స్క్రీన్ పై అందంగా చూపించడానికి UI బాక్సులు
            st.success("గణన విజయవంతంగా పూర్తయింది!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="మీ లగ్నం", value=ఫలితాలు["లగ్నం"])
            with col2:
                st.metric(label="మీ రాశి", value=ఫలితాలు["రాశి"])
            with col3:
                st.metric(label="మీ నక్షత్రం", value=f"{ఫలితాలు['నక్షత్రం']} - {ఫలితాలు['పాదం']} పాదం")
                
        except Exception as e:
            st.error("గణన చేయడంలో తప్పు జరిగింది. వివరాలు సరిగ్గా ఇచ్చారో లేదో చూసుకోండి.")
