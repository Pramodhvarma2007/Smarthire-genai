import re
from src.llm import call_llm
from src.generate.prompts import PLAN_PROMPT_V2

MAX_SKILLS = 6
PROMISE = re.compile(r"\b(salary|guarantee[d]?|lpa)\b|[₹$]", re.I)


def make_plan(my_skills, job, hours=2, prompt=PLAN_PROMPT_V2):
    """my_skills: the student's skills. job: one job from match_jobs()."""
    missing = list(job["missing"])[:MAX_SKILLS]
    if not missing:
        return {"plan": "You already have every skill this job lists. Next step: build one small "
                        "project that uses them all and add it to your resume.",
                "missing": [], "used_ai": False}
    text = call_llm(prompt.format(
        job_title=job["Job_Title"], level=job["Experience_Level"],
        have=", ".join(my_skills) or "none listed",
        missing=", ".join(missing), hours=hours), temperature=0.3)
    return {"plan": text.strip(), "missing": missing, "used_ai": True}


def check_plan(plan, missing):
    """Automatic checks. Returns a list of problems (empty = passed)."""
    issues, low = [], plan.lower()
    for s in missing:
        base = re.sub(r"\(.*?\)", "", s).strip().lower()
        if base and base not in low:
            issues.append(f"skill not covered: {s}")
    for w in range(1, 5):
        if f"week {w}" not in low:
            issues.append(f"week {w} missing")
    if "http" in low or "www." in low:
        issues.append("contains a web link")
    if PROMISE.search(plan):
        issues.append("contains a salary or promise word")
    return issues