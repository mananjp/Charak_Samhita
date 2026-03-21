
import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from frontend.styles.theme import CHARAKA_CSS, LOGO_HTML
from frontend.components.sidebar import render_sidebar
import requests
from datetime import datetime

st.set_page_config(page_title="Charaka Vaidya · Routine", page_icon="☀️", layout="wide")
st.markdown(CHARAKA_CSS, unsafe_allow_html=True)
render_sidebar()
st.markdown(LOGO_HTML, unsafe_allow_html=True)
st.markdown("## ☀️ Dinacharya & Ritucharya — Daily & Seasonal Routine")
st.caption("Ayurvedic daily routines aligned with nature's rhythms, as described in the Charaka Samhita.")

SEASONS = {"spring": "🌸 Vasanta (Spring)", "summer": "☀️ Grishma (Summer)",
           "monsoon": "🌧️ Varsha (Monsoon)", "autumn": "🍂 Sharad (Autumn)",
           "winter": "❄️ Hemanta/Shishira (Winter)"}

month = datetime.now().month
auto_season = ("spring" if month in [3,4] else "summer" if month in [5,6]
               else "monsoon" if month in [7,8,9] else "autumn" if month in [10,11] else "winter")

selected_season = st.selectbox(
    "Select Season",
    options=list(SEASONS.keys()),
    format_func=lambda k: SEASONS[k],
    index=list(SEASONS.keys()).index(auto_season),
)

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")
try:
    resp = requests.get(f"{API_BASE}/daily-routine?season={selected_season}", timeout=10)
    data = resp.json() if resp.status_code == 200 else {}
except Exception:
    data = {}

if data:
    st.markdown(f"### {SEASONS[selected_season]}")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**⏰ Wake Time:** {data.get('wake', 'N/A')}")
        st.markdown(f"**🏃 Exercise:** {data.get('exercise', 'N/A')}")
        st.markdown(f"**🥗 Diet Focus:** {data.get('diet_focus', 'N/A')}")
    with c2:
        herbs = data.get("herbs", [])
        st.markdown(f"**🌿 Recommended Herbs:** {', '.join(herbs)}")
        avoids = data.get("avoid", [])
        st.markdown("**🚫 Avoid:**")
        for a in avoids:
            st.markdown(f"• {a}")

    st.markdown("---")
    st.markdown("### 📅 Daily Routine (Dinacharya)")
    dinacharya = data.get("dinacharya", [])
    for i, step in enumerate(dinacharya, 1):
        st.markdown(f"**{i}.** {step}")
else:
    st.info("Start the FastAPI backend to load seasonal routine data.")
    st.markdown("### 📅 General Dinacharya (Daily Routine)")
    general = [
        "Wake up at Brahma Muhurta (96 min before sunrise)",
        "Tongue scraping (Jihwa Nirlekhana)",
        "Oil pulling with sesame oil — 5 minutes",
        "Warm water on empty stomach",
        "Abhyanga (self oil massage)",
        "Exercise / Yoga / Pranayama — 30 minutes",
        "Warm bath",
        "Nutritious breakfast after sunrise",
        "Main meal at midday",
        "Short walk after meals",
        "Dinner 2-3 hours before sleep",
        "Sleep by 10 PM",
    ]
    for i, s in enumerate(general, 1):
        st.markdown(f"**{i}.** {s}")

st.markdown("---")
st.caption("⚠️ Educational guidance only. Adjust routines based on your individual Prakriti and current health.")
