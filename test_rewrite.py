import glob
import os
import re
from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume
from src.search.matching import match_jobs
from src.generate.resume_rewrite import rewrite_resume, check_rewrite, build_docx

os.makedirs("output", exist_ok=True)
lines, passed, total = ["# Rewrite Samples", ""], 0, 0

for path in sorted(glob.glob("data/resumes/*")):
    if not path.lower().endswith((".pdf", ".docx")):
        continue
    name = os.path.splitext(os.path.basename(path))[0]
    try:
        profile = parse_resume(load_resume(path))
        jobs = match_jobs(profile)
        job = next((j for j in jobs if j["missing"]), jobs[0])
        result = rewrite_resume(profile, job)
    except Exception as e:
        print(name, "NOT RUN:", str(e)[:100])
        continue

    issues = check_rewrite(profile, job, result)
    slug = re.sub(r"\W+", "_", job["Job_Title"])
    out_path = f"output/{name}_for_{slug}.docx"
    with open(out_path, "wb") as f:
        f.write(build_docx(profile, result))
    readable = profile.name in load_resume(out_path)   # free read-back check

    total += 1
    passed += not issues
    print(f"{name} -> {job['Job_Title']} ({job['Experience_Level']}) | problems: {issues or 'none'} | file readable: {readable}")

    before = (profile.experience[0].summary if profile.experience
              else profile.projects[0].description if profile.projects else "")
    after = (result["experience"][0] if result["experience"]
             else result["projects"][0] if result["projects"] else [])
    lines += [f"## {name} -> {job['Job_Title']} ({job['Experience_Level']})",
              f"Skills the job wants that you lack (must NOT be claimed): {job['missing']}",
              f"Problems: {issues or 'none'}", "",
              f"**Summary:** {result['summary']}", "",
              f"**Before:** {before}", f"**After:** {' / '.join(after)}", ""]

print(f"\nRewrites passing all checks: {passed} / {total}")
open("reports/rewrite_samples.md", "w", encoding="utf-8").write("\n".join(lines))
print("Word files are in the output folder. Details: reports/rewrite_samples.md")