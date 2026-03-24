
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from charaka_vaidya.api.schemas import ChatRequest, ChatResponse
from charaka_vaidya.pipeline.intent_classifier import classify_intent
from charaka_vaidya.pipeline.safety_filter import check_safety
from charaka_vaidya.pipeline.context_builder import build_context
from charaka_vaidya.pipeline.llm_engine import generate_response
from charaka_vaidya.pipeline.response_formatter import format_response
from charaka_vaidya.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.post("", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    try:
        intent = classify_intent(req.query)
        is_emergency, emergency_msg = check_safety(req.query, intent)
        if is_emergency:
            return ChatResponse(answer=emergency_msg, intent="emergency",
                                sources=[], has_disclaimer=True, is_emergency=True)

        context, sources = build_context(req.query, intent)
        history = [m.dict() for m in req.history]
        raw_response = generate_response(req.query, context, history, intent, response_language=req.language)
        formatted = format_response(raw_response, intent, sources)

        return ChatResponse(
            answer=formatted["text"],
            intent=formatted["intent"],
            sources=formatted["sources"],
            has_disclaimer=formatted["has_disclaimer"],
            is_emergency=False,
        )
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
