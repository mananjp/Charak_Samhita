
from pydantic import BaseModel, Field
from typing import Optional, List

class ChatMessage(BaseModel):
    role:    str
    content: str

class ChatRequest(BaseModel):
    query:       str = Field(..., min_length=1, max_length=2000)
    history:     List[ChatMessage] = []
    simple_mode: bool = False
    language:    Optional[str] = None  # "English", "Hindi", "Gujarati"

class SourceRef(BaseModel):
    sthana:  str
    adhyaya: str
    preview: str
    score:   float
    tags:    List[str]

class DoshaSymptom(BaseModel):
    symptom: str
    dosha:   str

class DoshaAnalysis(BaseModel):
    dominant_dosha: str = "Unknown"
    vata:           str = "Low"
    pitta:          str = "Low"
    kapha:          str = "Low"
    per_symptom:    List[DoshaSymptom] = []

class ChatResponse(BaseModel):
    answer:         str
    intent:         str
    sources:        List[SourceRef]
    has_disclaimer: bool
    is_emergency:   bool
    dosha_analysis: Optional[DoshaAnalysis] = None

class HerbResponse(BaseModel):
    name:             str
    sanskrit:         str
    hindi:            str
    english:          str
    rasa:             str
    guna:             str
    virya:            str
    vipaka:           str
    traditional_uses: str
    modern_research:  str
    how_to_use:       str
    contraindications: str
    reference:        str

class DoshaQuizAnswer(BaseModel):
    question_id: int
    answer:      str  # "vata" | "pitta" | "kapha"

class DoshaAssessRequest(BaseModel):
    answers: List[DoshaQuizAnswer]

class DoshaAssessResponse(BaseModel):
    primary_dosha:   str
    secondary_dosha: str
    scores:          dict
    description:     str
    recommendations: List[str]

class SamhitaSearchRequest(BaseModel):
    query:   str
    top_k:   int = 5
    sthana:  Optional[str] = None

class ReportRequest(BaseModel):
    messages:       List[ChatMessage]
    dosha_analysis: Optional[DoshaAnalysis] = None
    language:       str = "English"

