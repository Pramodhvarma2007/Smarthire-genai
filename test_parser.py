from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume

text = load_resume("data/resumes/resume1_data_analyst.pdf")
profile = parse_resume(text)
print(profile.model_dump_json(indent=2))