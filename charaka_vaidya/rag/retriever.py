import os
from rag.embedder import load_vector_store
from core.config import config
from utils.logger import get_logger

logger = get_logger(__name__)

_store = None

def get_store():
    global _store
    if _store is None:
        if not os.path.exists(config.CHROMA_PERSIST_DIR):
            raise RuntimeError(
                "Vector store not found. Run: python scripts/ingest.py"
            )
        _store = load_vector_store()
    return _store

def retrieve(query: str, top_k: int = None, filter_sthana: str = None) -> list:
    k = top_k or config.TOP_K
    store = get_store()
    search_kwargs = {"k": k}
    if filter_sthana:
        search_kwargs["filter"] = {"sthana": filter_sthana}
    docs = store.similarity_search_with_score(query, **search_kwargs)
    results = []
    for doc, score in docs:
        results.append({
            "content": doc.page_content,
            "score":   round(float(score), 4),
            "sthana":  doc.metadata.get("sthana", "Unknown"),
            "adhyaya": doc.metadata.get("adhyaya", "Unknown"),
            "tags":    doc.metadata.get("topic_tags", []),
            "page":    doc.metadata.get("page", 0),
        })
    logger.info(f"Retrieved {len(results)} chunks for: '{query[:50]}'")
    return results

def retrieve_by_herb(herb_name: str) -> list:
    return retrieve(f"herb plant {herb_name} Ayurvedic properties uses rasa guna virya", top_k=3)

def retrieve_for_dosha(dosha: str) -> list:
    return retrieve(f"{dosha} dosha characteristics prakriti constitution treatment", top_k=4)
