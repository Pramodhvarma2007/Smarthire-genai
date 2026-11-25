import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
if not API_KEY:   # on the online app the key comes from the app's Secrets box
    try:
        import streamlit as st
        API_KEY = st.secrets["LLM_API_KEY"]
    except Exception:
        API_KEY = None

LLM_MODEL = "gemini-3.5-flash"

FALLBACK_MODEL = "gemini-3.5-flash-lite"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

TOP_N = 5

JOBS_PATH = "data/jobs/jobs.csv"

INDEX_PATH = "vectorstore/jobs.faiss"

JOB_TITLE_COL = "Job_Title"

JOB_SKILLS_COL = "Skills_Required"

SAMPLE_SIZE = 5000

META_PATH = "vectorstore/jobs_meta.pkl"

NOTES_DIR = "data/career_notes"
NOTES_INDEX_PATH = "vectorstore/notes.faiss"
NOTES_META_PATH = "vectorstore/notes_meta.pkl"
MIN_SCORE = 0.30

NOTE_MIN_SCORE = 0.30
JOB_MIN_SCORE = 0.45

MODEL_CHAIN = [LLM_MODEL, FALLBACK_MODEL, "gemini-3.7-flash", "gemini-3.1-flash-lite"]