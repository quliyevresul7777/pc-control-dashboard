import os
import streamlit as st
from supabase import create_client, Client

URL = os.environ.get("SUPABASE_URL", "https://sfshteybktaruvawmmsb.supabase.co")
KEY = os.environ.get("SUPABASE_KEY")

st.set_page_config(page_title="ByteV3nom Control Center", layout="wide", page_icon="🐍")
st.title("🐍 ByteV3nom - Mobil İdarəetmə Mərkəzi")

if not KEY:
    st.error("⚠️ SUPABASE_KEY tanımlanmadı!")
    st.stop()

supabase: Client = create_client(URL, KEY)

def send_cmd(cmd):
    try:
        supabase.table("commands").insert({"command": cmd}).execute()
        st.toast(f"✅ Əmr göndərildi: {cmd}", icon="⚡")
    except Exception as e:
        st.error(f"Xəta: {e}")

# Sidebar - Sürətli Kontrollər
st.sidebar.title("🎮 Sürətli Düymələr")
if st.sidebar.button("📸 Ekran Şəkli Al (Screenshot)", use_container_width=True):
    send_cmd("screenshot")
if st.sidebar.button("📷 Kamera Şəkli (Webcam)", use_container_width=True):
    send_cmd("webcam")
if st.sidebar.button("🔒 Ekranı Kilidlə", use_container_width=True):
    send_cmd("lock")
if st.sidebar.button("🌙 Yuxu Rejimi", use_container_width=True):
    send_cmd("sleep")

st.sidebar.divider()
st.sidebar.subheader("🔊 Səs və Parlaqlıq")
vol = st.sidebar.slider("Səs (%)", 0, 100, 50)
if st.sidebar.button("Səsi Ayarla", use_container_width=True):
    send_cmd(f"volume {vol}")

bright = st.sidebar.slider("Parlaqlıq (%)", 0, 100, 80)
if st.sidebar.button("Parlaqlığı Ayarla", use_container_width=True):
    send_cmd(f"brightness {bright}")

# Tablar
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🖥️ Sistem & Proseslər", 
    "🎵 Media & Brauzer", 
    "🎙️ Mikrofon & Səs", 
    "💡 Wake-on-LAN (Açma)", 
    "⚡ Terminal"
])

with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Sistem Statusu", use_container_width=True): send_cmd("sysinfo")
        if st.button("🔋 Batareya Məlumatı", use_container_width=True): send_cmd("battery")
    with col2:
        if st.button("📝 İşləyən Proseslər (proc)", use_container_width=True): send_cmd("proc")
        if st.button("📋 Clipboard Oxu", use_container_width=True): send_cmd("clipget")
    with col3:
        if st.button("🛑 Kompüteri Söndür", use_container_width=True): send_cmd("shutdown")
        if st.button("🔄 Yenidən Başlat", use_container_width=True): send_cmd("restart")

with tab2:
    st.subheader("🎵 Media Düymələri")
    m1, m2, m3 = st.columns(3)
    with m1:
        if st.button("⏯️ Başlat/Saxla", use_container_width=True): send_cmd("media play_pause")
    with m2:
        if st.button("⏭️ Növbəti", use_container_width=True): send_cmd("media next")
    with m3:
        if st.button("⏮️ Əvvəlki", use_container_width=True): send_cmd("media prev")

    st.divider()
    st.subheader("🌐 Brauzerdə Axtarış")
    browser_choice = st.selectbox("Brauzer Seçimi:", ["default", "chrome", "edge", "firefox", "brave"])
    search_q = st.text_input("Axtarılacaq söz:")
    if st.button("🔍 Brauzerdə Axtar"):
        send_cmd(f"search {browser_choice} {search_q}")

with tab3:
    st.subheader("🎙️ Ətrafın Səsini Yazmaq")
    rec_sec = st.number_input("Qeyd müddəti (saniyə):", min_value=1, max_value=60, value=5)
    if st.button("🔴 Səs Yaz"):
        send_cmd(f"record {rec_sec}")

with tab4:
    st.subheader("🔌 Kompüteri Uzaqdan Yandırmaq (Wake-on-LAN)")
    st.info("Kompüter tam sönülü olduqda onu açmaq üçün Şəbəkə Kartının (MAC Adres) məlumatı lazımdır.")
    mac_addr = st.text_input("Kompüterin MAC Adresi (məs: AA:BB:CC:DD:EE:FF):")
    if st.button("⚡ Kompüterə Yandırma Sinyalı Göndər (WOL)"):
        send_cmd(f"wol {mac_addr}")

with tab5:
    st.subheader("💻 Terminal / CMD Əmri")
    cmd_in = st.text_input("İcra olunacaq komanda:")
    if st.button("⚡ İcra Et"):
        send_cmd(f"run {cmd_in}")

st.divider()
st.subheader("📱 Kompüterdən Gələn Nəticələr")
try:
    response = supabase.table("commands").select("*").order("created_at", desc=True).limit(10).execute()
    st.dataframe(response.data, use_container_width=True)
except Exception as e:
    st.error(f"Xəta: {e}")
