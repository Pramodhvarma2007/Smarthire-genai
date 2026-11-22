import glob
from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume
from src.search.matching import match_jobs, explain_matches

for path in sorted(glob.glob("data/resumes/*.pdf")):
    profile = parse_resume(load_resume(path))
    jobs = explain_matches(profile, match_jobs(profile))
    print("\n" + "=" * 70)
    print(path, "| wants:", profile.target_role)
    for j in jobs:
        print(f"\n{j['Job_Title']} at {j['Company']} | {j['City']} | "
              f"{j['Experience_Level']} | skill match {j['skill_match']}%")
        print("  Have   :", ", ".join(j["matched"]) or "-")
        print("  Missing:", ", ".join(j["missing"]) or "-")
        print("  Why    :", j["why"])