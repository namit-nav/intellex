from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import html

router = APIRouter()

class ExportRequest(BaseModel):
    content: str


@router.post("/export-pdf")
def export_pdf(req: ExportRequest):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    story = []

    # 🔥 CLEAN TEXT (THIS FIXES YOUR ISSUE)
    safe_text = html.escape(req.content)

    for line in safe_text.split("\n"):
        if line.strip():
            story.append(Paragraph(line, styles["Normal"]))

    try:
        doc.build(story)
    except Exception as e:
        print("PDF ERROR:", str(e))

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=report.pdf"
        },
    )