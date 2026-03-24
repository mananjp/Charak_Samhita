
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from charaka_vaidya.api.schemas import ReportRequest
from io import BytesIO
from datetime import datetime
import re
import os

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

router = APIRouter()

# ── Font Registration for Multi-language support (Gujarati/Hindi) ──
# We try to find a common Windows font that supports Indic scripts
FONT_REGISTERED = False
try:
    # Nirmala UI is a standard Windows font for Indian languages
    font_path = "C:\\Windows\\Fonts\\Nirmala.ttf"
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('Nirmala', font_path))
        pdfmetrics.registerFont(TTFont('Nirmala-Bold', "C:\\Windows\\Fonts\\NirmalaB.ttf"))
        FONT_REGISTERED = True
    else:
        # Try .ttc if .ttf is not found (sometimes it's a collection)
        font_path_ttc = "C:\\Windows\\Fonts\\Nirmala.ttc"
        if os.path.exists(font_path_ttc):
            pdfmetrics.registerFont(TTFont('Nirmala', font_path_ttc))
            pdfmetrics.registerFont(TTFont('Nirmala-Bold', font_path_ttc))
            FONT_REGISTERED = True
except Exception:
    pass

# Use Nirmala if registered, otherwise fallback to Helvetica
BODY_FONT = "Nirmala" if FONT_REGISTERED else "Helvetica"
BOLD_FONT = "Nirmala-Bold" if FONT_REGISTERED else "Helvetica-Bold"

# ── Dosha color map ──
DOSHA_COLORS = {
    "Vata":  "#6A5ACD",   # Slate blue
    "Pitta": "#C05C44",   # Terra
    "Kapha": "#6B8F6E",   # Sage green
}

def _strip_markdown(text: str) -> str:
    """Strip markdown formatting and hidden metadata for clean PDF text."""
    # First, strip the hidden DOSHA_DATA metadata block
    text = re.sub(r'\[DOSHA_DATA:.*?\]', '', text, flags=re.DOTALL)
    
    # Standard Markdown stripping
    text = re.sub(r'#{1,6}\s?', '', text)
    text = re.sub(r'\*{1,2}(.*?)\*{1,2}', r'\1', text)
    text = re.sub(r'[_~`>]', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'\|[^\n]+\|', '', text)     # strip markdown tables
    text = re.sub(r'---+', '', text)
    text = re.sub(r'```[^`]*```', '', text, flags=re.DOTALL)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

@router.post("/generate")
def generate_report(req: ReportRequest):
    """Generate a branded PDF consultation report."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm, cm
    from reportlab.lib.colors import HexColor, Color, white
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.graphics.shapes import Drawing, Rect

    buf = BytesIO()
    
    # Custom Page Template for Border
    def add_border(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(HexColor("#D4A054")) # Gold border
        canvas.setLineWidth(2)
        canvas.rect(1*cm, 1*cm, A4[0]-2*cm, A4[1]-2*cm)
        
        # Footer
        canvas.setFont(BODY_FONT, 8)
        canvas.setFillColor(HexColor("#8B8B7A"))
        canvas.drawCentredString(A4[0]/2, 0.7*cm, f"Charaka Vaidya - Science of Living | Page {doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=2.5*cm, bottomMargin=2.5*cm,
                            leftMargin=2.5*cm, rightMargin=2.5*cm)

    # ── Color palette ──
    forest  = HexColor("#1E3A34")
    gold    = HexColor("#D4A054")
    parch   = HexColor("#F5F0E8")
    terra   = HexColor("#C05C44")
    muted   = HexColor("#8B8B7A")

    # ── Styles (Using Unicode font if available) ──
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("AppTitle", fontName=BOLD_FONT, fontSize=28,
                               textColor=forest, spaceAfter=18, alignment=TA_CENTER, leading=32))
    styles.add(ParagraphStyle("Tagline", fontName=BODY_FONT, fontSize=11,
                               textColor=gold, spaceAfter=25, alignment=TA_CENTER, italic=True))
    styles.add(ParagraphStyle("Subtitle", fontName=BODY_FONT, fontSize=10,
                               textColor=muted, spaceAfter=20, alignment=TA_RIGHT))
    styles.add(ParagraphStyle("SectionHead", fontName=BOLD_FONT, fontSize=16,
                               textColor=forest, spaceBefore=25, spaceAfter=12,
                               borderPadding=6, backColor=parch))
    styles.add(ParagraphStyle("UserMsg", fontName=BOLD_FONT, fontSize=11,
                               textColor=forest, leftIndent=12, spaceBefore=15))
    styles.add(ParagraphStyle("BotMsg", fontName=BODY_FONT, fontSize=10,
                               textColor=HexColor("#2C3E50"), leftIndent=25, spaceBefore=8,
                               spaceAfter=18, leading=16))
    styles.add(ParagraphStyle("Disclaimer", fontName=BODY_FONT, fontSize=8,
                               textColor=muted, spaceBefore=35, alignment=TA_CENTER, leading=11))
    styles.add(ParagraphStyle("TableHeader", fontName=BOLD_FONT, fontSize=11,
                               textColor=white, alignment=TA_CENTER))
    styles.add(ParagraphStyle("DoshaLabel", fontName=BOLD_FONT, fontSize=12,
                               textColor=forest, spaceBefore=12))

    story = []

    # ── Header ──
    story.append(Paragraph("🌿 Charaka Vaidya", styles["AppTitle"]))
    story.append(Paragraph("Ancient Wisdom for Modern Healing", styles["Tagline"]))
    
    story.append(Paragraph(
        f"<b>Consultation Ref:</b> CV-{datetime.now().strftime('%Y%m%d%H%M')}<br/>"
        f"<b>Date:</b> {datetime.now().strftime('%B %d, %Y')}<br/>"
        f"<b>Language:</b> {req.language}",
        styles["Subtitle"]
    ))
    story.append(HRFlowable(width="100%", thickness=2.5, color=gold, spaceAfter=20))

    # ── Dosha Analysis Section ──
    if req.dosha_analysis:
        da = req.dosha_analysis
        story.append(Paragraph("📊 Dosha Imbalance Summary", styles["SectionHead"]))

        # Summary table
        dosha_data = [
            [Paragraph("Dosha", styles["TableHeader"]), Paragraph("Involvement Level", styles["TableHeader"])],
            ["Vata (Wind & Ether)", da.vata],
            ["Pitta (Fire & Water)", da.pitta],
            ["Kapha (Earth & Water)", da.kapha],
        ]
        t = Table(dosha_data, colWidths=[200, 140])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), forest),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTNAME', (0, 0), (-1, -1), BOLD_FONT),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, muted),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, parch]),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(t)
        story.append(Spacer(1, 15))

        story.append(Paragraph(
            f"<b>Primary Constitution Imbalance:</b> <font color='#C05C44'>{da.dominant_dosha}</font>", 
            styles["DoshaLabel"]
        ))

        # Per-symptom breakdown
        if da.per_symptom:
            story.append(Spacer(1, 15))
            story.append(Paragraph("Symptom-Specific Classification", styles["DoshaLabel"]))
            symptom_data = [
                [Paragraph("Symptom Mentioned", styles["TableHeader"]), Paragraph("Dosha Association", styles["TableHeader"])]
            ]
            for s in da.per_symptom:
                # Ensure no metadata or internal labels leak here
                if s.symptom and "[DOSHA_DATA" not in s.symptom:
                    symptom_data.append([s.symptom, s.dosha])
            
            if len(symptom_data) > 1:
                st = Table(symptom_data, colWidths=[260, 140])
            st.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), gold),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('FONTNAME', (0, 0), (-1, -1), BOLD_FONT),
                ('GRID', (0, 0), (-1, -1), 0.5, muted),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, parch]),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(st)

        story.append(Spacer(1, 20))

    # ── Conversation Transcript ──
    story.append(Paragraph("💬 Consultation Narrative", styles["SectionHead"]))

    for msg in req.messages:
        if msg.role == "user":
            story.append(Paragraph(f"<b>Patient:</b> {msg.content}", styles["UserMsg"]))
        elif msg.role == "assistant":
            clean = _strip_markdown(msg.content)
            # Remove redundant "Symptoms Identified" header if it's already in the top section
            clean = re.sub(r'^Symptoms Identified:\n?', '', clean, flags=re.IGNORECASE)
            
            if len(clean) > 2800:
                clean = clean[:2800] + "\n\n[... response truncated for brevity ...]"
            
            if clean.strip():
                story.append(Paragraph(f"{clean}", styles["BotMsg"]))

    # ── Vaidya's Footer ──
    story.append(Spacer(1, 50))
    story.append(HRFlowable(width="100%", thickness=1, color=muted, spaceAfter=12))
    
    # Branded signature
    sig_data = [
        [Paragraph("<b>Clinically Assisted AI Diagnostics</b><br/>Charaka Vaidya Proprietary System", styles["BotMsg"]), 
         Paragraph("<b>Authenticated By</b><br/>Charaka Samhita Digital Engine", styles["Subtitle"])]
    ]
    sig_table = Table(sig_data, colWidths=[280, 200])
    story.append(sig_table)

    # ── Disclaimer ──
    story.append(Paragraph(
        "<b>LEGAL DISCLAIMER:</b> This document is for educational purposes only. It is generated using Artificial Intelligence "
        "trained on the Charaka Samhita. It should not be treated as a medical prescription. Ayurveda is a delicate science; "
        "please consult a certified Ayurvedic practitioner (BAMS/MD) before starting any regimen.",
        styles["Disclaimer"]
    ))

    # ── Build PDF with Border ──
    doc.build(story, onFirstPage=add_border, onLaterPages=add_border)
    buf.seek(0)

    filename = f"Vaidya_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
