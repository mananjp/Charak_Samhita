import os
from dotenv import load_dotenv

_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_env_path = os.path.join(_base_dir, ".env")
load_dotenv(_env_path)

class Config:
    # ── Groq LLM (only provider) ──────────────────────────────────────────────
    GROQ_API_KEY  = os.getenv("GROQ_API_KEY", "")
    LLM_MODEL     = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
    # Other solid Groq models: "mixtral-8x7b-32768", "gemma2-9b-it", "llama-3.1-8b-instant"

    # ── Embeddings (HuggingFace, free + local, no API key needed) ────────────
    EMBED_MODEL        = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma_db")
    COLLECTION_NAME    = "charaka_samhita"

    # ── RAG settings ──────────────────────────────────────────────────────────
    CHUNK_SIZE    = int(os.getenv("CHUNK_SIZE", 512))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 64))
    TOP_K         = int(os.getenv("TOP_K", 5))
    PDF_PATH      = os.getenv("PDF_PATH", "./data/charaka_samhita.pdf")

    # ── API server ────────────────────────────────────────────────────────────
    API_HOST      = os.getenv("API_HOST", "0.0.0.0")
    API_PORT      = int(os.getenv("API_PORT", 8000))
    FRONTEND_URL  = os.getenv("FRONTEND_URL", "http://localhost:8501")

    # ── App meta ──────────────────────────────────────────────────────────────
    APP_NAME      = "Charaka Vaidya"
    APP_VERSION   = "1.0.0"
    DEBUG         = os.getenv("DEBUG", "false").lower() == "true"

config = Config()
