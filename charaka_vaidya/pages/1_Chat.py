
import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from frontend.styles.theme import CHARAKA_CSS, LOGO_HTML
from frontend.components.chat_ui import render_message, call_chat_api, init_chat_state
from frontend.components.sidebar import render_sidebar
from frontend.components.source_panel import render_sources

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

if submitted and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    render_message("user", user_input.strip())

    with st.spinner("🌿 Consulting the Charaka Samhita..."):
        history_for_api = st.session_state.messages[:-1][-6:]
        response = call_chat_api(user_input.strip(), history_for_api, simple_mode)

    answer   = response.get("answer", "")
    sources  = response.get("sources", [])
    is_emerg = response.get("is_emergency", False)

    if is_emerg:
        st.markdown(f'<div class="emergency-banner">{answer}</div>', unsafe_allow_html=True)
    else:
        render_message("assistant", answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.last_sources = sources
    st.rerun()
