from src.eval_profiles import PROFILES
from src.evaluate import day12_skills_only, is_relevant
from src.parsing.resume_parser import Profile

for pf in PROFILES:
    profile = Profile(name=pf["id"], skills=pf["skills"], target_role=pf["role"])
    res = day12_skills_only(profile)
    rel = [is_relevant(r["Job_Title"], pf["accept"]) for r in res]
    if sum(rel) < 5:
        print(pf["id"], pf["role"], "| skills:", pf["skills"], "| relevant", sum(rel), "/ 5")
        print("    got:", [r["Job_Title"] for r in res])