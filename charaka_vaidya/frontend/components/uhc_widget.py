"""
UHC Awareness Widget — persistent dismissible banner.
Shows emergency number and health portal link based on user country.
Defaults to India (IN) since the app is India-focused.
"""
import streamlit as st
from core.constants import UHC_DATA
from core.i18n import t

def render_uhc_widget(default_country: str = "IN"):
    """Renders the UHC awareness banner unless user has dismissed it."""
    if st.session_state.get("uhc_dismissed", False):
        return

    data = UHC_DATA.get(default_country, UHC_DATA["DEFAULT"])

    st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #1a6b3a, #2e8b57);
    color: white; border-radius: 12px;
    padding: 14px 20px; margin: 12px 0;
    border-left: 6px solid #DAA520;
    display: flex; justify-content: space-between; align-items: center;
">
    <div>
        <strong>{data["flag"]} {t("uhc_title")}</strong><br>
        <small>{t("uhc_subtitle")}</small><br>
        <span style="font-size:1.1em;">
            📞 <strong>{t("uhc_emergency")}:</strong> {data["emergency"]} &nbsp;|&nbsp;
            <a href="{data["health_link"]}" target="_blank"
               style="color:#DAA520;">🏥 {data["country"]} Health Portal</a>
        </span>
    </div>
</div>
    """, unsafe_allow_html=True)

    if st.button(f"✕ {t('uhc_dismiss')}", key="uhc_dismiss_btn"):
        st.session_state["uhc_dismissed"] = True
        st.rerun()
