import json
import re
from src.search.job_search import search_jobs
from src.llm import call_llm
from src.generate.prompts import EXPLAIN_MATCH_PROMPT


def candidate_skills(profile):
    """Skills from the skills list plus tools used in projects."""
    skills = list(profile.skills)
    for p in profile.projects:
        skills.extend(p.tech)
    seen, result = set(), []
    for s in skills:
        key = s.strip().lower()
        if key and key not in seen:
            seen.add(key)
            result.append(s.strip())
    return result


def make_query(profile):
    """Text used to search. Name and email are left out on purpose."""
    parts = []
    if profile.target_role:
        parts.append(profile.target_role)
    skills = candidate_skills(profile)
    if skills:
        parts.append("Skills: " + ", ".join(skills))
    roles = [e.role for e in profile.experience if e.role]
    if roles:
        parts.append("Experience: " + ", ".join(roles))
    return ". ".join(parts)


def _clean(s):
    return re.sub(r"\(.*?\)", "", s.lower()).strip()


def same_skill(a, b):
    a, b = _clean(a), _clean(b)
    if not a or not b:
        return False
    if a == b:
        return True
    if len(a) <= 2 or len(b) <= 2:
        return False
    pa = rf"(?<!\w){re.escape(a)}(?!\w)"
    pb = rf"(?<!\w){re.escape(b)}(?!\w)"
    return bool(re.search(pa, b) or re.search(pb, a))


def skill_gap(my_skills, job_skills_text):
    job_skills = [s.strip() for s in str(job_skills_text).split(",") if s.strip()]
    matched = [j for j in job_skills if any(same_skill(m, j) for m in my_skills)]
    missing = [j for j in job_skills if j not in matched]
    pct = round(100 * len(matched) / len(job_skills)) if job_skills else 0
    return matched, missing, pct

def match_jobs(profile, top_n=5, pool=15):
    """Search by the full profile AND by the wanted role, then rank."""
    my_skills = candidate_skills(profile)
    role = (profile.target_role or "").strip()

    queries = [make_query(profile)]
    if role:
        queries.append(role)

    seen, results = set(), []
    for q in queries:
        for r in search_jobs(q, top_n=pool):
            key = r.get("Job_ID") or (r["Job_Title"], r["Company"])
            if key not in seen:
                seen.add(key)
                results.append(r)

    role_words = set(re.findall(r"[a-z]+", role.lower()))
    for r in results:
        matched, missing, pct = skill_gap(my_skills, r["Skills_Required"])
        r["matched"], r["missing"], r["skill_match"] = matched, missing, pct
        title_words = set(re.findall(r"[a-z]+", r["Job_Title"].lower()))
        title_hit = len(role_words & title_words) / len(role_words) if role_words else 0
        r["final"] = round(0.25 * r["score"] + 0.35 * pct / 100 + 0.40 * title_hit, 3)
    results.sort(key=lambda r: r["final"], reverse=True)
    return results[:top_n]


def explain_matches(profile, jobs):
    """One call to the AI model explains all jobs."""
    listing = "\n".join(
        f"{i + 1}. {j['Job_Title']} at {j['Company']}. "
        f"Matched: {', '.join(j['matched']) or 'none'}. "
        f"Missing: {', '.join(j['missing']) or 'none'}."
        for i, j in enumerate(jobs))
    raw = call_llm(
        EXPLAIN_MATCH_PROMPT.format(role=profile.target_role, listing=listing),
        json_mode=True, temperature=0.2)
    try:
        data = json.loads(raw)
        lines = data if isinstance(data, list) else list(data.values())[0]
    except (json.JSONDecodeError, IndexError, AttributeError):
        lines = []
    for i, j in enumerate(jobs):
        j["why"] = lines[i] if i < len(lines) else ""
    return jobs