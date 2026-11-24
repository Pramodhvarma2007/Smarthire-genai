import io
import json
import re
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from src.llm import call_llm
from src.generate.prompts import REWRITE_PROMPT

NUM = re.compile(r"\d+(?:\.\d+)?")
HIDE = {"email", "name", "target_role"}


def rewrite_resume(profile, job, fresh=False):
    """The AI rewrites wording only. Facts are kept by the code."""
    prompt = REWRITE_PROMPT.format(
        job_title=job["Job_Title"], level=job["Experience_Level"],
        job_skills=job["Skills_Required"],
        profile_json=profile.model_dump_json(indent=2, exclude=HIDE))
    data, last = None, None
    for attempt in range(2):
        raw = call_llm(prompt, json_mode=True, temperature=0.2,use_cache=(attempt == 0 and not fresh))
        try:
            data = json.loads(raw)
            break
        except json.JSONDecodeError as e:
            last = e
    if not isinstance(data, dict):
        raise ValueError(f"Could not get a valid rewrite: {last}")

    # skills: keep only the student's own skills, and drop none
    wanted = [str(s).strip().lower() for s in data.get("skills", [])]
    own = list(profile.skills)
    ordered = [s for w in wanted for s in own if s.lower() == w]
    skills = list(dict.fromkeys(ordered + own))

    def bullets(items, key, fallback_field):
        given = data.get(key, [])
        result = []
        for i, item in enumerate(items):
            b = []
            if i < len(given) and isinstance(given[i], dict):
                b = [str(x).strip() for x in given[i].get("bullets", []) if str(x).strip()]
            if not b and getattr(item, fallback_field):
                b = [getattr(item, fallback_field)]
            result.append(b)
        return result

    return {"summary": str(data.get("summary", "")).strip(),
            "skills": skills,
            "experience": bullets(profile.experience, "experience", "summary"),
            "projects": bullets(profile.projects, "projects", "description")}


def check_rewrite(profile, job, result):
    """Returns a list of problems. An empty list means it passed."""
    issues = []
    text = " ".join([result["summary"]] +
                    [b for group in result["experience"] + result["projects"] for b in group])
    original = profile.model_dump_json(exclude=HIDE)
    invented = set(NUM.findall(text)) - set(NUM.findall(original))
    if invented:
        issues.append("numbers not in your resume: " + ", ".join(sorted(invented)))
    for s in job["missing"]:
        base = re.sub(r"\(.*?\)", "", s).strip()
        if len(base) > 2 and re.search(rf"(?<!\w){re.escape(base)}(?!\w)", text, re.I):
            issues.append(f"mentions a skill you do not have: {s}")
    if not result["summary"]:
        issues.append("no summary")
    return issues


def build_docx(profile, result):
    """Returns the Word file as bytes. Only plain paragraphs are used."""
    doc = Document()
    for section in doc.sections:
        section.left_margin = section.right_margin = Inches(0.8)
        section.top_margin = section.bottom_margin = Inches(0.7)
    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(10.5)

    def heading(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(text.upper())
        r.bold = True
        r.font.size = Pt(11)

    def line(parts, bold_first=True):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        parts = [x for x in parts if x]
        for i, part in enumerate(parts):
            r = p.add_run(("  |  " if i else "") + part)
            r.bold = bold_first and i == 0

    def bullet_lines(items):
        for b in items:
            p = doc.add_paragraph(b, style="List Bullet")
            p.paragraph_format.space_after = Pt(1)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = title.add_run(profile.name or "Your Name")
    r.bold = True
    r.font.size = Pt(18)
    contact = doc.add_paragraph()
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact.add_run("  |  ".join(x for x in (profile.email, "[add phone number]") if x))

    if result["summary"]:
        heading("Summary")
        doc.add_paragraph(result["summary"])
    if result["skills"] or profile.soft_skills:
        heading("Skills")
        if result["skills"]:
            line(["Technical: " + ", ".join(result["skills"])], bold_first=False)
        if profile.soft_skills:
            line(["Strengths: " + ", ".join(profile.soft_skills)], bold_first=False)
    if profile.experience:
        heading("Experience")
        for e, b in zip(profile.experience, result["experience"]):
            line([e.role, e.company, e.duration])
            bullet_lines(b)
    if profile.projects:
        heading("Projects")
        for pr, b in zip(profile.projects, result["projects"]):
            line([pr.name, ", ".join(pr.tech)])
            bullet_lines(b)
    if profile.education:
        heading("Education")
        for ed in profile.education:
            line([ed.degree, ed.institution, ed.year])

    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()