
STHANAS = [
    "Sutrasthana", "Nidanasthana", "Vimanasthana", "Sharirasthana",
    "Indriyasthana", "Chikitsasthana", "Kalpasthana", "Siddhisthana"
]

DOSHAS = {
    "vata": {
        "name": "Vata",
        "elements": "Air + Space",
        "analogy": "The body's movement and nervous energy principle, like wind",
        "traits": ["Creative", "Energetic when balanced", "Anxious when imbalanced", "Dry skin", "Light frame"],
        "emoji": "💨"
    },
    "pitta": {
        "name": "Pitta",
        "elements": "Fire + Water",
        "analogy": "The body's transformation and metabolic engine, like fire",
        "traits": ["Sharp intellect", "Strong digestion", "Irritable when imbalanced", "Medium build", "Warm body"],
        "emoji": "🔥"
    },
    "kapha": {
        "name": "Kapha",
        "elements": "Earth + Water",
        "analogy": "The body's structure, stability and lubrication, like earth",
        "traits": ["Calm and grounded", "Strong build", "Sluggish when imbalanced", "Good memory", "Oily skin"],
        "emoji": "🌊"
    }
}

QUERY_INTENTS = ["health_symptom", "herb_query", "philosophy_lifestyle", "dosha_constitution", "emergency", "general"]

EMERGENCY_KEYWORDS = [
    "chest pain", "heart attack", "stroke", "can't breathe", "shortness of breath",
    "suicidal", "want to die", "severe allergy", "anaphylaxis", "unconscious",
    "high fever", "organ failure", "emergency", "ambulance"
]

AYURVEDIC_TERMS = {
    "Agni": "Digestive fire / metabolic strength",
    "Ama": "Undigested metabolic waste / toxin accumulation",
    "Ojas": "Vital essence / immunity force",
    "Prana": "Life force / vital energy",
    "Dinacharya": "Daily routine aligned with natural rhythms",
    "Ritucharya": "Seasonal health regimen",
    "Rasayana": "Rejuvenation therapy",
    "Panchakarma": "Five-fold detoxification procedures",
    "Prakriti": "Individual body constitution",
    "Vikriti": "Current state of imbalance",
    "Srotas": "Body channels / micro-circulatory systems",
    "Dhatu": "Seven body tissues (plasma, blood, muscle, fat, bone, marrow, reproductive)",
}

THEME = {
    "primary":     "#8B4513",   # Terracotta
    "secondary":   "#6B8E5A",   # Sage green
    "background":  "#FDF5E6",   # Cream
    "accent":      "#DAA520",   # Gold
    "text":        "#3B2A1A",   # Dark brown
    "surface":     "#FAF0DC",   # Light cream
    "error":       "#C0392B",
}
