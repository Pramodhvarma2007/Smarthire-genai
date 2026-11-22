from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume
from src.generate.prompts import PARSER_PROMPT_V1, PARSER_PROMPT_V2

text = load_resume("data/resumes/resume4_fresher_mixed.pdf")
print("===== V1 =====")
print(parse_resume(text, PARSER_PROMPT_V1).model_dump_json(indent=2))
print("===== V2 =====")
print(parse_resume(text, PARSER_PROMPT_V2).model_dump_json(indent=2))