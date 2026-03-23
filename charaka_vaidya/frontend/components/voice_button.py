"""
Voice input using st.audio_input (Streamlit 1.33+) + Groq Whisper.
GROQ_API_KEY is NEVER sent to the browser — all transcription happens server-side.
"""
import streamlit as st
import os
import io
from core.i18n import t, get_lang, get_bcp47
from utils.logger import get_logger

logger = get_logger(__name__)

def transcribe_audio(audio_bytes: bytes, lang: str = None) -> dict:
    """Call Groq Whisper server-side. Returns {text, detected_language}."""
    from groq import Groq
    api_key = st.session_state.get("groq_api_key") or os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        return {"text": "", "detected_language": "en", "error": "No Groq API key set."}
    try:
        client = Groq(api_key=api_key)
        response = client.audio.transcriptions.create(
            file=("audio.wav", audio_bytes, "audio/wav"),
            model="whisper-large-v3",
            response_format="verbose_json",
            language=None,   # auto-detect language
            temperature=0.0,
        )
        detected = getattr(response, "language", get_lang())
        return {"text": response.text.strip(), "detected_language": detected, "error": None}
    except Exception as e:
        logger.error(f"Whisper transcription error: {e}")
        return {"text": "", "detected_language": "en", "error": str(e)}

def render_voice_input(key: str = "voice_main") -> str | None:
    """
    Renders the voice input widget.
    Returns the transcribed text string if audio was recorded and transcribed,
    otherwise returns None.
    """
    st.markdown(f"**{t('voice_start')}** — record your question, then click Transcribe.")
    audio = st.audio_input(
        label=t("voice_start"),
        key=f"audio_input_{key}",
        label_visibility="collapsed",
    )

    if audio is not None:
        audio_bytes = audio.read()
        with st.spinner(t("voice_transcribing")):
            result = transcribe_audio(audio_bytes)

        if result["error"]:
            st.error(f"⚠️ {result['error']}")
            return None

        text = result["text"]
        detected = result["detected_language"]

        if text:
            st.success(f"🎙️ *{t('voice_detected_lang')}: {detected.upper()}*")
            st.info(f"**Transcribed:** {text}")

            # Auto-switch app language if detected differs from current
            lang_map = {"hindi": "hi", "gujarati": "gu", "english": "en",
                        "hi": "hi", "gu": "gu", "en": "en"}
            mapped = lang_map.get(detected.lower())
            if mapped and mapped != st.session_state.get("lang", "en"):
                if not st.session_state.get("lang_pinned", False):
                    st.session_state["lang"] = mapped
                    st.info(f"🌐 Language auto-switched to: {mapped.upper()}")

            return text
    return None
