
STHANA_WEIGHTS = {
    "Chikitsasthana": 1.0,
    "Sutrasthana":    0.95,
    "Kalpasthana":    0.90,
    "Vimanasthana":   0.85,
    "Nidanasthana":   0.80,
    "Siddhisthana":   0.75,
    "Sharirasthana":  0.70,
    "Indriyasthana":  0.65,
    "Unknown":        0.50,
}

def rerank(chunks: list, query: str, intent: str = "health_symptom") -> list:
    if intent == "herb_query":
        for c in chunks:
            if "kalpasthana" in c.get("sthana", "").lower():
                c["score"] *= 1.1
    for c in chunks:
        sthana_weight = STHANA_WEIGHTS.get(c.get("sthana", "Unknown"), 0.5)
        c["final_score"] = c["score"] * sthana_weight
    return sorted(chunks, key=lambda x: x["final_score"], reverse=True)

def format_context(chunks: list) -> str:
    parts = []
    for i, c in enumerate(chunks, 1):
        ref = f"{c.get('sthana', 'Unknown')}, Chapter {c.get('adhyaya', '?')}"
        parts.append(f"[Source {i} — {ref}]\n{c['content']}")
    return "\n\n---\n\n".join(parts)
