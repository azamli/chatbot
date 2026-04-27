import streamlit as st
from groq import Groq
import base64

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Aalam Healthcare AI",
    page_icon="⚕️",
    layout="centered",
)
from dotenv import load_dotenv
import os

load_dotenv()
# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

:root {
    --bg:       #060D1A;
    --card:     #0E1C2F;
    --border:   rgba(0,200,150,0.15);
    --accent:   #00C896;
    --accent2:  #00A3FF;
    --danger:   #FF6B6B;
    --text:     #E8F0F8;
    --muted:    #5A7088;
    --user-bg:  #0A2540;
    --bot-bg:   #0D1E30;
}

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}
#MainMenu, footer, header { visibility: hidden; }
.main .block-container { max-width: 860px; padding: 1.2rem 1rem 6rem; }

/* HEADER */
.header {
    display: flex; align-items: center; gap: 1.2rem;
    padding: 1.6rem 2rem;
    background: linear-gradient(135deg, #0C1A2E 0%, #091422 100%);
    border: 1px solid var(--border); border-radius: 22px;
    margin-bottom: 1.2rem; position: relative; overflow: hidden;
}
.header::before {
    content: ''; position: absolute; top: -50px; right: -50px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(0,200,150,0.10) 0%, transparent 70%);
    border-radius: 50%;
}
.header-icon {
    font-size: 3rem;
    filter: drop-shadow(0 0 14px rgba(0,200,150,0.7));
    animation: glow 3s ease-in-out infinite; z-index:1;
}
@keyframes glow {
    0%,100% { filter: drop-shadow(0 0 14px rgba(0,200,150,0.7)); }
    50%      { filter: drop-shadow(0 0 26px rgba(0,200,150,1.0)); }
}
.hc { z-index:1; }
.header-brand {
    font-family: 'DM Serif Display', serif;
    font-size: 1.75rem; color: white;
}
.header-brand span { color: var(--accent); }
.header-tagline { color: var(--muted); font-size: 0.82rem; margin-top: 3px; }
.status-pill {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(0,200,150,0.08);
    border: 1px solid rgba(0,200,150,0.25);
    color: var(--accent);
    font-size: 0.70rem; font-weight: 600; letter-spacing: 0.8px;
    padding: 3px 10px; border-radius: 20px; margin-top: 8px;
}
.status-dot {
    width: 6px; height: 6px; background: var(--accent);
    border-radius: 50%; animation: blink 2s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.2;} }

/* SCOPE BANNER */
.scope-banner {
    display: flex; align-items: flex-start; gap: 0.8rem;
    background: rgba(0,200,150,0.04);
    border: 1px solid rgba(0,200,150,0.18);
    border-left: 3px solid var(--accent); border-radius: 12px;
    padding: 0.85rem 1.2rem; margin-bottom: 1.2rem;
    font-size: 0.83rem; color: #8BBEAA; line-height: 1.6;
}
.scope-banner strong { color: var(--accent); }

/* SECTION LABEL */
.section-label {
    font-size: 0.70rem; font-weight: 600; color: var(--muted);
    letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 0.6rem;
}

/* CHAT */
.chat-wrap { display: flex; flex-direction: column; gap: 1.1rem; margin: 1rem 0; }
.msg-row { display: flex; gap: 0.75rem; align-items: flex-start; }
.msg-row.user { flex-direction: row-reverse; }
.avatar {
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; flex-shrink: 0; border: 1.5px solid var(--border);
}
.avatar.bot  { background: linear-gradient(135deg,#0A2030,#102840); color: var(--accent); }
.avatar.user { background: linear-gradient(135deg,#0A2540,#071A2E); color: var(--accent2); }
.bubble {
    max-width: 78%; padding: 0.95rem 1.25rem;
    border-radius: 18px; font-size: 0.91rem; line-height: 1.78;
}
.bubble.bot    { background:var(--bot-bg); border:1px solid var(--border); border-top-left-radius:4px; color:var(--text); }
.bubble.user   { background:var(--user-bg); border:1px solid rgba(0,163,255,0.2); border-top-right-radius:4px; color:#C8E4F8; }
.bubble.reject { background:rgba(255,107,107,0.06); border:1px solid rgba(255,107,107,0.25); border-top-left-radius:4px; color:#F0A0A0; }
.bubble-sender {
    font-size: 0.67rem; font-weight: 700; letter-spacing: 1.2px;
    text-transform: uppercase; color: var(--muted); margin-bottom: 5px;
}
.bubble.bot    .bubble-sender { color: var(--accent); }
.bubble.user   .bubble-sender { color: var(--accent2); text-align:right; }
.bubble.reject .bubble-sender { color: var(--danger); }

/* TYPING */
.typing { display:flex; gap:5px; align-items:center; padding:4px 0; }
.typing span {
    width:7px; height:7px; background:var(--accent);
    border-radius:50%; animation:bounce 1.3s ease-in-out infinite; opacity:0.6;
}
.typing span:nth-child(2){animation-delay:.18s;}
.typing span:nth-child(3){animation-delay:.36s;}
@keyframes bounce {
    0%,80%,100%{transform:translateY(0);opacity:0.4;}
    40%         {transform:translateY(-7px);opacity:1;}
}

/* INPUT */
.stTextArea textarea {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.93rem !important;
    resize: none !important;
    padding: 0.75rem 1rem !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,200,150,0.08) !important;
}
.stTextArea textarea::placeholder { color: var(--muted) !important; }
.stTextArea > div { background: transparent !important; }

.stButton > button {
    background: linear-gradient(135deg,#00C896,#00A878) !important;
    color: #040D18 !important; border: none !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important; font-size: 0.88rem !important;
    width: 100% !important; padding: 0.7rem !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background: rgba(0,200,150,0.03) !important;
    border: 1px dashed rgba(0,200,150,0.25) !important;
    border-radius: 12px !important;
    padding: 0.5rem !important;
}

/* VOICE CARD */
.voice-card {
    background: rgba(0,163,255,0.04);
    border: 1px solid rgba(0,163,255,0.2);
    border-radius: 14px; padding: 0.9rem 1.2rem;
    margin-bottom: 1rem; text-align: center;
}
.voice-title { color: var(--accent2); font-size: 0.75rem; font-weight:600; letter-spacing:1px; text-transform:uppercase; margin-bottom:0.5rem; }
.voice-note  { color: var(--muted); font-size: 0.75rem; margin-top:0.5rem; }
.v-btn {
    background: linear-gradient(135deg,#00A3FF,#0080CC);
    color: white; border: none; border-radius: 10px;
    padding: 8px 24px; font-size: 0.88rem; font-weight:600;
    cursor: pointer; font-family: 'DM Sans', sans-serif;
    transition: opacity 0.2s;
}
.v-btn:hover { opacity: 0.85; }

/* DIVIDER */
hr.divider { border:none; border-top:1px solid rgba(255,255,255,0.05); margin:1rem 0; }

/* DISCLAIMER */
.disclaimer {
    font-size: 0.72rem; color: var(--muted);
    text-align: center; padding: 0.9rem 1rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    margin-top: 1rem; line-height: 1.6;
}
.disclaimer strong { color: #6A8FA8; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# VOICE JS
# ─────────────────────────────────────────────
st.components.v1.html("""
<div class="voice-card" style="
    background:rgba(0,163,255,0.04);
    border:1px solid rgba(0,163,255,0.2);
    border-radius:14px; padding:0.9rem 1.2rem;
    margin-bottom:0.5rem; text-align:center;
    font-family:'DM Sans',sans-serif;">
    <div style="color:#00A3FF;font-size:0.75rem;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:0.5rem;">
        🎙️ Voice Input
    </div>
    <button id="vbtn" onclick="startVoice()" style="
        background:linear-gradient(135deg,#00A3FF,#0080CC);
        color:white;border:none;border-radius:10px;
        padding:8px 24px;font-size:0.88rem;font-weight:600;
        cursor:pointer;font-family:DM Sans,sans-serif;">
        🎙️ Click to Speak
    </button>
    <div id="vtranscript" style="color:#5A7088;font-size:0.78rem;margin-top:0.5rem;">
        Chrome browser recommended · Speak your health question
    </div>
</div>

<script>
function startVoice() {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { alert('Voice not supported. Please use Chrome.'); return; }
    const rec = new SR();
    rec.lang = 'en-US';
    rec.interimResults = false;
    rec.maxAlternatives = 1;
    document.getElementById('vbtn').innerText = '🔴 Listening...';
    document.getElementById('vbtn').style.background = '#c0392b';
    rec.start();
    rec.onresult = function(e) {
        const t = e.results[0][0].transcript;
        document.getElementById('vtranscript').innerText = '✅ Heard: ' + t;
        document.getElementById('vbtn').innerText = '🎙️ Click to Speak';
        document.getElementById('vbtn').style.background = 'linear-gradient(135deg,#00A3FF,#0080CC)';
        // Send transcript to parent Streamlit textarea
        try {
            const ta = window.parent.document.querySelector('textarea');
            if (ta) {
                const setter = Object.getOwnPropertyDescriptor(window.parent.HTMLTextAreaElement.prototype, 'value').set;
                setter.call(ta, t);
                ta.dispatchEvent(new Event('input', {bubbles:true}));
            }
        } catch(err) { console.log(err); }
    };
    rec.onerror = function(e) {
        document.getElementById('vbtn').innerText = '🎙️ Click to Speak';
        document.getElementById('vbtn').style.background = 'linear-gradient(135deg,#00A3FF,#0080CC)';
        document.getElementById('vtranscript').innerText = 'Error: ' + e.error;
    };
    rec.onend = function() {
        document.getElementById('vbtn').innerText = '🎙️ Click to Speak';
        document.getElementById('vbtn').style.background = 'linear-gradient(135deg,#00A3FF,#0080CC)';
    };
}
</script>
""", height=110)

# ─────────────────────────────────────────────
# GROQ CLIENT + SYSTEM PROMPT
# ─────────────────────────────────────────────

import os
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
SYSTEM_PROMPT = """You are Aalam Healthcare AI, a professional medical assistant by Aalam Healthcare.

STRICT RULES:
1. ONLY answer healthcare and medical questions.
2. ALWAYS respond in ENGLISH only.
3. Accepted topics: symptoms, diseases, medications, treatments, nutrition, mental health, first aid, anatomy, fitness, pregnancy, child health, elderly care, dental, eye, skin, vaccines, medical tests, health tips, wellness.
4. If user asks about ANYTHING outside healthcare — respond ONLY with:
   "I'm Aalam Healthcare AI and I'm only able to assist with healthcare and medical questions. Your question appears to be outside my scope. Please ask me anything related to health, symptoms, medications, or wellness!"
5. If an image is shared, analyze it from a medical/health perspective only (skin conditions, wounds, reports, etc.).
6. Always recommend consulting a qualified doctor for serious concerns.
7. For emergencies, advise calling 108 (India) or 911 (US) immediately.
8. Be professional, warm, clear, and well-structured in English only.
"""

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "messages"      not in st.session_state: st.session_state.messages      = []
if "pending"       not in st.session_state: st.session_state.pending        = None
if "input_key"     not in st.session_state: st.session_state.input_key      = 0

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="header">
    <div class="header-icon">⚕️</div>
    <div class="hc">
        <div class="header-brand">Aalam <span>Healthcare</span> AI</div>
        <div class="header-tagline">Your trusted AI-powered medical assistant</div>
        <div class="status-pill">
            <span class="status-dot"></span> ONLINE &nbsp;·&nbsp; Healthcare Specialist
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="scope-banner">
    🩺&nbsp;&nbsp;<div>
    <strong>Healthcare Topics Only.</strong> Aalam Healthcare AI answers questions about
    symptoms, diseases, medications, treatments, nutrition, mental health, first aid, and wellness.
    Questions outside the medical field will not be answered.
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# QUICK QUESTIONS
# ─────────────────────────────────────────────
QUICK = [
    "💊 What is Paracetamol used for?",
    "🤒 How to treat a high fever?",
    "🩸 What causes high blood pressure?",
    "😴 How to improve sleep quality?",
    "🤰 Diet tips during pregnancy?",
    "🧠 How to reduce anxiety naturally?",
    "🦷 How to prevent tooth decay?",
    "🏃 Best exercises for heart health?",
]

st.markdown('<p class="section-label">⚡ Quick Questions</p>', unsafe_allow_html=True)
qcols = st.columns(4)
for i, q in enumerate(QUICK):
    with qcols[i % 4]:
        if st.button(q, key=f"q_{i}"):
            st.session_state.pending = {"text": q, "image": None}

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CHAT HISTORY DISPLAY
# ─────────────────────────────────────────────
if st.session_state.messages:
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        role    = msg["role"]
        content = msg["content"]
        reject  = msg.get("is_reject", False)
        img_b64 = msg.get("image_b64")

        if role == "user":
            img_html = (f'<br><img src="data:image/jpeg;base64,{img_b64}" '
                        f'style="max-width:220px;border-radius:10px;margin-top:8px;">') if img_b64 else ""
            st.markdown(f"""
            <div class="msg-row user">
                <div class="avatar user">👤</div>
                <div class="bubble user">
                    <div class="bubble-sender">You</div>
                    {content}{img_html}
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            cls = "reject" if reject else "bot"
            st.markdown(f"""
            <div class="msg-row bot">
                <div class="avatar bot">⚕️</div>
                <div class="bubble {cls}">
                    <div class="bubble-sender">Aalam Healthcare AI</div>
                    {content}
                </div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INPUT SECTION
# ─────────────────────────────────────────────
uploaded = st.file_uploader(
    "📎 Attach a medical image — skin condition, medical report, wound, etc. (optional)",
    type=["png", "jpg", "jpeg"],
    key=f"file_{st.session_state.input_key}"
)

user_text = st.text_area(
    "msg",
    placeholder="Type your healthcare question here...",
    height=85,
    label_visibility="collapsed",
    key=f"txt_{st.session_state.input_key}"
)

c1, c2 = st.columns([4, 1])
with c1:
    send_btn = st.button("➤  Send Message", use_container_width=True)
with c2:
    clear_btn = st.button("🗑️ Clear", use_container_width=True)

# ─────────────────────────────────────────────
# HANDLE BUTTONS
# ─────────────────────────────────────────────
if clear_btn:
    st.session_state.messages  = []
    st.session_state.pending   = None
    st.session_state.input_key += 1
    st.rerun()

if send_btn and (user_text.strip() or uploaded):
    img_b64 = None
    if uploaded:
        img_b64 = base64.b64encode(uploaded.read()).decode("utf-8")

    st.session_state.pending   = {
        "text":  user_text.strip() if user_text.strip() else "Please analyze this medical image.",
        "image": img_b64
    }
    st.session_state.input_key += 1   # ← key rotation clears textarea + file uploader
    st.rerun()

# ─────────────────────────────────────────────
# PROCESS PENDING MESSAGE
# ─────────────────────────────────────────────
if st.session_state.pending is not None:
    p       = st.session_state.pending
    q_text  = p["text"]
    q_img   = p["image"]
    st.session_state.pending = None  # clear so it doesn't re-trigger

    # Save user message
    st.session_state.messages.append({
        "role": "user", "content": q_text, "image_b64": q_img
    })

    # Build API payload
    api_msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in st.session_state.messages:
        if m["role"] == "user":
            if m.get("image_b64"):
                api_msgs.append({
                    "role": "user",
                    "content": [
                        {"type": "image_url",
                         "image_url": {"url": f"data:image/jpeg;base64,{m['image_b64']}"}},
                        {"type": "text", "text": m["content"]}
                    ]
                })
            else:
                api_msgs.append({"role": "user", "content": m["content"]})
        elif m["role"] == "assistant":
            api_msgs.append({"role": "assistant", "content": m["content"]})

    # Typing indicator
    t_ph = st.empty()
    t_ph.markdown("""
    <div class="msg-row bot" style="margin-top:1rem;">
        <div class="avatar bot">⚕️</div>
        <div class="bubble bot">
            <div class="typing"><span></span><span></span><span></span></div>
        </div>
    </div>""", unsafe_allow_html=True)

    try:
        model = "meta-llama/llama-4-scout-17b-16e-instruct" if q_img else "llama-3.1-8b-instant"
        stream = client.chat.completions.create(
            model=model,
            messages=api_msgs,
            max_tokens=900,
            stream=True,
            temperature=0.5,
        )

        full = ""
        r_ph = st.empty()
        t_ph.empty()

        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                full += delta
                r_ph.markdown(f"""
                <div class="msg-row bot" style="margin-top:1rem;">
                    <div class="avatar bot">⚕️</div>
                    <div class="bubble bot">
                        <div class="bubble-sender">Aalam Healthcare AI</div>
                        {full}▌
                    </div>
                </div>""", unsafe_allow_html=True)

        r_ph.empty()

        is_reject = ("outside my scope" in full.lower() or
                     "only able to assist" in full.lower())

        st.session_state.messages.append({
            "role": "assistant", "content": full, "is_reject": is_reject
        })

    except Exception as e:
        t_ph.empty()
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"⚠️ Connection error: {str(e)}. Please check your API key.",
            "is_reject": False
        })

    st.rerun()

# ─────────────────────────────────────────────
# DISCLAIMER
# ─────────────────────────────────────────────
st.markdown("""
<div class="disclaimer">
    <strong>⚕️ Medical Disclaimer:</strong> Aalam Healthcare AI provides general health information only
    and does not replace professional medical advice, diagnosis, or treatment.
    Always consult a qualified healthcare provider for medical concerns.
    In case of emergency, call <strong>108</strong> (India) or <strong>911</strong> (US) immediately.
</div>
""", unsafe_allow_html=True)