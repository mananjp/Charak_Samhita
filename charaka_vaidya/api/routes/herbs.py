
from fastapi import APIRouter, HTTPException
from charaka_vaidya.pipeline.context_builder import build_context
from charaka_vaidya.pipeline.llm_engine import generate_response
import json, os

router = APIRouter()

def load_herbs_db():
    path = "./data/herbs_db.json"
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}

@router.get("/{name}")
def get_herb(name: str):
    herbs_db = load_herbs_db()
    herb_key = name.lower().strip()
    if herb_key in herbs_db:
        return herbs_db[herb_key]
    context, sources = build_context(f"properties uses of herb {name}", intent="herb_query")
    response = generate_response(f"Give full herb profile for {name}", context, intent="herb_query")
    return {"name": name, "generated": True, "profile": response, "sources": sources}

@router.get("")
def list_herbs():
    herbs_db = load_herbs_db()
    return {"herbs": list(herbs_db.keys()), "count": len(herbs_db)}
