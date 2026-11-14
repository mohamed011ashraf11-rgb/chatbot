import streamlit as st
from google import genai

API_KEY = "AQ.Ab8RN6L7DDyN3dk5POc9Xbr7tMS7svjInDC5O1KSrN3AzdXAoA"
MODEL = "gemini-2.5-flash"

USERS = {
    "admin": "1234",
    "student": "tiba2026",
}

PRIMARY = "#6C3FD1"
SECONDARY = "#9B5DE5"
ACCENT = "#F59E0B"
BG = "#F6F3FF"

SUGGESTED = [
    "إيه الأقسام الموجودة في المعهد؟",
    "المصاريف كام؟",
    "المعهد فين بالظبط؟",
    "إمتى مواعيد التقديم؟",
    "أتواصل مع شؤون الطلبة إزاي؟",
]

INFO = """
- اسم المعهد: معهد طيبة العالي لنظم ومعلومات الأعمال
- الأقسام: (نظم ومعلومات الأعمال، إدارة الأعمال، المحاسبةو اداره بنوك و علوم حاسب )
- المصاريف: (18000 و تختلف حسب القسم)
- العنوان: (في فرعين فرع في المعادي و التاني في طريق سقارة السياحي في المريوطيه)
- مواعيد التقديم والدراسة: (المواعيد تستمر قبل الميد ترم)
- التواصل: (مفيش ارقام ممكن تسالني وانا هرد عليك في كل اللي محتاجه)
"""

SYSTEM = f"""إنت مساعد ذكي للرد على أسئلة الطلبة عن معهد طيبة العالي.
جاوب بالعربي وبشكل مختصر ومحترم، ومن المعلومات دي بس.
لو السؤال مش موجود في المعلومات قول إنك مش متأكد، واطلب منهم يتواصلوا مع شؤون الطلبة.

المعلومات:
{INFO}"""

st.set_page_config(page_title="معهد طيبة العالي", page_icon="🎓")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Reem+Kufi:wght@500;700&display=swap');

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pop {
    0%   { transform: scale(0.5); opacity: 0; }
    70%  { transform: scale(1.15); }
    100% { transform: scale(1); opacity: 1; }
}
@keyframes floaty {
    0%   { transform: translateY(0) rotate(-4deg); }
    50%  { transform: translateY(-22px) rotate(4deg); }
    100% { transform: translateY(0) rotate(-4deg); }
}

.stApp { background: %BG%; }
.block-container { animation: fadeUp 0.8s ease; position: relative; z-index: 1; }

.deco {
    position: fixed; z-index: 0; pointer-events: none;
    font-family: 'Amiri', serif; color: %PRIMARY%;
    opacity: 0.12; animation: floaty 9s ease-in-out infinite;
}
.deco.o { color: %ACCENT%; opacity: 0.18; }

.header {
    background: linear-gradient(135deg, %PRIMARY%, %SECONDARY%);
    color: white; padding: 22px; border-radius: 18px;
    text-align: center; margin-bottom: 18px;
    box-shadow: 0 8px 20px rgba(108,63,209,0.25);
    animation: fadeUp 1s ease;
}
.header h2 { margin: 0; color: white; font-family: 'Reem Kufi', sans-serif; }
.header p { margin: 4px 0 0; opacity: 0.9; color: white; }

.logo { font-size: 4rem; text-align: center; animation: pop 0.9s ease; }
.title {
    text-align: center; font-size: 2rem; font-weight: 700;
    color: %PRIMARY%; font-family: 'Reem Kufi', sans-serif;
    animation: fadeUp 1.2s ease;
}
.motto {
    text-align: center; font-family: 'Amiri', serif;
    font-size: 1.5rem; color: %ACCENT%; margin: 2px 0 8px;
}
.orn {
    text-align: center; color: %ACCENT%;
    letter-spacing: 10px; font-size: 1.1rem; margin: 6px 0 14px;
}
.sub { text-align: center; color: gray; animation: fadeUp 1.6s ease; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, %PRIMARY%, %SECONDARY%);
}
section[data-testid="stSidebar"] * { color: white !important; }
section[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.35);
    border-radius: 12px; text-align: right;
    transition: all 0.2s ease;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: %ACCENT%; border-color: %ACCENT%;
}

[data-testid="stChatMessage"] {
    background: white; border-radius: 16px; padding: 12px 16px;
    margin-bottom: 10px; border: 1px solid #E5DDFB;
    animation: fadeUp 0.4s ease;
}
[data-testid="stChatMessage"] * { color: #222 !important; }

.stFormSubmitButton button {
    background: %PRIMARY%; color: white; border-radius: 12px; border: none;
}
</style>

<div class="deco" style="top:6%; left:5%; font-size:110px;">طَ</div>
<div class="deco o" style="top:18%; right:7%; font-size:80px; animation-delay:1s;">يِّ</div>
<div class="deco" style="top:48%; left:3%; font-size:90px; animation-delay:2s;">بَ</div>
<div class="deco o" style="top:60%; right:5%; font-size:120px; animation-delay:3s;">ةُ</div>
<div class="deco" style="bottom:6%; left:14%; font-size:100px; animation-delay:4s;">عِلْمٌ</div>
<div class="deco o" style="bottom:10%; right:16%; font-size:90px; animation-delay:5s;">نُورٌ</div>
"""

COLORS = {
    "%BG%": BG,
    "%PRIMARY%": PRIMARY,
    "%SECONDARY%": SECONDARY,
    "%ACCENT%": ACCENT,
}
for key, val in COLORS.items():
    CSS = CSS.replace(key, val)

st.markdown(CSS, unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def ask_gemini(messages):
    client = genai.Client(vertexai=True, api_key=API_KEY)

    contents = []
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": m["content"]}]})

    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config={"system_instruction": SYSTEM},
    )
    return response.text


def login_page():
    st.markdown('<div class="logo">🎓</div>', unsafe_allow_html=True)
    st.markdown('<div class="title">مَعْهَدُ طَيْبَةَ العَالِي</div>', unsafe_allow_html=True)
    st.markdown('<div class="motto">العِلْمُ نُورٌ</div>', unsafe_allow_html=True)
    st.markdown('<div class="orn">❁ ✦ ❁</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub">سجّل دخولك للمتابعة</div>', unsafe_allow_html=True)

    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", use_container_width=True)

    if submit:
        if USERS.get(username) == password and password != "":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("اسم المستخدم أو كلمة السر غلط")


def chat_page():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    header_html = (
        '<div class="header"><h2>🎓 مَعْهَدُ طَيْبَةَ العَالِي</h2>'
        '<div class="orn" style="color:white; margin:2px 0;">❁ ✦ ❁</div>'
        '<p>أهلاً ' + st.session_state.username + '، اسألني عن أي حاجة في المعهد</p></div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)

    clicked = None
    with st.sidebar:
        st.markdown('<div class="motto">العِلْمُ نُورٌ</div>', unsafe_allow_html=True)
        st.markdown("### 💡 أسئلة مقترحة")
        for i, q in enumerate(SUGGESTED):
            if st.button(q, key="sq" + str(i), use_container_width=True):
                clicked = q
        st.markdown("---")
        if st.button("🗑️ محادثة جديدة", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        if st.button("🚪 تسجيل خروج", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.messages = []
            st.rerun()

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    question = st.chat_input("اسأل عن المعهد...") or clicked

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        try:
            reply = ask_gemini(st.session_state.messages)
        except Exception as e:
            reply = "حصل خطأ: " + str(e)

        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)


if st.session_state.logged_in:
    chat_page()
else:
    login_page()
