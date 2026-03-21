
from fastapi import APIRouter
from api.schemas import DoshaAssessRequest, DoshaAssessResponse
from core.constants import DOSHAS

router = APIRouter()

@router.post("", response_model=DoshaAssessResponse)
async def assess_dosha(req: DoshaAssessRequest):
    scores = {"vata": 0, "pitta": 0, "kapha": 0}
    for ans in req.answers:
        d = ans.answer.lower()
        if d in scores:
            scores[d] += 1
    primary   = max(scores, key=scores.get)
    remaining = {k: v for k, v in scores.items() if k != primary}
    secondary = max(remaining, key=remaining.get)
    total     = sum(scores.values()) or 1
    pct       = {k: round(v / total * 100, 1) for k, v in scores.items()}
    dosha_info = DOSHAS[primary]
    recommendations = [
        f"Follow a {primary}-balancing diet",
        f"Emphasize {dosha_info['elements'].split('+')[0].strip().lower()}-reducing foods",
        "Practice consistent daily routine (Dinacharya)",
        "Consult an Ayurvedic practitioner for personalized guidance",
    ]
    return DoshaAssessResponse(
        primary_dosha=primary.capitalize(),
        secondary_dosha=secondary.capitalize(),
        scores=pct,
        description=dosha_info["analogy"],
        recommendations=recommendations,
    )
