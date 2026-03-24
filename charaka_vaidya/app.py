
import streamlit as st
import sys, os

# Add parent directory (Charak_Samhita) to path so charaka_vaidya is importable as a package
_charaka_dir = os.path.abspath(os.path.dirname(__file__))
_parent_dir = os.path.dirname(_charaka_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from charaka_vaidya.frontend.styles.theme import CHARAKA_CSS, LOGO_HTML
from charaka_vaidya.frontend.components.sidebar import render_sidebar

# Initialize session state for language (must be before page_config)
if "lang" not in st.session_state:
    st.session_state["lang"] = "en"

# Ensure this is marked as the home page
st.set_page_config(
    page_title="Charaka Vaidya",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Charaka Vaidya — RAG-powered Ayurvedic AI grounded in the Charaka Samhita."}
)
st.markdown(CHARAKA_CSS, unsafe_allow_html=True)
render_sidebar()
st.markdown(LOGO_HTML, unsafe_allow_html=True)

st.markdown("""
## Welcome to Charaka Vaidya 🌿

> *"The physician who knows the science of Ayurveda has the power to root out all diseases."*
> — Acharya Charaka, Charaka Samhita

Charaka Vaidya is an AI-powered Ayurvedic health guide that bridges **ancient Vedic wisdom** from the
Charaka Samhita with **modern biomedical understanding**, using Retrieval-Augmented Generation (RAG).

---

### 🚀 How to Use
""")

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.markdown("""
<div class="dosha-card">
    <h2>💬</h2>
    <h4>Consult Vaidya</h4>
    <p>Ask about symptoms, herbs, digestion, sleep, stress, and more.</p>
</div>""", unsafe_allow_html=True)
    if st.button("Open Chat →", key="home_chat", use_container_width=True):
        st.switch_page("pages/1_Chat.py")

with col2:
    st.markdown("""
<div class="dosha-card">
    <h2>🌱</h2>
    <h4>Herb Glossary</h4>
    <p>Explore herbs from the Charaka Samhita with uses and modern research.</p>
</div>""", unsafe_allow_html=True)
    if st.button("Open Glossary →", key="home_herb", use_container_width=True):
        st.switch_page("pages/2_Herb_Glossary.py")

with col3:
    st.markdown("""
<div class="dosha-card">
    <h2>🧘</h2>
    <h4>Dosha Quiz</h4>
    <p>Discover your Prakriti (body constitution) with our self-assessment.</p>
</div>""", unsafe_allow_html=True)
    if st.button("Take Quiz →", key="home_quiz", use_container_width=True):
        st.switch_page("pages/3_Dosha_Quiz.py")

with col4:
    st.markdown("""
<div class="dosha-card">
    <h2>☀️</h2>
    <h4>Daily Routine</h4>
    <p>Get seasonal Dinacharya & Ritucharya guidance from the texts.</p>
</div>""", unsafe_allow_html=True)
    if st.button("View Routine →", key="home_routine", use_container_width=True):
        st.switch_page("pages/4_Daily_Routine.py")

with col5:
    st.markdown("""
<div class="dosha-card">
    <h2>🌍</h2>
    <h4>Health & SDG 3</h4>
    <p>Explore UN SDG 3 health topics with curated information cards.</p>
</div>""", unsafe_allow_html=True)
    if st.button("Explore SDG 3 →", key="home_sdg3", use_container_width=True):
        st.switch_page("pages/5_SDG3_Health.py")

with col6:
    st.markdown("""
<div class="dosha-card">
    <h2>💚</h2>
    <h4>Well-Being</h4>
    <p>Track your daily mood, symptoms, and health check-ins.</p>
</div>""", unsafe_allow_html=True)
    if st.button("Track Well-Being →", key="home_wellbeing", use_container_width=True):
        st.switch_page("pages/6_Wellbeing.py")

st.markdown("""
---
### ⚙️ First-Time Setup

**1. Add your Charaka Samhita PDF**
```bash
cp your_charaka_samhita.pdf charaka_vaidya/data/charaka_samhita.pdf
```

**2. Build the vector database**
```bash
python scripts/ingest.py
```

**3. Set your API key in the sidebar (or `.env` file)**

---
⚠️ *Charaka Vaidya is an educational tool. Always consult a qualified Ayurvedic practitioner
or medical doctor for health decisions.*
""")
