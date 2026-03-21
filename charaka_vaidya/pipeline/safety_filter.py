
from core.constants import EMERGENCY_KEYWORDS

EMERGENCY_RESPONSE = """
🚨 **Immediate Medical Attention Required**

What you're describing sounds like it may need **immediate medical attention**.

Please:
- **Call emergency services (112 in India)**
- **Visit the nearest hospital or emergency room right away**
- **Do not rely on Ayurvedic guidance for emergency situations**

> Ayurvedic guidance is not a substitute for emergency care.
"""

def check_safety(query: str, intent: str) -> tuple[bool, str]:
    """Returns (is_emergency: bool, emergency_message: str)"""
    if intent == "emergency":
        return True, EMERGENCY_RESPONSE
    q = query.lower()
    if any(kw in q for kw in EMERGENCY_KEYWORDS):
        return True, EMERGENCY_RESPONSE
    return False, ""
