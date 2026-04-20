from pypdf import PdfReader
import docx


def load_pdf(path):

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text


def load_docx(path):

    doc = docx.Document(path)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def load_txt(path):

    with open(path, "r") as f:
        return f.read()