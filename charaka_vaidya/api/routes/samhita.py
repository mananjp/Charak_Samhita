
from fastapi import APIRouter, HTTPException
from api.schemas import SamhitaSearchRequest
from rag.retriever import retrieve
from utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.post("")
async def search_samhita(req: SamhitaSearchRequest):
    try:
        chunks = retrieve(req.query, top_k=req.top_k, filter_sthana=req.sthana)
        return {"query": req.query, "results": chunks, "count": len(chunks)}
    except Exception as e:
        logger.error(f"Samhita search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
