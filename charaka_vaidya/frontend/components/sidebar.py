import streamlit as st
import os
from charaka_vaidya.core.constants import DOSHAS, AYURVEDIC_TERMS, STHANAS
from charaka_vaidya.core.config import config
from charaka_vaidya.core.i18n import SUPPORTED_LANGUAGES, t

def render_sidebar():
    with st.sidebar:
        st.markdown("## 🌿 Charaka Vaidya")
        st.markdown("*Ancient Wisdom · Modern Clarity*")
        st.markdown("---")

        # Initialize session state for language
        if "lang" not in st.session_state:
            st.session_state["lang"] = "en"

        # ── Language selector ─────────────────────────────────────────────────
        def change_language():
            """Callback for language change - updates session state without rerun"""
            selected = st.session_state.lang_select
            if selected != st.session_state.get("lang"):
                st.session_state["lang"] = selected
        
        langs = list(SUPPORTED_LANGUAGES.keys())
        current = st.session_state.get("lang", "en")
        idx = langs.index(current) if current in langs else 0
        
        st.selectbox(
            t("language_label"),
            options=langs,
            format_func=lambda k: SUPPORTED_LANGUAGES[k],
            index=idx,
            key="lang_select",
            on_change=change_language,
        )


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

        # ── Groq API Key (optional if .env is set) ───────────────────────────
        with st.expander("🔑 API Configuration"):
            api_key = st.text_input(
                "Groq API Key",
                value=st.session_state.get("groq_api_key", ""),
                type="password",
                help="Get free key at https://console.groq.com",
                key="groq_key_input",
            )
            if api_key and api_key != st.session_state.get("groq_api_key"):
                st.session_state["groq_api_key"] = api_key
                os.environ["GROQ_API_KEY"] = api_key
                st.success("✅ Groq API key configured!")

        st.markdown("---")

        # ── Navigation ────────────────────────────────────────────────────────
        st.markdown("### 📖 Navigation")
        
        # Home link uses link_button (app.py is not in pages/ directory)
        st.link_button("🏠 Home", url="/", use_container_width=True)
        
        # Page links for pages/ directory
        st.page_link("pages/1_Chat.py",          label="💬 Consult Vaidya")
        st.page_link("pages/2_Herb_Glossary.py", label="🌱 Herb Glossary")
        st.page_link("pages/3_Dosha_Quiz.py",    label="🧘 Dosha Quiz")
        st.page_link("pages/4_Daily_Routine.py", label="☀️ Daily Routine")
        st.page_link("pages/5_SDG3_Health.py",   label="🌍 Health & SDG 3")
        st.page_link("pages/6_Wellbeing.py",      label="💚 Well-Being Tracker")

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
