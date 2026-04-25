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

    # ✨ Custom Styles
    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER
    title_style.textColor = colors.HexColor("#0B1C3F")

    heading_style = styles["Heading2"]
    heading_style.textColor = colors.HexColor("#FF7A00")

    normal_style = styles["Normal"]

    story = []

    safe_text = html.escape(req.content)

    # 👉 Title
    story.append(Paragraph("Intellex Research Report", title_style))
    story.append(Spacer(1, 20))

    # 👉 Format content
    for line in safe_text.split("\n"):
        line = line.strip()
        if not line:
            continue
        
        line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
        
        if line.startswith("##"):
            story.append(Paragraph(line.replace("##", "").strip(), heading_style))
            story.append(Spacer(1, 10))
            
        elif line.startswith("-"):
            story.append(Paragraph(f"• {line[1:].strip()}", normal_style))
        
        else:
            story.append(Paragraph(line, normal_style))
            
        story.append(Spacer(1, 8))

    doc.build(story)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=Intellex_Report.pdf"
        },
    )