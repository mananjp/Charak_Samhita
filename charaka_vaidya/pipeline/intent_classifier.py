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

def classify_intent(query: str) -> str:
    q = query.lower()
    if any(kw in q for kw in EMERGENCY_KEYWORDS):
        return "emergency"
    if any(kw in q for kw in HERB_KEYWORDS):
        return "herb_query"
    if any(kw in q for kw in DOSHA_KEYWORDS):
        return "dosha_constitution"
    if any(kw in q for kw in PHILO_KEYWORDS):
        return "philosophy_lifestyle"
    symptom_patterns = [r"i have", r"i feel", r"i am suffering", r"my .* hurts",
                        r"pain in", r"problem with", r"suffering from", r"symptoms of"]
    if any(re.search(p, q) for p in symptom_patterns):
        return "health_symptom"
    return "general"

