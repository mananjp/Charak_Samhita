
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from charaka_vaidya.api.schemas import ReportRequest
from io import BytesIO
from datetime import datetime
import re

router = APIRouter()

# ── Dosha color map ──
DOSHA_COLORS = {
    "Vata":  (106, 90, 205),   # Slate blue
    "Pitta": (192, 92, 68),    # Terra
    "Kapha": (107, 143, 110),  # Sage green
}

LEVEL_WIDTHS = {"High": 0.9, "Medium": 0.55, "Low": 0.25}


def _strip_markdown(text: str) -> str:
    """Strip markdown formatting for clean PDF text."""
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
    from reportlab.lib.colors import HexColor, Color
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm,
                            leftMargin=2*cm, rightMargin=2*cm)

    # ── Color palette (matching Chat Theme) ──
    forest  = HexColor("#1E3A34")
    gold    = HexColor("#D4A054")
    parch   = HexColor("#F5F0E8")
    terra   = HexColor("#C05C44")
    muted   = HexColor("#8B8B7A")

    # ── Styles ──
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("AppTitle", fontName="Helvetica-Bold", fontSize=22,
                               textColor=forest, spaceAfter=4))
    styles.add(ParagraphStyle("Subtitle", fontName="Helvetica", fontSize=10,
                               textColor=muted, spaceAfter=16))
    styles.add(ParagraphStyle("SectionHead", fontName="Helvetica-Bold", fontSize=14,
                               textColor=forest, spaceBefore=18, spaceAfter=8))
    styles.add(ParagraphStyle("UserMsg", fontName="Helvetica-Bold", fontSize=10,
                               textColor=forest, leftIndent=8, spaceBefore=10))
    styles.add(ParagraphStyle("BotMsg", fontName="Helvetica", fontSize=10,
                               textColor=HexColor("#333333"), leftIndent=8, spaceBefore=4,
                               spaceAfter=10, leading=14))
    styles.add(ParagraphStyle("Disclaimer", fontName="Helvetica-Oblique", fontSize=8,
                               textColor=muted, spaceBefore=20, alignment=TA_CENTER))
    styles.add(ParagraphStyle("DoshaLabel", fontName="Helvetica-Bold", fontSize=11,
                               textColor=forest))

    story = []

    # ── Header ──
    story.append(Paragraph("🌿 Charaka Vaidya", styles["AppTitle"]))
    story.append(Paragraph(
        f"Ayurvedic Consultation Report | {datetime.now().strftime('%B %d, %Y at %I:%M %p')} | Language: {req.language}",
        styles["Subtitle"]
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=gold, spaceAfter=12))

    # ── Dosha Analysis Section ──
    if req.dosha_analysis:
        da = req.dosha_analysis
        story.append(Paragraph("📊 Dosha Imbalance Analysis", styles["SectionHead"]))

        # Summary table
        dosha_data = [
            ["Dosha", "Involvement", ""],
            ["Vata (Wind)", da.vata, ""],
            ["Pitta (Fire)", da.pitta, ""],
            ["Kapha (Earth)", da.kapha, ""],
        ]
        t = Table(dosha_data, colWidths=[120, 80, 200])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), forest),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#FFFFFF")),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, muted),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [parch, HexColor("#FFFFFF")]),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 8))

        story.append(Paragraph(
            f"<b>Primary Imbalance:</b> {da.dominant_dosha}", styles["DoshaLabel"]
        ))

        # Per-symptom breakdown
        if da.per_symptom:
            story.append(Spacer(1, 8))
            symptom_data = [["Symptom", "Dosha Classification"]]
            for s in da.per_symptom:
                symptom_data.append([s.symptom, s.dosha])
            st = Table(symptom_data, colWidths=[250, 150])
            st.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), gold),
                ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#FFFFFF")),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, muted),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor("#FFFFFF"), parch]),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            story.append(st)

        story.append(Spacer(1, 12))
        story.append(HRFlowable(width="100%", thickness=0.5, color=muted, spaceAfter=8))

    # ── Conversation Transcript ──
    story.append(Paragraph("💬 Consultation Transcript", styles["SectionHead"]))

    for msg in req.messages:
        if msg.role == "user":
            story.append(Paragraph(f"🧑 Patient: {msg.content}", styles["UserMsg"]))
        elif msg.role == "assistant":
            clean = _strip_markdown(msg.content)
            # Truncate very long responses for PDF readability
            if len(clean) > 2000:
                clean = clean[:2000] + "\n\n[... response truncated for PDF ...]"
            story.append(Paragraph(f"🌿 Vaidya: {clean}", styles["BotMsg"]))

    # ── Disclaimer ──
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=muted, spaceAfter=8))
    story.append(Paragraph(
        "⚠️ This report is generated by Charaka Vaidya, an AI-powered educational tool. "
        "It is NOT a substitute for professional medical advice. Always consult a qualified "
        "Ayurvedic practitioner or medical doctor for health decisions.",
        styles["Disclaimer"]
    ))
    story.append(Paragraph(
        f"Aligned with UN SDG 3 — Good Health & Well-Being | Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        styles["Disclaimer"]
    ))

    # ── Build PDF ──
    doc.build(story)
    buf.seek(0)

    filename = f"charaka_consultation_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
