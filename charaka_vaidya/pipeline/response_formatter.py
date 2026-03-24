
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
    if intent == "multi_symptom" or "[DOSHA_DATA:" in raw_text or "Dosha Imbalance Summary" in raw_text:
        result["dosha_analysis"] = extract_dosha_classification(raw_text)
        # Strip the hidden DOSHA_DATA block from user-facing text
        result["text"] = re.sub(r'\n?---?\n?\[DOSHA_DATA:.*?\]\s*\n?---?\n?', '', result["text"], flags=re.DOTALL).strip()
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

    # 1. New Hidden Metadata Format: [DOSHA_DATA: Vata=Low, Pitta=High, Kapha=Low, Primary=Pitta]
    meta_match = re.search(r'\[DOSHA_DATA:\s*Vata=(High|Medium|Low),\s*Pitta=(High|Medium|Low),\s*Kapha=(High|Medium|Low),\s*Primary=(Vata|Pitta|Kapha)\]', response_text, re.IGNORECASE)
    if meta_match:
        result["vata"] = meta_match.group(1).strip().capitalize()
        result["pitta"] = meta_match.group(2).strip().capitalize()
        result["kapha"] = meta_match.group(3).strip().capitalize()
        result["dominant_dosha"] = meta_match.group(4).strip().capitalize()

    # 2. Extract per-symptom classifications: "**[Symptom]** → Dosha: **[Dosha]**"
    symptom_patterns = [
        r'\*\*(.+?)\*\*\s*[→\-:]+\s*(?:Dosha:?\s*)?(?:\*\*)?(Vata|Pitta|Kapha)(?:\*\*)?',
        r'-\s*(.+?)\s*[:]\s*(?:\*\*)?(Vata|Pitta|Kapha)(?:\*\*)?'
    ]
    
    for pattern in symptom_patterns:
        for match in re.finditer(pattern, response_text, re.IGNORECASE):
            symptom = match.group(1).strip()
            # CRITICAL: Filter out metadata and header-like strings
            if (symptom.lower() not in ["symptom", "dosha", "involvement", "primary imbalance", "vat", "pitta", "kapha"] 
                and "[DOSHA_DATA" not in symptom):
                result["per_symptom"].append({
                    "symptom": symptom,
                    "dosha": match.group(2).strip().capitalize(),
                })

    # 3. Fallback for legacy format / failed metadata instruction
    if result["dominant_dosha"] == "Unknown":
        for dosha in ["Vata", "Pitta", "Kapha"]:
            table_match = re.search(rf'\|\s*{dosha}\s*\|\s*(High|Medium|Low)\s*\|', response_text, re.IGNORECASE)
            if table_match:
                result[dosha.lower()] = table_match.group(1).strip().capitalize()
            else:
                list_match = re.search(rf'-\s*{dosha}\s*[:]\s*(High|Medium|Low)', response_text, re.IGNORECASE)
                if list_match:
                    result[dosha.lower()] = list_match.group(1).strip().capitalize()

        dom_patterns = [r'Primary Imbalance[:\*\s]*(Vata|Pitta|Kapha)', r'Dominant Dosha[:\*\s]*(Vata|Pitta|Kapha)']
        for pattern in dom_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                result["dominant_dosha"] = match.group(1).strip().capitalize()
                break

    if result["dominant_dosha"] == "Unknown" and result["per_symptom"]:
        from collections import Counter
        dosha_counts = Counter(s["dosha"] for s in result["per_symptom"])
        if dosha_counts:
            result["dominant_dosha"] = dosha_counts.most_common(1)[0][0]

    return result

