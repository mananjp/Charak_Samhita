
import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from frontend.styles.theme import CHARAKA_CSS, LOGO_HTML
from frontend.components.chat_ui import render_message, call_chat_api, init_chat_state
from frontend.components.sidebar import render_sidebar
from frontend.components.source_panel import render_sources
from core.i18n import get_lang, SUPPORTED_LANGUAGES

st.set_page_config(page_title="Charaka Vaidya · Chat", page_icon="🌿", layout="wide")
st.markdown(CHARAKA_CSS, unsafe_allow_html=True)

render_sidebar()
st.markdown(LOGO_HTML, unsafe_allow_html=True)
st.markdown("## 💬 Consult Charaka Vaidya")
st.caption("Ask about symptoms, herbs, doshas, diet, or Ayurvedic lifestyle. Powered by RAG over the Charaka Samhita.")

init_chat_state()

col1, col2 = st.columns([3, 1])
with col2:
    simple_mode = st.toggle("🔤 Simple Language", value=False, help="Adjusts complexity of explanations")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.last_sources = []
        st.rerun()

# ── Display history ──────────────────────────────────────────────────────────
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        render_message(msg["role"], msg["content"])

# ── Source panel (last response) ─────────────────────────────────────────────
if st.session_state.last_sources:
    render_sources(st.session_state.last_sources, key_prefix="chat")

st.markdown("---")

# ── Suggested prompts ────────────────────────────────────────────────────────
st.markdown("**✨ Try asking:**")
example_cols = st.columns(3)
examples = [
    "I have constant bloating and gas after meals",
    "Tell me about Ashwagandha benefits",
    "How should I structure my daily routine?",
    "What is my body type if I feel cold and anxious?",
    "Explain Triphala and how to use it",
    "What foods should I avoid in summer?",
]
for i, ex in enumerate(examples):
    with example_cols[i % 3]:
        if st.button(ex, key=f"ex_{i}", use_container_width=True):
            st.session_state["prefill_query"] = ex

# ── Input form ────────────────────────────────────────────────────────────────
prefill = st.session_state.pop("prefill_query", "")
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area(
        "Your question:",
        value=prefill,
        placeholder="e.g. I've been having trouble sleeping for weeks...",
        height=80,
        key="chat_input",
    )
    submitted = st.form_submit_button("🙏 Ask Vaidya", use_container_width=True)

# ── Translation helper ───────────────────────────────────────────────────────
def translate_answer(text: str, target_lang: str) -> str:
    """Translate the answer to the target language using Groq LLM."""
    if target_lang == "en":
        return text
    lang_name = SUPPORTED_LANGUAGES.get(target_lang, target_lang)
    try:
        from groq import Groq
        from core.config import config
        api_key = st.session_state.get("groq_api_key") or config.GROQ_API_KEY
        if not api_key:
            return text
        client = Groq(api_key=api_key)
        resp = client.chat.completions.create(
            model=st.session_state.get("llm_model", config.LLM_MODEL),
            messages=[
                {"role": "system", "content": f"You are a translator. Translate the following text to {lang_name}. Keep all markdown formatting, emojis, and structure intact. Only translate the text, do not add anything else."},
                {"role": "user", "content": text},
            ],
            temperature=0.3,
            max_tokens=4096,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        st.warning(f"Translation failed: {e}")
        return text

if submitted and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    render_message("user", user_input.strip())

    with st.spinner("🌿 Consulting the Charaka Samhita..."):
        history_for_api = st.session_state.messages[:-1][-6:]
        response = call_chat_api(user_input.strip(), history_for_api, simple_mode)

    answer   = response.get("answer", "")
    sources  = response.get("sources", [])
    is_emerg = response.get("is_emergency", False)

    # Translate if user selected a non-English language
    current_lang = get_lang()
    if current_lang != "en" and answer:
        with st.spinner(f"🌐 Translating to {SUPPORTED_LANGUAGES.get(current_lang, current_lang)}..."):
            answer = translate_answer(answer, current_lang)

    if is_emerg:
        st.markdown(f'<div class="emergency-banner">{answer}</div>', unsafe_allow_html=True)
    else:
        render_message("assistant", answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.last_sources = sources
    st.rerun()
