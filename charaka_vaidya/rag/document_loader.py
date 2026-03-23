from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from charaka_vaidya.core.config import config
from charaka_vaidya.utils.logger import get_logger
import re, json

logger = get_logger(__name__)

STHANA_PATTERNS = {
    "Sutrasthana":    r"sutra\s*sthana|sutrasthana",
    "Nidanasthana":   r"nidana\s*sthana|nidanasthana",
    "Vimanasthana":   r"vimana\s*sthana|vimanasthana",
    "Sharirasthana":  r"sharira\s*sthana|sharirasthana",
    "Indriyasthana":  r"indriya\s*sthana|indriyasthana",
    "Chikitsasthana": r"chikitsa\s*sthana|chikitsasthana",
    "Kalpasthana":    r"kalpa\s*sthana|kalpasthana",
    "Siddhisthana":   r"siddhi\s*sthana|siddhisthana",
}

TOPIC_TAGS = {
    "diet":         ["ahara", "food", "eating", "meal", "diet", "nutrition"],
    "digestion":    ["agni", "digest", "ama", "bowel", "stomach", "gastric"],
    "sleep":        ["nidra", "sleep", "insomnia", "rest"],
    "herbs":        ["herb", "plant", "churna", "rasayana", "dravya", "aushadha"],
    "dosha":        ["vata", "pitta", "kapha", "dosha", "prakriti", "constitution"],
    "detox":        ["panchakarma", "vamana", "virechana", "basti", "nasya"],
    "mind":         ["manas", "mind", "mental", "stress", "anxiety", "emotion"],
    "lifestyle":    ["dinacharya", "ritucharya", "routine", "daily", "seasonal"],
}

def detect_sthana(text: str) -> str:
    text_lower = text.lower()
    for sthana, pattern in STHANA_PATTERNS.items():
        if re.search(pattern, text_lower):
            return sthana
    return "Unknown"

def detect_adhyaya(text: str) -> str:
    match = re.search(r"chapter\s*(\d+)|adhyaya\s*(\d+)", text.lower())
    return match.group(1) or match.group(2) if match else "Unknown"

def detect_topic_tags(text: str) -> list:
    text_lower = text.lower()
    tags = []
    for tag, keywords in TOPIC_TAGS.items():
        if any(kw in text_lower for kw in keywords):
            tags.append(tag)
    return tags or ["general"]

def load_and_chunk_pdf(pdf_path: str = None) -> list:
    path = pdf_path or config.PDF_PATH
    logger.info(f"Loading PDF: {path}")
    loader = PyPDFLoader(path)
    raw_pages = loader.load()
    logger.info(f"Loaded {len(raw_pages)} pages.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " "],
    )
    chunks = splitter.split_documents(raw_pages)
    logger.info(f"Split into {len(chunks)} chunks.")

    for i, chunk in enumerate(chunks):
        text = chunk.page_content
        chunk.metadata.update({
            "chunk_id":    i,
            "sthana":      detect_sthana(text),
            "adhyaya":     detect_adhyaya(text),
            "topic_tags":  detect_topic_tags(text),
            "char_count":  len(text),
        })
    return chunks

def save_chunks_manifest(chunks: list, out_path: str = "./data/chunks_manifest.json"):
    manifest = [{"chunk_id": c.metadata["chunk_id"],
                 "sthana": c.metadata["sthana"],
                 "adhyaya": c.metadata["adhyaya"],
                 "tags": c.metadata["topic_tags"],
                 "preview": c.page_content[:80]} for c in chunks]
    with open(out_path, "w") as f:
        json.dump(manifest, f, indent=2)
    logger.info(f"Manifest saved to {out_path}")
