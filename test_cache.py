import time
import random
from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume

text = load_resume("data/resumes/resume1_data_analyst.pdf")
text += f"\nReference number: {random.randint(100000, 999999)}"   # makes the text new

for i in (1, 2):
    t = time.time()
    parse_resume(text)
    print(f"Run {i}: {time.time() - t:.2f} seconds")