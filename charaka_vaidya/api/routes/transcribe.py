"""
POST /transcribe — Groq Whisper proxy.
GROQ_API_KEY stays server-side; the browser never sees it.
Supports all languages that Groq Whisper supports (95+ languages).
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from groq import Groq
from charaka_vaidya.core.config import config
from charaka_vaidya.utils.logger import get_logger
from typing import Optional

router = APIRouter()
logger = get_logger(__name__)

# Groq Whisper supports 95+ languages - here's the comprehensive mapping
GROQ_LANGUAGE_CODES = {
    # ISO 639-1 codes
    "en": "en", "af": "af", "ar": "ar", "hy": "hy", "az": "az", "be": "be",
    "bs": "bs", "bg": "bg", "ca": "ca", "ceb": "ceb", "zh": "zh", "zh-CN": "zh",
    "zh-TW": "zh", "co": "co", "hr": "hr", "cs": "cs", "da": "da", "nl": "nl",
    "et": "et", "fi": "fi", "fr": "fr", "fy": "fy", "gl": "gl", "de": "de",
    "el": "el", "gu": "gu", "ht": "ht", "ha": "ha", "haw": "haw", "he": "he",
    "hi": "hi", "hu": "hu", "is": "is", "ig": "ig", "id": "id", "ga": "ga",
    "it": "it", "ja": "ja", "jw": "jw", "kk": "kk", "km": "km", "rw": "rw",
    "ko": "ko", "ku": "ku", "ky": "ky", "lo": "lo", "la": "la", "lv": "lv",
    "lt": "lt", "lb": "lb", "mk": "mk", "mg": "mg", "ms": "ms", "ml": "ml",
    "mt": "mt", "mi": "mi", "mr": "mr", "mn": "mn", "my": "my", "ne": "ne",
    "no": "no", "or": "or", "ps": "ps", "fa": "fa", "pl": "pl", "pt": "pt",
    "pa": "pa", "ro": "ro", "ru": "ru", "sm": "sm", "sn": "sn", "sd": "sd",
    "si": "si", "sk": "sk", "sl": "sl", "so": "so", "es": "es", "su": "su",
    "sw": "sw", "sv": "sv", "tg": "tg", "ta": "ta", "te": "te", "th": "th",
    "tr": "tr", "tk": "tk", "uk": "uk", "ur": "ur", "ug": "ug", "uz": "uz",
    "vi": "vi", "cy": "cy", "xh": "xh", "yi": "yi", "yo": "yo", "zu": "zu",
}

@router.post("")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: Optional[str] = Query(None, description="ISO 639-1 language code (e.g., 'hi', 'gu', 'en'). Auto-detect if None.")
):
    """Transcribe audio using Groq Whisper. Supports 95+ languages worldwide.
    
    Args:
        file: Audio file (WAV, MP3, OGG, etc.)
        language: Optional language code for explicit language. None = auto-detect
    
    Returns:
        - text: Transcribed text
        - detected_language: Language code detected by Whisper
        - language_name: Full language name
        - segments: Detailed transcription segments
    """
    if not config.GROQ_API_KEY:
        raise HTTPException(status_code=400, detail="GROQ_API_KEY not configured.")
    try:
        audio_bytes = await file.read()
        logger.info(f"📥 Audio received: {len(audio_bytes)} bytes, type: {file.content_type}, filename: {file.filename}")
        logger.info(f"   Requested language: {language or 'auto-detect'}")
        
        client = Groq(api_key=config.GROQ_API_KEY)
        
        # Prepare Whisper API call
        whisper_kwargs = {
            "file": (file.filename or "audio.wav", audio_bytes, file.content_type or "audio/wav"),
            "model": "whisper-large-v3",
            "response_format": "verbose_json",
            "temperature": 0.0,
        }
        
        # Add explicit language if specified
        if language:
            lang_lower = language.lower().strip()
            whisper_kwargs["language"] = lang_lower
            logger.info(f"   Using explicit language: {lang_lower}")
        else:
            whisper_kwargs["language"] = None  # Auto-detect
            logger.info(f"   Auto-detecting language...")
        
        response = client.audio.transcriptions.create(**whisper_kwargs)
        
        # Extract detected language
        detected = getattr(response, "language", "en")
        logger.info(f"🎤 Whisper Response:")
        logger.info(f"   language attr: {detected}")
        logger.info(f"   language type: {type(detected)}")
        logger.info(f"   text: {response.text[:100]}")
        logger.info(f"   has segments: {hasattr(response, 'segments')}")
        
        # Normalize to ISO 639-1 code
        language_normalized = str(detected).lower().strip() if detected else "en"
        logger.info(f"✅ Normalized language code: {language_normalized}")
        
        # Get full language name
        language_name = LANGUAGE_NAMES.get(language_normalized, language_normalized.upper())
        
        return {
            "text":               response.text.strip(),
            "detected_language":  language_normalized,
            "language_name":      language_name,
            "segments":           getattr(response, "segments", []),
        }
    except Exception as e:
        logger.error(f"❌ Transcription error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# Comprehensive language names
LANGUAGE_NAMES = {
    "en": "English", "af": "Afrikaans", "ar": "Arabic", "hy": "Armenian",
    "az": "Azerbaijani", "be": "Belarusian", "bs": "Bosnian", "bg": "Bulgarian",
    "ca": "Catalan", "ceb": "Cebuano", "zh": "Chinese", "co": "Corsican",
    "hr": "Croatian", "cs": "Czech", "da": "Danish", "nl": "Dutch",
    "et": "Estonian", "fi": "Finnish", "fr": "French", "fy": "Frisian",
    "gl": "Galician", "de": "German", "el": "Greek", "gu": "Gujarati",
    "ht": "Haitian", "ha": "Hausa", "haw": "Hawaiian", "he": "Hebrew",
    "hi": "Hindi", "hu": "Hungarian", "is": "Icelandic", "ig": "Igbo",
    "id": "Indonesian", "ga": "Irish", "it": "Italian", "ja": "Japanese",
    "jw": "Javanese", "kk": "Kazakh", "km": "Khmer", "rw": "Kinyarwanda",
    "ko": "Korean", "ku": "Kurdish", "ky": "Kyrgyz", "lo": "Lao",
    "la": "Latin", "lv": "Latvian", "lt": "Lithuanian", "lb": "Luxembourgish",
    "mk": "Macedonian", "mg": "Malagasy", "ms": "Malay", "ml": "Malayalam",
    "mt": "Maltese", "mi": "Maori", "mr": "Marathi", "mn": "Mongolian",
    "my": "Burmese", "ne": "Nepali", "no": "Norwegian", "or": "Odia",
    "ps": "Pashto", "fa": "Persian", "pl": "Polish", "pt": "Portuguese",
    "pa": "Punjabi", "ro": "Romanian", "ru": "Russian", "sm": "Samoan",
    "sn": "Shona", "sd": "Sindhi", "si": "Sinhala", "sk": "Slovak",
    "sl": "Slovenian", "so": "Somali", "es": "Spanish", "su": "Sundanese",
    "sw": "Swahili", "sv": "Swedish", "tg": "Tajik", "ta": "Tamil",
    "te": "Telugu", "th": "Thai", "tr": "Turkish", "tk": "Turkmen",
    "uk": "Ukrainian", "ur": "Urdu", "ug": "Uyghur", "uz": "Uzbek",
    "vi": "Vietnamese", "cy": "Welsh", "xh": "Xhosa", "yi": "Yiddish",
    "yo": "Yoruba", "zu": "Zulu",
}
