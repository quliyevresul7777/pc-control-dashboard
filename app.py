import os
import time
import streamlit as st
from supabase import create_client, Client

Supabase Konfiqurasiyası

URL = "https://sfshteybktaruvawmmsb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNmc2h0ZXlia3RhcnV2YXdtbXNiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTA0MDgyNTcsImV4cCI6MjEwNTk4NDI1N30.jHeTFuSf5Nb7A_aNP9Kc_NLz1W1r-GRwdQcj_bacDOg"

st.set_page_config(
page_title="ByteV3nom App",
layout="centered",
page_icon="🟢",
initial_sidebar_state="collapsed"
)

supabase: Client = create_client(URL, KEY)

Telefonda PWA (Tətbiq İkonası) və Müasir Neon-Yaşıl UI Stili

st.markdown("""

""", unsafe_allow_html=True)

def send_cmd(cmd_text):
if not cmd_text.strip():
return
try:
supabase.table("commands").insert({"command": cmd_text.strip()}).execute()
st.toast(f"🟢 Əmr göndərildi: {cmd_text}")
except Exception as e:
st.error(f"Xəta: {e}")

--- SOL MENYU (SIDEBAR & ƏN ÇOX İSTİFADƏ OLUNANLARIN AVTO-ANALİZİ) ---

st.sidebar.title("🟢 ByteV3nom Menyu")

top_cmds = []
try:
all_data = supabase.table("commands").select("command").execute().data
if all_data:
counts = {}
for d in all_data:
c = d.get("command", "").split()[0].lower()
counts[c] = counts.get(c, 0) + 1
sorted_cmds = sorted(counts.items(), key=lambda x: x[1], reverse=True)
top_cmds = [x[0] for x in sorted_cmds[:4]]
except Exception:
pass

if top_cmds:
st.sidebar.subheader("🔥 Ən çox istifadə olunanlar")
col_t1, col_t2 = st.sidebar.columns(2)
for idx, c_name in enumerate(top_cmds):
if idx % 2 == 0:
if col_t1.button(f"⭐ {c_name}"): send_cmd(c_name)
else:
if col_t2.button(f"⭐ {c_name}"): send_cmd(c_name)
st.sidebar.divider()

st.sidebar.subheader("⚡ Sürətli Əmrlər")
c1, c2 = st.sidebar.columns(2)
with c1:
if st.button("📸 Screen"): send_cmd("screen")
if st.button("🔒 Kilidlə"): send_cmd("lock")
with c2:
if st.button("🌙 Yuxu"): send_cmd("sleep")
if st.button("🛑 Söndür"): send_cmd("shutdown")

st.sidebar.divider()
st.sidebar.subheader("🔊 Səs & Parlaqlıq")
v_val = st.sidebar.slider("Səs (%)", 0, 100, 50)
if st.sidebar.button("Səsi Tənzimlə"): send_cmd(f"səs {v_val}")

b_val = st.sidebar.slider("Parlaqlıq (%)", 0, 100, 80)
if st.sidebar.button("Parlaqlığı Tənzimlə"): send_cmd(f"parlaqlıq {b_val}")

--- ƏSAS ÇAT EKRANI (TELEGRAM STİLİ) ---

st.title("💬 ByteV3nom Chat")
st.caption("Əmri aşağıdan yazın və ya soldakı menyudan düymələrə basın.")

try:
chat_res = supabase.table("commands").select("*").order("created_at", desc=True).limit(8).execute()
chat_data = reversed(chat_res.data) if chat_res.data else []

for chat in chat_data:
    cmd = chat.get("command", "")
    res = chat.get("result", "Gözlənilir...")
    f_url = chat.get("file_url")

    # İstifadəçinin əmri (Sağda)
    st.markdown(f'


', unsafe_allow_html=True)

    # Botun cavabı (Solda)
    st.markdown(f'


', unsafe_allow_html=True)
if f_url:
st.image(f_url, use_column_width=True)
except Exception as e:
st.error(f"Xəta: {e}")

Aşağıdakı Mesaj Yazma Xanasi

st.divider()
with st.form(key="chat_form", clear_on_submit=True):
user_input = st.text_input("Əmri yazın...", placeholder="Məsələn: screen, səs 50, aç chrome...")
submit_btn = st.form_submit_button("💬 Göndər")
if submit_btn and user_input:
send_cmd(user_input)
st.rerun()
