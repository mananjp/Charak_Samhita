
import re

def format_response(raw_text: str, intent: str, sources: list) -> dict:
    result = {
        "text":    raw_text,
        "intent":  intent,
        "sources": _format_sources(sources),
        "has_disclaimer": "⚠️" in raw_text,
        "dosha_analysis": None,
    }
    # Extract dosha classification if this is a multi-symptom response
    if intent == "multi_symptom" or "Dosha Imbalance Summary" in raw_text:
        result["dosha_analysis"] = extract_dosha_classification(raw_text)
    return result

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

def extract_dosha_classification(response_text: str) -> dict:
    """Parse the LLM's structured output to extract dosha breakdown."""
    result = {
        "dominant_dosha": "Unknown",
        "vata": "Low",
        "pitta": "Low",
        "kapha": "Low",
        "per_symptom": [],
    }

    # Extract per-symptom classifications: "**[Symptom]** → Dosha: [Dosha]"
    symptom_pattern = r'\*\*(.+?)\*\*\s*[→\-:]+\s*(?:Dosha:?\s*)?(Vata|Pitta|Kapha)'
    for match in re.finditer(symptom_pattern, response_text, re.IGNORECASE):
        result["per_symptom"].append({
            "symptom": match.group(1).strip(),
            "dosha": match.group(2).strip().capitalize(),
        })

    # Extract table-based dosha levels: "| Vata | High/Medium/Low |"
    for dosha in ["vata", "pitta", "kapha"]:
        table_pattern = rf'\|\s*{dosha}\s*\|\s*(High|Medium|Low)\s*\|'
        match = re.search(table_pattern, response_text, re.IGNORECASE)
        if match:
            result[dosha] = match.group(1).strip().capitalize()

    # Extract dominant dosha: "**Primary Imbalance:** [Dosha]"
    dom_pattern = r'Primary Imbalance[:\*\s]*(Vata|Pitta|Kapha)'
    match = re.search(dom_pattern, response_text, re.IGNORECASE)
    if match:
        result["dominant_dosha"] = match.group(1).strip().capitalize()
    elif result["per_symptom"]:
        # Fallback: count most frequent dosha from per-symptom
        from collections import Counter
        dosha_counts = Counter(s["dosha"] for s in result["per_symptom"])
        result["dominant_dosha"] = dosha_counts.most_common(1)[0][0]

    return result

