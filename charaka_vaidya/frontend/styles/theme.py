
CHARAKA_CSS = """
<style>
    /* ── Base ── */
    .stApp { background-color: #FDF5E6; font-family: "Georgia", serif; color: #3B2A1A !important; }
    .main .block-container { max-width: 900px; padding: 2rem 2rem 5rem; }
    .main * { color: #3B2A1A; }
    .main p, .main span, .main div { color: inherit; }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #8B4513 0%, #6B3410 100%);
        color: #FDF5E6;
    }
    section[data-testid="stSidebar"] * { color: #FDF5E6 !important; }
    section[data-testid="stSidebar"] .stSelectbox label { color: #DAA520 !important; }

    /* ── Chat bubbles ── */
    .user-bubble {
        background: #DAA520; color: #3B2A1A !important;
        border-radius: 18px 18px 4px 18px;
        padding: 12px 18px; margin: 8px 0 8px 20%;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        line-height: 1.6;
    }
    .assistant-bubble {
        background: #FAF0DC; color: #3B2A1A !important;
        border: 1px solid #DAA52050;
        border-radius: 18px 18px 18px 4px;
        padding: 14px 20px; margin: 8px 20% 8px 0;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.08);
        line-height: 1.8;
    }
    .emergency-banner {
        background: #C0392B; color: white !important;
        border-radius: 10px; padding: 16px 20px; margin: 10px 0;
        font-weight: bold; border-left: 6px solid #922B21;
    }
    .source-card {
        background: #FFF8E7; border-left: 4px solid #8B4513;
        padding: 10px 14px; margin: 6px 0; border-radius: 6px;
        font-size: 0.85em; color: #5A3A1A !important;
    }

    /* ── Headings ── */
    h1, h2, h3 { color: #8B4513 !important; font-family: "Georgia", serif; }
    h1 { border-bottom: 2px solid #DAA520; padding-bottom: 8px; }

    /* ── Buttons ── */
    .stButton > button {
        background: #8B4513; color: #FDF5E6 !important; border: none;
        border-radius: 8px; font-family: "Georgia", serif;
        transition: background 0.2s;
    }
    .stButton > button:hover { background: #DAA520; color: #3B2A1A !important; }

    /* ── Input ── */
    .stTextInput > div > div > input, .stTextArea textarea {
        border: 2px solid #DAA52060; border-radius: 10px;
        background: #FFFDF5; font-family: "Georgia", serif;
        color: #3B2A1A !important;
    }

    /* ── Radio & Checkbox Options ── */
    .stRadio label, .stRadio p, .stRadio span, .stRadio div,
    .stCheckbox label, .stCheckbox p, .stCheckbox span, .stCheckbox div {
        color: #3B2A1A !important;
    }

    /* ── Metric cards ── */
    .dosha-card {
        background: #FAF0DC; border-radius: 12px;
        padding: 16px; text-align: center;
        border: 2px solid #DAA520; margin: 8px;
    }

    /* ── Divider ── */
    hr { border-color: #DAA52040; }

    /* ── Tag pills ── */
    .tag-pill {
        display: inline-block; background: #6B8E5A; color: white;
        border-radius: 12px; padding: 2px 10px; font-size: 0.75em;
        margin: 2px;
    }
</style>
"""

LOGO_HTML = """
<div style="text-align:center; padding: 20px 0 10px;">
    <span style="font-size: 3rem;">🌿</span>
    <h1 style="color:#8B4513; font-family:Georgia,serif; margin:0; font-size:2rem;">
        Charaka Vaidya
    </h1>
    <p style="color:#6B8E5A; font-style:italic; margin:4px 0;">
        Ancient Wisdom · Modern Clarity
    </p>
</div>
<hr style="border-color:#DAA52060;">
"""
