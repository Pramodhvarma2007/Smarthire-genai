from pypdf import PdfReader
from docx import Document


def load_resume(path):
    path_lower = path.lower()
    if path_lower.endswith(".pdf"):
        reader = PdfReader(path)
        text = "\n".join(p.extract_text() or "" for p in reader.pages)
    elif path_lower.endswith(".docx"):
        doc = Document(path)
        text = "\n".join(p.text for p in doc.paragraphs)
    else:
        raise ValueError("Only PDF or DOCX files are supported")

    text = text.strip()
    if len(text) < 50:
        raise ValueError("Could not read text from this file")
    return text