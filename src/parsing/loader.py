import re
from pypdf import PdfReader
from docx import Document

_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


def fix_joined_email(text):
    """Some PDFs glue the last word of the name to the email. Put the space back."""
    def fix(m):
        email = m.group(0)
        local, domain = email.split("@", 1)
        if "." in local and local[0].isupper():
            head, tail = local.rsplit(".", 1)
            if len(head) > len(tail) and head.lower().startswith(tail.lower()):
                n = len(tail)
                return local[:n] + " " + local[n:] + "@" + domain
        return email
    return _EMAIL.sub(fix, text)


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
        raise ValueError("No readable text found. Please upload a PDF with selectable text, not a scanned image.")
    return fix_joined_email(text)