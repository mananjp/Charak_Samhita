
import re

def format_response(raw_text: str, intent: str, sources: list) -> dict:
    return {
        "text":    raw_text,
        "intent":  intent,
        "sources": _format_sources(sources),
        "has_disclaimer": "⚠️" in raw_text,
    }

def _format_sources(chunks: list) -> list:
    seen, sources = set(), []
    for c in chunks:
        key = f"{c.get('sthana')}-{c.get('adhyaya')}"
        if key not in seen:
            seen.add(key)
            sources.append({
                "sthana":  c.get("sthana", "Unknown"),
                "adhyaya": c.get("adhyaya", "Unknown"),
                "preview": c["content"][:120] + "...",
                "score":   c.get("final_score", c.get("score", 0)),
                "tags":    c.get("tags", []),
            })
    return sources

def extract_layers(response_text: str) -> dict:
    layers = {
        "charaka_says": "",
        "simple_terms": "",
        "modern_science": "",
        "practical": "",
    }
    patterns = {
        "charaka_says":  r"What Charaka Samhita Says[:\*\*]*(.*?)(?=##|\*\*In Simple|$)",
        "simple_terms":  r"In Simple Terms[:\*\*]*(.*?)(?=##|\*\*What Modern|$)",
        "modern_science":r"What Modern Science[:\*\*]*(.*?)(?=##|\*\*What You Can Do|$)",
        "practical":     r"What You Can Do[:\*\*]*(.*?)(?=⚠️|---|\*Would you|$)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
        if match:
            layers[key] = match.group(1).strip()
    return layers
