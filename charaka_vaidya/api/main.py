
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add parent directory (Charak_Samhita) to path so charaka_vaidya is importable as a package
_api_dir = os.path.dirname(os.path.abspath(__file__))
_charaka_dir = os.path.dirname(_api_dir)
_parent_dir = os.path.dirname(_charaka_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from charaka_vaidya.core.config import config
from charaka_vaidya.api.routes import chat, herbs, dosha, routine, samhita, transcribe, report

app = FastAPI(
    title=config.APP_NAME,
    description="RAG-powered Ayurvedic AI grounded in the Charaka Samhita",
    version=config.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.FRONTEND_URL, "http://localhost:8501", "http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router,    prefix="/chat",         tags=["Chat"])
app.include_router(herbs.router,   prefix="/herb",         tags=["Herbs"])
app.include_router(dosha.router,   prefix="/assess-dosha", tags=["Dosha"])
app.include_router(routine.router, prefix="/daily-routine",tags=["Routine"])
app.include_router(samhita.router, prefix="/search-samhita",tags=["Samhita"])
app.include_router(transcribe.router, prefix="/transcribe", tags=["Transcribe"])
app.include_router(report.router, prefix="/report", tags=["Report"])

@app.get("/health")
def health_check():
    return {"status": "ok", "app": config.APP_NAME, "version": config.APP_VERSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT,
                reload=config.DEBUG)
