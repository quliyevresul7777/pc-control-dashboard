import streamlit as st
from supabase import create_client, Client

# =========================
# Supabase Konfiqurasiyası
# =========================
SUPABASE_URL = "https://sfshteybktaruvawmmsb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNmc2h0ZXlia3RhcnV2YXdtbXNiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTA0MDgyNTcsImV4cCI6MjEwNTk4NDI1N30.jHeTFuSf5Nb7A_aNP9Kc_NLz1W1r-GRwdQcj_bacDOg"

st.set_page_config(
    page_title="ByteV3nom App",
    page_icon="🟢",
    layout="centered",
)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================
# UI
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background: #07110b;
    }

    .chat-user {
        background: #123d24;
        padding: 10px 14px;
        border-radius: 14px;
        margin: 8px 0 4px auto;
        max-width: 85%;
        text-align: right;
    }

    .chat-bot {
        background: #101b14;
        border: 1px solid #1d5c36;
        padding: 10px 14px;
        border-radius: 14px;
        margin: 4px 0 8px 0;
        max-width: 85%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def send_cmd(cmd_text: str) -> None:
    """Bazaya yeni əmr əlavə edir."""
    cmd_text = cmd_text.strip()

    if not cmd_text:
        return

    try:
        supabase.table("commands").insert(
            {
                "command": cmd_text,
                "result": None,
                "file_url": None,
            }
        ).execute()

        st.toast(f"🟢 Əmr göndərildi: {cmd_text}")
    except Exception as e:
        st.error(f"Əmr göndərilərkən xəta baş verdi: {e}")


# =========================
# SOL MENYU
# =========================
st.sidebar.title("🟢 ByteV3nom Menyu")

# Ən çox istifadə olunan əmrlər
top_cmds = []

try:
    all_data = (
        supabase.table("commands")
        .select("command")
        .execute()
        .data
    )

    if all_data:
        counts = {}

        for item in all_data:
            command = (item.get("command") or "").strip()

            if not command:
                continue

            first_word = command.split()[0].lower()
            counts[first_word] = counts.get(first_word, 0) + 1

        sorted_cmds = sorted(
            counts.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        top_cmds = [item[0] for item in sorted_cmds[:4]]

except Exception:
    pass


if top_cmds:
    st.sidebar.subheader("🔥 Ən çox istifadə olunanlar")

    col_t1, col_t2 = st.sidebar.columns(2)

    for idx, command_name in enumerate(top_cmds):
        if idx % 2 == 0:
            if col_t1.button(f"⭐ {command_name}", key=f"top_{idx}"):
                send_cmd(command_name)
                st.rerun()
        else:
            if col_t2.button(f"⭐ {command_name}", key=f"top_{idx}"):
                send_cmd(command_name)
                st.rerun()

    st.sidebar.divider()


# Sürətli əmrlər
st.sidebar.subheader("⚡ Sürətli Əmrlər")

c1, c2 = st.sidebar.columns(2)

with c1:
    if st.button("📸 Screen"):
        send_cmd("screen")
        st.rerun()

    if st.button("🔒 Kilidlə"):
        send_cmd("lock")
        st.rerun()

with c2:
    if st.button("🌙 Yuxu"):
        send_cmd("sleep")
        st.rerun()

    if st.button("🛑 Söndür"):
        send_cmd("shutdown")
        st.rerun()


st.sidebar.divider()

# Səs
st.sidebar.subheader("🔊 Səs & Parlaqlıq")

v_val = st.sidebar.slider(
    "Səs (%)",
    min_value=0,
    max_value=100,
    value=50,
)

if st.sidebar.button("Səsi Tənzimlə"):
    send_cmd(f"səs {v_val}")
    st.rerun()


# Parlaqlıq
b_val = st.sidebar.slider(
    "Parlaqlıq (%)",
    min_value=0,
    max_value=100,
    value=80,
)

if st.sidebar.button("Parlaqlığı Tənzimlə"):
    send_cmd(f"parlaqlıq {b_val}")
    st.rerun()


# =========================
# ƏSAS ÇAT
# =========================
st.title("💬 ByteV3nom Chat")
st.caption("Əmri aşağıdan yazın və ya soldakı menyudan sürətli əmrlərdən istifadə edin.")

try:
    chat_res = (
        supabase.table("commands")
        .select("*")
        .order("created_at", desc=True)
        .limit(8)
        .execute()
    )

    chat_data = list(reversed(chat_res.data or []))

    for chat in chat_data:
        command = chat.get("command") or ""
        result = chat.get("result") or "Gözlənilir..."
        file_url = chat.get("file_url")

        # İstifadəçinin əmri
        st.markdown(
            f'<div class="chat-user">{command}</div>',
            unsafe_allow_html=True,
        )

        # Agentin cavabı
        st.markdown(
            f'<div class="chat-bot">🤖 {result}</div>',
            unsafe_allow_html=True,
        )

        # Screenshot varsa göstər
        if file_url:
            st.image(file_url, use_container_width=True)

except Exception as e:
    st.error(f"Çat məlumatları yüklənərkən xəta baş verdi: {e}")


# =========================
# MESAJ XANASI
# =========================
st.divider()

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Əmri yazın...",
        placeholder="Məsələn: screen, səs 50, aç chrome...",
    )

    submit_btn = st.form_submit_button("💬 Göndər")

    if submit_btn and user_input.strip():
        send_cmd(user_input)
        st.rerun()
