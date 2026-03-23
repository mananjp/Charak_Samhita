"""
Text-to-speech using the Web Speech API (SpeechSynthesis).
Injected via st.components.v1.html — no server round-trip needed.
"""
import streamlit as st
import streamlit.components.v1 as stc
import json, re
from core.i18n import t, get_bcp47

def render_speak_button(text: str, key: str = "speak_main"):
    """Render a TTS button that reads `text` aloud in the current language."""
    if not text:
        return
    lang = get_bcp47()
    safe_text = json.dumps(text[:2000])  # cap to avoid huge utterances
    button_label = t("speak_button")

    html = f"""
    <style>
        .speak-btn {{
            background: #6B8E5A; color: white; border: none;
            border-radius: 8px; padding: 8px 18px; cursor: pointer;
            font-size: 14px; font-family: Georgia, serif;
            transition: background 0.2s;
        }}
        .speak-btn:hover {{ background: #8B4513; }}
        .speak-btn:disabled {{ background: #aaa; cursor: not-allowed; }}
    </style>
    <button class="speak-btn" id="speakBtn_{key}" onclick="handleSpeak_{key}()">
        {button_label}
    </button>
    <script>
    var _speaking_{key} = false;
    function handleSpeak_{key}() {{
        var btn = document.getElementById("speakBtn_{key}");
        if (_speaking_{key}) {{
            window.speechSynthesis.cancel();
            _speaking_{key} = false;
            btn.textContent = "{button_label}";
            btn.disabled = false;
            return;
        }}
        if (!window.speechSynthesis) {{
            btn.textContent = "TTS not supported";
            return;
        }}
        window.speechSynthesis.cancel();
        var u = new SpeechSynthesisUtterance({safe_text});
        u.lang = "{lang}";
        u.rate = 0.9;
        u.onstart = function() {{
            _speaking_{key} = true;
            btn.textContent = "⏹️ Stop";
        }};
        u.onend = u.onerror = function() {{
            _speaking_{key} = false;
            btn.textContent = "{button_label}";
        }};
        window.speechSynthesis.speak(u);
    }}
    </script>
    """
    stc.html(html, height=55)
