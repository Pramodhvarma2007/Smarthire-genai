from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume
from src.generate.cv_suggestions import suggest_improvements
from src.generate.prompts import CV_SUGGEST_V1, CV_SUGGEST_V2

profile = parse_resume(load_resume("data/resumes/resume4_fresher_mixed.pdf"))
job = "Data Analyst. Needs SQL, Excel, Power BI, Python (Pandas), dashboards, and clear communication."

print("===== V1 (weak prompt) =====")
print(suggest_improvements(profile, job, prompt=CV_SUGGEST_V1))

print("\n===== V2 (better prompt) =====")
print(suggest_improvements(profile, job, prompt=CV_SUGGEST_V2))