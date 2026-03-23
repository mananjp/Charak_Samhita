
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import config
from api.routes import chat, herbs, dosha, routine, samhita, transcribe

app = FastAPI(
    title=config.APP_NAME,
    description="RAG-powered Ayurvedic AI grounded in the Charaka Samhita",
    version=config.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.FRONTEND_URL, "http://localhost:8501", "*"],
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

@app.get("/health")
def health_check():
    return {"status": "ok", "app": config.APP_NAME, "version": config.APP_VERSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host=config.API_HOST, port=config.API_PORT,
                reload=config.DEBUG)
