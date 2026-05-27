import datetime
import streamlit as st
import swisseph as swe# --- 3. స్ట్రీమ్‌లిట్ స్క్రీన్ డిజైన్ (UI) ---
st.set_page_config(page_title="ఆచార్య అడ్వాన్స్డ్ ఆస్ట్రో", layout="wide")
st.title("🕉️ ఆచార్య అడ్వాన్స్డ్ ఆస్ట్రో యాప్")
st.write("ఇక్కడ మీ పూర్తి జాతక చక్రం, రాశి-నక్షత్ర వివరాలు మరియు వింశోత్తరి దశలను ఖచ్చితంగా తెలుసుకోవచ్చు.")

st.markdown("---")

# ఇన్‌పుట్ ఫీల్డ్‌లు
col_in1, col_in2 = st.columns(2)
with col_in1:
    name = st.text_input("👤 మీ పేరు (Name):")
    dob = st.date_input("📅 పుట్టిన తేదీ (Date of Birth):", min_value=datetime.date(1900, 1, 1))
    tob = st.time_input("⏰ పుట్టిన సమయం (Time of Birth):")
with col_in2:
    place = st.text_input("📍 పుట్టిన ఊరు (Place of Birth):")
    latitude = st.number_input("🌐 అక్షాంశం (Latitude - ఉదా: 17.3850)", value=17.3850, format="%.4f")
    longitude = st.number_input("🌐 ரேఖాంశం (Longitude - ఉదా: 78.4867)", value=78.4867, format="%.4f")

st.markdown("---")

if st.button("🔮 పూర్తి జాతక చక్రం & దశలు గణించు", type="primary"):
    if name and place:
        with st.spinner("గ్రహ స్థానాలు మరియు దశల గణన జరుగుతోంది..."):
            try:
                # లెక్కింపు రన్ చేయడం
                res = calculate_complete_horoscope(
                    dob.year, dob.month, dob.day, tob.hour, tob.minute, latitude, longitude
                )
                
                st.success("🎉 గణితం విజయవంతంగా పూర్తయింది!")
                
                # --- విభాగాలు చూపించడం ---
                tab1, tab2, tab3 = st.tabs(["✨ ప్రాథమిక వివరాలు", "📊 జాతక చక్రం (Kundali)", "⏳ వింశోత్తరి దశలు"])
                
                with tab1:
                    st.subheader("📌 మీ జనన నಕ್ಷత్ర మరియు రాశి వివరాలు")
                    c1, c2, c3 = st.columns(3)
                    c1.metric("🌟 లగ్నం", res["లగ్నం"])
                    c2.metric("🌙 రాశి", res["రాశి"])
                    c3.metric("✨ నక్షత్రం", f"{res['నక్షత్రం']} - {res['పాదం']} వ పాదం")
                    
                with tab2:
                    st.subheader("📦 రాశి కుండలి చక్రం (12 ఇళ్లు)")
                    st.write("కింది బాక్సులలో ఏయే గ్రహాలు ఏ రాశిలో ఉన్నాయో స్పష్టంగా చూడవచ్చు:")
                    
                    grid_cols = st.columns(4)
                    for idx, r_name in enumerate(RASHIS):
                        col_pos = idx % 4
                        with grid_cols[col_pos]:
                            planets_in_rashi = ", ".join(res["చక్రం"][idx]) if res["చక్రం"][idx] else "ఖాళీ"
                            st.info(f"{r_name} \n\n {planets_in_rashi}")
                            
                with tab3:
                    st.subheader("⏳ ప్రస్తుత మరియు రాబోయే వింశోత్తరి మహాదశల వివరాలు")
                    st.write("ఏ మహాదశ ఏ తేదీతో ముగుస్తుందో కింద ఇవ్వబడింది:")
                    st.table(res["దశలు"])
                    
            except Exception as e:
                st.error(f"గణనలో సాంకేతిక లోపం వచ్చింది: {e}. దయచేసి వివరాలు సరిగ్గా సరిచూసుకోండి.")
     else:
     st.warning("Please enter Name and Place.")
