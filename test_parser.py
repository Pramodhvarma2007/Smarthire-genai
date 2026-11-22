from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume

text = load_resume("data/resumes/resume3_web_developer.pdf")
profile = parse_resume(text)
print(profile.model_dump_json(indent=2))