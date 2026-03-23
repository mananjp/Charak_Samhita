
import streamlit as st
import sys, os, json

# Robust path handling
_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if _root not in sys.path:
    sys.path.insert(0, _root)

try:
    from charaka_vaidya.frontend.styles.theme import CHARAKA_CSS, LOGO_HTML
    from charaka_vaidya.frontend.components.sidebar import render_sidebar
    from charaka_vaidya.core.constants import DOSHAS
except ImportError:
    from frontend.styles.theme import CHARAKA_CSS, LOGO_HTML
    from frontend.components.sidebar import render_sidebar
    from core.constants import DOSHAS
import requests

st.set_page_config(page_title="Charaka Vaidya · Dosha Quiz", page_icon="🧘", layout="wide")
st.markdown(CHARAKA_CSS, unsafe_allow_html=True)
render_sidebar()
st.markdown(LOGO_HTML, unsafe_allow_html=True)
st.markdown("## 🧘 Prakriti Assessment — Discover Your Dosha")
st.caption("Answer honestly based on your lifelong tendencies, not temporary states.")

QUIZ = [
    {"id": 1, "question": "My body frame is:",
     "options": {"vata": "Thin, light, difficult to gain weight",
                  "pitta": "Medium, muscular, moderate build",
                  "kapha": "Large, solid, tendency to gain weight"}},
    {"id": 2, "question": "My skin is typically:",
     "options": {"vata": "Dry, rough, or chapped",
                  "pitta": "Warm, reddish, prone to rashes",
                  "kapha": "Smooth, oily, thick"}},
    {"id": 3, "question": "My digestion is:",
     "options": {"vata": "Irregular — sometimes great, sometimes poor",
                  "pitta": "Strong — I get irritable when I miss a meal",
                  "kapha": "Slow but steady — rarely starving"}},
    {"id": 4, "question": "Under stress, I tend to:",
     "options": {"vata": "Become anxious or worried",
                  "pitta": "Become irritable or angry",
                  "kapha": "Withdraw and become quiet"}},
    {"id": 5, "question": "My sleep pattern is:",
     "options": {"vata": "Light, interrupted, difficulty falling asleep",
                  "pitta": "Moderate — wake up if too hot or stressed",
                  "kapha": "Deep and long — hard to wake up"}},
    {"id": 6, "question": "My memory and learning style:",
     "options": {"vata": "Quick to learn, quick to forget",
                  "pitta": "Sharp, analytical, good retention",
                  "kapha": "Slow to learn, but never forgets"}},
    {"id": 7, "question": "My energy level through the day:",
     "options": {"vata": "Variable — bursts of energy followed by fatigue",
                  "pitta": "Consistent and focused",
                  "kapha": "Steady but slow to start"}},
    {"id": 8, "question": "My natural temperament is:",
     "options": {"vata": "Creative, enthusiastic, changeable",
                  "pitta": "Ambitious, organized, determined",
                  "kapha": "Calm, patient, nurturing"}},
]

answers = {}
with st.form("dosha_quiz"):
    for q in QUIZ:
        st.markdown(f"**{q['id']}. {q['question']}**")
        options = q["options"]
        choice = st.radio(
            label=f"q{q['id']}",
            options=list(options.keys()),
            format_func=lambda k, opts=options: opts[k],
            horizontal=False,
            key=f"dosha_q{q['id']}",
            label_visibility="collapsed"
        )
        answers[q["id"]] = choice
        st.markdown("")

    submitted = st.form_submit_button("🌿 Reveal My Prakriti", use_container_width=True)

if submitted:
    scores = {"vata": 0, "pitta": 0, "kapha": 0}
    for qid, ans in answers.items():
        scores[ans] += 1

    total     = sum(scores.values())
    primary   = max(scores, key=scores.get)
    remaining = {k: v for k, v in scores.items() if k != primary}
    secondary = max(remaining, key=remaining.get)
    pct       = {k: round(v / total * 100, 1) for k, v in scores.items()}

    st.markdown("---")
    st.markdown("## 🎯 Your Prakriti Result")

    c1, c2, c3 = st.columns(3)
    for col, (dosha, info) in zip([c1, c2, c3], DOSHAS.items()):
        with col:
            st.markdown(f"""
<div class="dosha-card">
    <h2>{info['emoji']}</h2>
    <h3>{info['name']}</h3>
    <h1 style="color:#8B4513">{pct[dosha]}%</h1>
</div>""", unsafe_allow_html=True)

    st.success(f"🌟 **Primary Dosha: {primary.upper()} {DOSHAS[primary]['emoji']}** | Secondary: {secondary.capitalize()}")
    st.info(f"**{DOSHAS[primary]['name']}** — {DOSHAS[primary]['analogy']}")
    st.markdown("**Typical Traits:**")
    for trait in DOSHAS[primary]["traits"]:
        st.markdown(f"• {trait}")
    st.warning("⚠️ This is a simplified self-assessment. For a proper Prakriti analysis, consult a qualified Ayurvedic practitioner.")
