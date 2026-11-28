from docx import Document
from src.parsing.loader import load_resume

path = "data/resumes_test/t4_two_column_table.docx"
old = len("\n".join(p.text for p in Document(path).paragraphs).strip())
print("old method reads", old, "characters;", "fixed reader reads", len(load_resume(path)))