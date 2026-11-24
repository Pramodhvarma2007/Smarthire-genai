from src.eval_profiles import PROFILES
from src.parsing.resume_parser import Profile
from src.search.matching import match_jobs, candidate_skills
from src.generate.learning_plan import make_plan, check_plan
from src.generate.prompts import PLAN_PROMPT_V1, PLAN_PROMPT_V2

V2_IDS = ["P01", "P03", "P06", "P09", "P14"]
V1_IDS = ["P01", "P14"]
lines, v2_pass = ["# Learning Plan Samples", ""], 0

for pf in PROFILES:
    if pf["id"] not in V2_IDS:
        continue
    profile = Profile(name=pf["id"], skills=pf["skills"], target_role=pf["role"])
    jobs = [j for j in match_jobs(profile) if j["missing"]]
    if not jobs:
        print(pf["id"], "no job with missing skills")
        continue
    job, mine = jobs[0], candidate_skills(profile)
    for label, prompt in (("V2", PLAN_PROMPT_V2), ("V1", PLAN_PROMPT_V1)):
        if label == "V1" and pf["id"] not in V1_IDS:
            continue
        r = make_plan(mine, job, prompt=prompt)
        issues = check_plan(r["plan"], r["missing"])
        if label == "V2":
            v2_pass += not issues
        print(f"{pf['id']} {label}: {job['Job_Title']} | learn {r['missing']} | problems: {issues or 'none'}")
        lines += [f"## {pf['id']} {label}: {job['Job_Title']} ({job['Experience_Level']})",
                  f"Learn: {r['missing']}", f"Problems: {issues or 'none'}", "", r["plan"], ""]

print(f"\nV2 plans passing all checks: {v2_pass} / {len(V2_IDS)}")
open("reports/plan_samples.md", "w", encoding="utf-8").write("\n".join(lines))
print("Saved to reports/plan_samples.md")