import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
from frontend.components.sidebar import render_sidebar
from frontend.components.speak_button import render_speak_button
from frontend.components.uhc_widget import render_uhc_widget
from frontend.styles.theme import inject_theme
from core.i18n import t, sdg3

st.set_page_config(page_title="SDG 3 Health", page_icon="🌍", layout="wide")
inject_theme()
render_sidebar()

st.title(f"🌍 {sdg3('page_title')}")
st.info(sdg3("page_subtitle"))
st.warning(f"📊 {sdg3('progress_note')}")

render_uhc_widget()

# ── Voice-activated card search ───────────────────────────────────────────────
st.caption(sdg3("voice_hint"))
search = st.text_input("🔍 Search health topic / बीमारी खोजें / આरोग्ય વિષय શોધો", "")

# ── Health Cards ──────────────────────────────────────────────────────────────
st.subheader(sdg3("section_cards"))
cards = sdg3("cards")

KEYWORD_MAP = {
    "maternal": ["maternal", "mother", "pregnancy", "गर्भ", "माता", "ماँ", "ગર્ભ"],
    "child":    ["child", "baby", "infant", "बच्चा", "शिशु", "બાળ"],
    "infectious": ["malaria", "hiv", "tb", "tuberculosis", "hepatitis", "infectious",
                   "संक्रमण", "ચેપ"],
    "ncd":      ["heart", "diabetes", "cancer", "blood pressure", "hypertension",
                 "हृदय", "मधुमेह", "हार्ट", "હૃદય"],
    "mental_health": ["mental", "anxiety", "depression", "stress", "suicide",
                      "मानसिक", "तनाव", "मन", "માનसिक"],
    "substance": ["tobacco", "alcohol", "drug", "addiction", "तंबाकू", "शराब"],
    "uhc":      ["coverage", "hospital", "free", "subsidy", "healthcare", "स्वास्थ्य"],
    "vaccines": ["vaccine", "vaccination", "immunization", "टीका", "रसीकरण"],
}

def card_matches(card: dict, query: str) -> bool:
    if not query:
        return True
    q = query.lower()
    keywords = KEYWORD_MAP.get(card["key"], [])
    return (
        q in card["title"].lower() or
        q in card["body"].lower() or
        any(q in kw for kw in keywords)
    )

disclaimer = sdg3("disclaimer_card")
learn_more  = sdg3("learn_more")

cols = st.columns(2)
shown = 0
for i, card in enumerate(cards):
    if not card_matches(card, search):
        continue
    with cols[shown % 2]:
        with st.container(border=True):
            st.markdown(f"### {card['emoji']} {card['title']}")
            st.write(card["body"])
            render_speak_button(card["body"], key=f"speak_card_{i}")
            st.markdown(f"[{learn_more}]({card['who_link']})")
            st.caption(f"⚠️ {disclaimer}")
    shown += 1

if shown == 0:
    st.info("No cards matched your search. Try a different keyword.")

# ── SDG 3 Badge ───────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:12px;" aria-label="This project supports UN SDG Goal 3 Good Health and Well Being">
    <a href="https://sdgs.un.org/goals/goal3" target="_blank">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/SDG_icon-EN-13.jpg/200px-SDG_icon-EN-13.jpg"
             width="90" alt="SDG 3 Badge"/>
    </a><br>
    <small>{badge}</small>
</div>
""".format(badge=t("sdg3_badge")), unsafe_allow_html=True)
