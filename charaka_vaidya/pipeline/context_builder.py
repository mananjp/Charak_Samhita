
from rag.retriever import retrieve, retrieve_by_herb, retrieve_for_dosha
from rag.reranker import rerank, format_context
from pipeline.intent_classifier import classify_intent
from utils.logger import get_logger

logger = get_logger(__name__)

def build_context(query: str, intent: str = None) -> tuple[str, list]:
    if not intent:
        intent = classify_intent(query)
    if intent == "herb_query":
        herb_name = _extract_herb_name(query)
        raw_chunks = retrieve_by_herb(herb_name)
    elif intent == "dosha_constitution":
        dosha = _extract_dosha(query)
        raw_chunks = retrieve_for_dosha(dosha)
    else:
        raw_chunks = retrieve(query)
    ranked_chunks = rerank(raw_chunks, query, intent)
    context_text  = format_context(ranked_chunks)
    return context_text, ranked_chunks

def _extract_herb_name(query: str) -> str:
    herb_names = ["ashwagandha", "triphala", "tulsi", "neem", "brahmi", "shatavari",
                  "giloy", "amla", "haritaki", "turmeric", "ginger", "cumin", "bibhitaki"]
    q = query.lower()
    for h in herb_names:
        if h in q:
            return h
    return query

def _extract_dosha(query: str) -> str:
    for d in ["vata", "pitta", "kapha"]:
        if d in query.lower():
            return d
    return "vata pitta kapha"
