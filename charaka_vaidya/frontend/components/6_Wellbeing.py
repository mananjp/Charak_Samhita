import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
from datetime import date, timedelta
from frontend.components.sidebar import render_sidebar
from frontend.styles.theme import inject_theme
from core.i18n import t

st.set_page_config(page_title="Well-Being Tracker", page_icon="💚", layout="centered")
inject_theme()
render_sidebar()

st.title(f"💚 {t('wellbeing_title')}")
st.caption(t("disclaimer"))

if "wellbeing_log" not in st.session_state:
    st.session_state["wellbeing_log"] = []

# ── Daily Check-In ────────────────────────────────────────────────────────────
st.subheader("📋 " + t("wellbeing_title"))
today = date.today().isoformat()
already_checked = any(e["date"] == today for e in st.session_state["wellbeing_log"])

if already_checked:
    st.success("✅ You have already checked in today!")
else:
    with st.form("wellbeing_form"):
        mood = st.slider(t("wellbeing_q1"), 1, 5, 3,
            format="%d",
            help="1 = Very poor  |  3 = Okay  |  5 = Great")
        medicated = st.radio(t("wellbeing_q2"), ["Yes", "No"], horizontal=True, index=1)
        symptoms  = st.text_input(t("wellbeing_q3"), placeholder="e.g. mild headache, fatigue")
        submitted = st.form_submit_button(t("wellbeing_submit"))
        if submitted:
            st.session_state["wellbeing_log"].append({
                "date":      today,
                "mood":      mood,
                "medicated": medicated,
                "symptoms":  symptoms,
            })
            st.success(t("wellbeing_saved"))
            st.rerun()

# ── Weekly Trend ──────────────────────────────────────────────────────────────
if st.session_state["wellbeing_log"]:
    st.subheader(t("wellbeing_history"))
    last7 = [e for e in st.session_state["wellbeing_log"]
             if e["date"] >= (date.today() - timedelta(days=7)).isoformat()]
    if last7:
        import pandas as pd
        df = pd.DataFrame(last7).set_index("date")
        st.line_chart(df["mood"], height=200)
        with st.expander("📋 Log entries"):
            st.dataframe(df[["mood","medicated","symptoms"]], use_container_width=True)
    else:
        st.info("No check-ins in the last 7 days yet.")

# ── Privacy Notice ────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("🔒 All data is stored only in your browser session and is cleared when you close the tab. "
           "Nothing is sent to any server.")
