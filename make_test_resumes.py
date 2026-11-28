import os
from docx import Document
from docx.shared import Pt, Inches
from src.eval_resumes import RESUMES

OUT = "data/resumes_test"
os.makedirs(OUT, exist_ok=True)


def new_doc():
    d = Document()
    for s in d.sections:
        s.left_margin = s.right_margin = Inches(0.8)
        s.top_margin = s.bottom_margin = Inches(0.7)
    d.styles["Normal"].font.name = "Arial"
    d.styles["Normal"].font.size = Pt(10.5)
    return d


def head(container, text):
    p = container.add_paragraph()
    p.add_run(text.upper()).bold = True


def fill(container, r):
    """Write the sections of one resume into a document."""
    if r.get("summary"):
        head(container, "Summary")
        container.add_paragraph(r["summary"])
    head(container, "Skills")
    container.add_paragraph(r["skills_text"] if r.get("skills_text") else ", ".join(r["skills"]))
    if r["experience"]:
        head(container, "Experience")
        for role, company, dates, bullets in r["experience"]:
            p = container.add_paragraph()
            p.add_run(role).bold = True
            p.add_run(f"  |  {company}  |  {dates}")
            for b in bullets:
                container.add_paragraph(b, style="List Bullet")
    if r["projects"]:
        head(container, "Projects")
        for name, tech, bullets in r["projects"]:
            p = container.add_paragraph()
            p.add_run(name).bold = True
            p.add_run(f"  |  {tech}")
            for b in bullets:
                container.add_paragraph(b, style="List Bullet")
    head(container, "Education")
    for degree, school, years in r["education"]:
        p = container.add_paragraph()
        p.add_run(degree).bold = True
        p.add_run(f"  |  {school}  |  {years}")


for r in RESUMES:
    d = new_doc()
    title = d.add_paragraph()
    run = title.add_run(r["name"])
    run.bold = True
    run.font.size = Pt(18)
    d.add_paragraph(f"Email: {r['email']}   Phone: {r['phone']}")
    if r.get("paragraphs_only"):
        for t in r["text"]:
            d.add_paragraph(t)
    elif r.get("table"):
        table = d.add_table(rows=1, cols=2)
        left, right = table.rows[0].cells
        left.paragraphs[0].add_run("SKILLS").bold = True
        left.add_paragraph(", ".join(r["skills"]))
        head(left, "Education")
        for degree, school, years in r["education"]:
            left.add_paragraph(f"{degree}, {school}, {years}")
        right.paragraphs[0].add_run("EXPERIENCE").bold = True
        for role, company, dates, bullets in r["experience"]:
            right.add_paragraph(f"{role} | {company} | {dates}")
            for b in bullets:
                right.add_paragraph(b)
        head(right, "Projects")
        for name, tech, bullets in r["projects"]:
            right.add_paragraph(f"{name} | {tech}")
            for b in bullets:
                right.add_paragraph(b)
    else:
        fill(d, r)
    if r.get("extra_line"):
        d.add_paragraph(r["extra_line"])
    path = f"{OUT}/{r['file']}.docx"
    d.save(path)
    print("created", path, "-", r["layout"])