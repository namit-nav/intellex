from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
import html
import re

router = APIRouter()


class ExportRequest(BaseModel):
    content: str


@router.post("/export-pdf")
def export_pdf(req: ExportRequest):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    # ---------- STYLES ----------
    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER
    title_style.textColor = colors.HexColor("#0B1C3F")
    title_style.fontSize = 20
    title_style.spaceAfter = 20

    heading_style = styles["Heading2"]
    heading_style.textColor = colors.HexColor("#FF7A00")
    heading_style.fontSize = 14
    heading_style.spaceAfter = 10

    normal_style = styles["Normal"]
    normal_style.fontSize = 10
    normal_style.leading = 14

    story = []

    # ---------- TEXT CLEANING ----------
    # Fix ₹ and weird symbols
    safe_text = req.content.replace("₹", "Rs. ")
    safe_text = html.escape(safe_text)

    # ---------- TITLE ----------
    story.append(Paragraph("Intellex Research Report", title_style))
    story.append(Spacer(1, 20))

    # ---------- CONTENT PROCESSING ----------
    for line in safe_text.split("\n"):

        line = line.strip()

        if not line:
            continue

        line = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", line)
        line = line.replace("##", "").strip()

        if line.lower().startswith(("company", "products", "market", "competitors", "recent", "opportunities", "strategic")):
            story.append(Paragraph(f"<b>{line}</b>", heading_style))
            story.append(Spacer(1, 12))

        elif line.startswith("-"):
            story.append(Paragraph(f"• {line[1:].strip()}", normal_style))
            story.append(Spacer(1, 8))

        else:
            story.append(Paragraph(line, normal_style))
            story.append(Spacer(1, 8))

    # ---------- BUILD PDF ----------
    doc.build(story)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=Intellex_Report.pdf"
        },
    )