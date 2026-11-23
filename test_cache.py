import time
from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume

text = load_resume("data/resumes/resume1_data_analyst.pdf")
for i in (1, 2):
    t = time.time()
    parse_resume(text)
    print(f"Run {i}: {time.time() - t:.2f} seconds")