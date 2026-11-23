from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume
from src.search.matching import match_jobs

p = parse_resume(load_resume("data/resumes/resume1_data_analyst.pdf"))
for role in ["Data Analyst", "Web Developer", "Machine Learning Engineer"]:
    p.target_role = role
    print(role, "->", [j["Job_Title"] for j in match_jobs(p)])