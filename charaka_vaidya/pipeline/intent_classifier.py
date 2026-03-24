import re
from charaka_vaidya.core.constants import EMERGENCY_KEYWORDS
from charaka_vaidya.utils.logger import get_logger

logger = get_logger(__name__)

HERB_KEYWORDS   = ["herb", "plant", "ashwagandha", "triphala", "tulsi", "neem", "brahmi",
                    "shatavari", "giloy", "amla", "haritaki", "bibhitaki", "turmeric",
                    "ginger", "cumin", "churna", "aushadha", "dravya"]
DOSHA_KEYWORDS  = ["dosha", "vata", "pitta", "kapha", "prakriti", "constitution", "body type",
                    "body nature"]
PHILO_KEYWORDS  = ["how should i eat", "diet", "lifestyle", "routine", "dinacharya", "ritucharya",
                    "ayurvedic philosophy", "yoga", "pranayama", "daily routine", "what is ayurveda"]

# Patterns that indicate a health symptom mention
SYMPTOM_PATTERNS = [r"i have", r"i feel", r"i am suffering", r"my .* hurts",
                    r"pain in", r"problem with", r"suffering from", r"symptoms of",
                    r"i get", r"i can'?t sleep", r"trouble with", r"difficulty"]

def _count_symptom_signals(query: str) -> int:
    """Count how many distinct symptom signals are present in a query."""
    q = query.lower()
    count = 0
    # Count symptom pattern matches
    for p in SYMPTOM_PATTERNS:
        count += len(re.findall(p, q))
    # Count comma-separated or 'and'-joined segments in symptom-like context
    if any(re.search(p, q) for p in SYMPTOM_PATTERNS):
        # commas and " and " between symptom phrases add more signals
        count += q.count(",")
        count += q.count(" and ")
        count += q.count(" also ")
        # Hindi/Gujarati conjunctions
        count += q.count(" aur ")
        count += q.count(" ane ")
        count += q.count("અને")
        count += q.count("और")
    return count

def classify_intent(query: str) -> str:
    q = query.lower()
    if any(kw in q for kw in EMERGENCY_KEYWORDS):
        return "emergency"
    # Check for multi-symptom BEFORE single symptom
    if _count_symptom_signals(q) >= 2:
        return "multi_symptom"
    if any(kw in q for kw in HERB_KEYWORDS):
        return "herb_query"
    if any(kw in q for kw in DOSHA_KEYWORDS):
        return "dosha_constitution"
    if any(kw in q for kw in PHILO_KEYWORDS):
        return "philosophy_lifestyle"
    if any(re.search(p, q) for p in SYMPTOM_PATTERNS):
        return "health_symptom"
    return "general"

