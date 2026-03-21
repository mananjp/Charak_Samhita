
import streamlit as st

def render_sources(sources: list, key_prefix: str = "src"):
    if not sources:
        return
    with st.expander(f"📚 Sources from Charaka Samhita ({len(sources)} passages)", expanded=False):
        for i, src in enumerate(sources):
            tags_html = " ".join(
                f'<span class="tag-pill">{t}</span>' for t in src.get("tags", [])
            )
            st.markdown(f"""
<div class="source-card">
    <strong>📖 {src.get("sthana", "?")} · Chapter {src.get("adhyaya", "?")}</strong><br>
    <em style="color:#8B7355;">{src.get("preview", "")}</em><br>
    {tags_html}
    <small style="float:right; color:#AAA;">Relevance: {round(src.get("score", 0)*100, 1)}%</small>
</div>
            """, unsafe_allow_html=True)
