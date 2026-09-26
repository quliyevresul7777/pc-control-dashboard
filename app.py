import os
import time
import streamlit as st
from supabase import create_client, Client

URL = os.environ.get("SUPABASE_URL", "https://sfshteybktaruvawmmsb.supabase.co")
KEY = os.environ.get("SUPABASE_KEY")

# PWA və Mobil Ekran Tənzimləmələri
st.set_page_config(
    page_title="ByteV3nom App",
    layout="centered",
    page_icon="🟢"
)

if not KEY:
    st.error("⚠️ SUPABASE_KEY təyin edilməyib!")
    st.stop()

supabase: Client = create_client(URL, KEY)

# Müasir Yaşıl Dark UI Stili (CSS)
st.markdown("""
    
""", unsafe_allow_html=True)


def send_cmd(cmd_text):
    if not cmd_text.strip():
        return

    try:
        supabase.table("commands").insert(
            {"command": cmd_text.strip()}
        ).execute()

        st.toast(f"🟢 Əmr göndərildi: {cmd_text}")

    except Exception as e:
        st.error(f"Xəta: {e}")


# --- SOL MENYU (SIDEBAR) ---

st.sidebar.title("🟢 ByteV3nom Menyu")


# Avto-Analiz: Ən çox istifadə olunan əmrləri bazadan çəkmək

top_cmds = []

try:
    all_data = supabase.table("commands").select("command").execute().data

    if all_data:
        counts = {}

        for d in all_data:
            c = d.get("command", "").split()[0].lower()
            counts[c] = counts.get(c, 0) + 1

        sorted_cmds = sorted(
            counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        top_cmds = [x[0] for x in sorted_cmds[:3]]

except Exception:
    pass


if top_cmds:
    st.sidebar.subheader("🔥 Ən çox istifadə olunanlar")

    col_t1, col_t2 = st.sidebar.columns(2)

    for idx, c_name in enumerate(top_cmds):

        if idx % 2 == 0:
            if col_t1.button(f"⭐ {c_name}"):
                send_cmd(c_name)

        else:
            if col_t2.button(f"⭐ {c_name}"):
                send_cmd(c_name)

    st.sidebar.divider()


st.sidebar.subheader("⚡ Sürətli Əmrlər")

c1, c2 = st.sidebar.columns(2)

with c1:

    if st.button("📸 Screen"):
        send_cmd("screen")

    if st.button("🔒 Kilidlə"):
        send_cmd("lock")


with c2:

    if st.button("🌙 Yuxu"):
        send_cmd("sleep")

    if st.button("🛑 Söndür"):
        send_cmd("shutdown")


st.sidebar.divider()

st.sidebar.subheader("🔊 Səs & Parlaqlıq")

v_val = st.sidebar.slider(
    "Səs",
    0,
    100,
    50
)

if st.sidebar.button("Səsi Tənzimlə"):
    send_cmd(f"səs {v_val}")


b_val = st.sidebar.slider(
    "Parlaqlıq",
    0,
    100,
    80
)

if st.sidebar.button("Parlaqlığı Tənzimlə"):
    send_cmd(f"parlaqlıq {b_val}")


# --- ƏSAS ÇAT EKRANI (TELEGRAM STİLİ) ---

st.title("💬 ByteV3nom Çat")

st.caption(
    "Əmri aşağıdan yazın və ya menyudan düyməyə basın."
)


# Son 8 mesajı göstərmək

try:

    chat_res = (
        supabase
        .table("commands")
        .select("*")
        .order("created_at", desc=True)
        .limit(8)
        .execute()
    )

    chat_data = (
        reversed(chat_res.data)
        if chat_res.data
        else []
    )

    for chat in chat_data:

        cmd = chat.get("command", "")
        res = chat.get("result", "Gözlənilir...")
        f_url = chat.get("file_url")

        # İstifadəçinin əmri (Sağda)

        st.markdown(
            f"""
            <div style="
                text-align: right;
                background-color: #1f6f43;
                padding: 10px;
                border-radius: 10px;
                margin: 5px 0;
            ">
                {cmd}
            </div>
            """,
            unsafe_allow_html=True
        )

        # Botun cavabı (Solda)

        st.markdown(
            f"""
            <div style="
                text-align: left;
                background-color: #222;
                padding: 10px;
                border-radius: 10px;
                margin: 5px 0;
            ">
                🤖 {res}
            </div>
            """,
            unsafe_allow_html=True
        )

        if f_url:
            st.image(
                f_url,
                use_column_width=True
            )

except Exception as e:
    st.error(f"Xəta: {e}")


# Aşağıdakı Mesaj Yazma Xanası

st.divider()

with st.form(
    key="chat_form",
    clear_on_submit=True
):

    user_input = st.text_input(
        "Əmri yazın...",
        placeholder="Məsələn: screen, səs 50, aç chrome..."
    )

    submit_btn = st.form_submit_button("💬 Göndər")

    if submit_btn and user_input:
        send_cmd(user_input)
        st.rerun()
