import os
import subprocess

tracked = set(subprocess.run(["git", "ls-files"], capture_output=True, text=True).stdout.split())

MUST_BE_THERE = ["app/streamlit_app.py", "requirements.txt", "src/config.py", "src/llm.py",
                 "vectorstore/jobs.faiss", "vectorstore/jobs_meta.pkl",
                 "vectorstore/notes.faiss", "vectorstore/notes_meta.pkl",
                 "data/resumes/resume1_data_analyst.pdf"]
MUST_NOT_BE_THERE = [".env", "vectorstore/llm_cache.json", "data/jobs/jobs.csv"]
NEEDED = ["streamlit", "faiss-cpu", "sentence-transformers", "rank-bm25", "python-docx", "pypdf",
          "pydantic", "pandas", "google-genai", "langchain-core", "langchain-text-splitters",
          "python-dotenv"]

ok = True
for f in MUST_BE_THERE:
    if f not in tracked:
        print("NOT in git yet:", f)
        ok = False
for f in MUST_NOT_BE_THERE:
    if f in tracked:
        print("MUST NOT be on GitHub:", f)
        ok = False
req = open("requirements.txt").read().lower()
for pkg in NEEDED:
    if pkg not in req:
        print("requirements.txt is missing:", pkg)
        ok = False
for f in ("jobs.faiss", "jobs_meta.pkl", "notes.faiss", "notes_meta.pkl"):
    print(f, round(os.path.getsize(f"vectorstore/{f}") / 1_000_000, 1), "MB")
print("\nREADY TO PUSH" if ok else "\nFIX THE LINES ABOVE FIRST")