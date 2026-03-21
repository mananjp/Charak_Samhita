
import streamlit as st
import sys, os, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from frontend.styles.theme import CHARAKA_CSS, LOGO_HTML
from frontend.components.sidebar import render_sidebar
import requests

st.set_page_config(page_title="Charaka Vaidya · Herbs", page_icon="🌱", layout="wide")
st.markdown(CHARAKA_CSS, unsafe_allow_html=True)
render_sidebar()
st.markdown(LOGO_HTML, unsafe_allow_html=True)
st.markdown("## 🌱 Ayurvedic Herb Glossary")
st.caption("Explore herbs referenced in the Charaka Samhita with traditional uses and modern research.")

KNOWN_HERBS = [
    "Ashwagandha", "Triphala", "Tulsi", "Neem", "Brahmi", "Shatavari",
    "Giloy (Guduchi)", "Amla (Amalaki)", "Haritaki", "Bibhitaki",
    "Turmeric (Haridra)", "Ginger (Shunti)", "Cumin (Jiraka)",
    "Licorice (Yashtimadhu)", "Shankhapushpi", "Vidari", "Punarnava"
]

herbs_db_path = "./data/herbs_db.json"
if os.path.exists(herbs_db_path):
    with open(herbs_db_path) as f:
        herbs_db = json.load(f)
else:
    herbs_db = {}

col1, col2 = st.columns([2, 1])
with col1:
    search = st.text_input("🔍 Search herb", placeholder="e.g. Ashwagandha")
with col2:
    selected = st.selectbox("Or choose from list", ["— select —"] + KNOWN_HERBS)

herb_query = search.strip() or (selected if selected != "— select —" else "")

if herb_query:
    st.markdown(f"### 🌿 {herb_query}")
    herb_key = herb_query.lower().split("(")[0].strip()

    if herb_key in herbs_db:
        data = herbs_db[herb_key]
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**📚 Reference:** {data.get('reference', 'N/A')}")
            st.markdown(f"**👅 Rasa (Taste):** {data.get('rasa', 'N/A')}")
            st.markdown(f"**🌡️ Virya (Potency):** {data.get('virya', 'N/A')}")
            st.markdown(f"**🔄 Vipaka:** {data.get('vipaka', 'N/A')}")
        with c2:
            st.markdown(f"**✨ Guna (Quality):** {data.get('guna', 'N/A')}")
        st.markdown("**📜 Traditional Uses:**")
        st.info(data.get("traditional_uses", "N/A"))
        st.markdown("**🔬 Modern Research:**")
        st.success(data.get("modern_research", "N/A"))
        st.markdown("**💊 How to Use:**")
        st.markdown(data.get("how_to_use", "N/A"))
        st.warning(f"⚠️ **Avoid if:** {data.get('contraindications', 'N/A')}")
    else:
        st.info("🔎 Fetching from Charaka Samhita RAG system...")
        API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")
        try:
            resp = requests.get(f"{API_BASE}/herb/{herb_key}", timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                st.markdown(data.get("profile", "No data found."))
        except Exception as e:
            st.error(f"Could not fetch herb data: {e}")
            st.markdown("*Please ensure the FastAPI backend is running.*")

st.markdown("---")
st.markdown("### 📋 All Known Herbs")
cols = st.columns(4)
for i, herb in enumerate(KNOWN_HERBS):
    with cols[i % 4]:
        if st.button(herb, key=f"herb_btn_{i}", use_container_width=True):
            st.session_state["herb_search"] = herb
            st.rerun()
