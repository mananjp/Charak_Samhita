"""
One-time script to index the Charaka Samhita PDF into ChromaDB.

Usage:
    python scripts/ingest.py
    python scripts/ingest.py --pdf /custom/path/charaka.pdf
"""
import argparse, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag.document_loader import load_and_chunk_pdf, save_chunks_manifest
from rag.embedder import build_vector_store
from utils.logger import get_logger

logger = get_logger("ingest")

def main(pdf_path: str = None):
    print("\n🌿 Charaka Vaidya — Ingestion Pipeline")
    print("=" * 45)

    print("\n📄 Step 1: Loading & chunking PDF...")
    chunks = load_and_chunk_pdf(pdf_path)
    print(f"   ✅ {len(chunks)} chunks created")

    print("\n📋 Step 2: Saving chunk manifest...")
    save_chunks_manifest(chunks)
    print("   ✅ Saved to data/chunks_manifest.json")

    print(f"\n🔢 Step 3: Building embeddings (HuggingFace) + ChromaDB...")
    print("   ⏳ First run downloads ~90MB model — please wait...")
    store = build_vector_store(chunks)
    print("   ✅ Vector store built and saved")

    print("\n🔍 Step 4: Testing retrieval...")
    results = store.similarity_search("Agni digestive fire imbalance", k=2)
    for r in results:
        sthana = r.metadata.get("sthana", "?")
        preview = r.page_content[:80].replace("\n", " ")
        print(f"   [{sthana}] {preview}...")

    print("\n" + "=" * 45)
    print("✅ Ingestion complete!")
    print("\nNow run:")
    print("  Terminal 1: uvicorn api.main:app --reload --port 8000")
    print("  Terminal 2: streamlit run app.py")
    print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=str, default=None, help="Path to Charaka Samhita PDF")
    args = parser.parse_args()
    main(args.pdf)
