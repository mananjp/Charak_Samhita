"""
POST /transcribe — Groq Whisper proxy.
GROQ_API_KEY stays server-side; the browser never sees it.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from groq import Groq
from core.config import config
from utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.post("")
async def transcribe_audio(file: UploadFile = File(...)):
    if not config.GROQ_API_KEY:
        raise HTTPException(status_code=400, detail="GROQ_API_KEY not configured.")
    try:
        audio_bytes = await file.read()
        client = Groq(api_key=config.GROQ_API_KEY)
        response = client.audio.transcriptions.create(
            file=(file.filename or "audio.wav", audio_bytes, file.content_type or "audio/wav"),
            model="whisper-large-v3",
            response_format="verbose_json",
            language=None,
            temperature=0.0,
        )
        detected = getattr(response, "language", "en")
        logger.info(f"Transcription OK | lang={detected} | text={response.text[:60]}")
        return {
            "text":               response.text.strip(),
            "detected_language":  detected,
            "segments":           getattr(response, "segments", []),
        }
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
