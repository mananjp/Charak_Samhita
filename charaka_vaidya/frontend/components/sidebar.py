import streamlit as st
import os
from core.constants import DOSHAS, AYURVEDIC_TERMS, STHANAS
from core.config import config

def render_sidebar():
    with st.sidebar:
        st.markdown("## 🌿 Charaka Vaidya")
        st.markdown("*Ancient Wisdom · Modern Clarity*")
        st.markdown("---")


        # ── Model selector ────────────────────────────────────────────────────
        GROQ_MODELS = {
            "llama-3.3-70b-versatile":       "LLaMA 3.3 70B  (best quality)",
            "llama-3.1-8b-instant":  "LLaMA 3.1 8B (fastest)",
            "mixtral-8x7b-32768":    "Mixtral 8x7B (long context)",
            "gemma2-9b-it":          "Gemma 2 9B   (lightweight)",
        }
        model = st.selectbox(
            "Model",
            options=list(GROQ_MODELS.keys()),
            format_func=lambda k: GROQ_MODELS[k],
            index=0,
            key="groq_model_select",
        )
        st.session_state["llm_model"] = model
        os.environ["LLM_MODEL"] = model

        st.markdown("---")

        # ── Navigation ────────────────────────────────────────────────────────
        st.markdown("### 📖 Navigation")
        st.page_link("app.py",                           label="🏠 Home")
        st.page_link("pages/1_Chat.py",          label="💬 Consult Vaidya")
        st.page_link("pages/2_Herb_Glossary.py", label="🌱 Herb Glossary")
        st.page_link("pages/3_Dosha_Quiz.py",    label="🧘 Dosha Quiz")
        st.page_link("pages/4_Daily_Routine.py", label="☀️ Daily Routine")

        st.markdown("---")

        # ── Reference panels ─────────────────────────────────────────────────
        with st.expander("🌬️ Dosha Quick Reference"):
            for key, info in DOSHAS.items():
                st.markdown(f"**{info['emoji']} {info['name']}** — {info['analogy']}")

        with st.expander("📚 Ayurvedic Glossary"):
            for term, meaning in AYURVEDIC_TERMS.items():
                st.markdown(f"**{term}** — {meaning}")

        with st.expander("📕 Charaka Samhita — 8 Books"):
            for s in STHANAS:
                st.markdown(f"• {s}")

        st.markdown("---")
        st.caption("⚠️ Educational use only. Consult a qualified practitioner for medical decisions.")
