import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")

LLM_MODEL = "gemini-3.8-flash"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

TOP_N = 5

JOBS_PATH = "data/jobs/jobs.csv"

INDEX_PATH = "vectorstore/jobs.faiss"