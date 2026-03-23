"""
Minimal i18n utility for Charaka Vaidya.
Supports en, hi, gu. Falls back to English for any missing key.
"""
import json, os
import streamlit as st

SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "हिंदी",
    "gu": "ગુજરાતી",
}

# BCP-47 language tags for Web Speech API / Whisper
LANG_CODES = {
    "en": "en-IN",
    "hi": "hi-IN",
    "gu": "gu-IN",
}

_cache: dict = {}

def _load(lang: str, namespace: str = "translation") -> dict:
    key = f"{lang}/{namespace}"
    if key not in _cache:
        path = os.path.join(
            os.path.dirname(__file__), "..", "locales", lang, f"{namespace}.json"
        )
        path = os.path.normpath(path)
        try:
            with open(path, encoding="utf-8") as f:
                _cache[key] = json.load(f)
        except FileNotFoundError:
            _cache[key] = {}
    return _cache[key]

def get_lang() -> str:
    """Return current language from session state, default English."""
    return st.session_state.get("lang", "en")

def t(key: str, namespace: str = "translation", **kwargs) -> str:
    """Translate a key in the current language, fallback to English."""
    lang = get_lang()
    data = _load(lang, namespace)
    val = data.get(key)
    if val is None:
        val = _load("en", namespace).get(key, key)
    if kwargs and isinstance(val, str):
        try:
            val = val.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return val

def sdg3(key: str, **kwargs) -> str:
    """Shorthand for SDG3 namespace."""
    return t(key, namespace="sdg3", **kwargs)

def get_bcp47() -> str:
    """Return BCP-47 tag for current language (for TTS / Whisper)."""
    return LANG_CODES.get(get_lang(), "en-IN")
