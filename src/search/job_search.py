import faiss
import pandas as pd
from src.config import (JOBS_PATH, INDEX_PATH, META_PATH, TOP_N, SAMPLE_SIZE,
                        JOB_TITLE_COL, JOB_SKILLS_COL)
from src.search.embed import embed_texts


def make_job_text(row):
    return (f"{row['Job_Title']}. Skills: {row[JOB_SKILLS_COL]}. "
            f"Industry: {row['Industry']}. "
            f"Experience: {row['Experience_Level']}. "
            f"Education: {row['Education_Required']}.")


def build_index():
    df = pd.read_csv(JOBS_PATH)
    df = df.dropna(subset=[JOB_TITLE_COL, JOB_SKILLS_COL]).reset_index(drop=True)
    if len(df) > SAMPLE_SIZE:
        df = df.sample(SAMPLE_SIZE, random_state=42).reset_index(drop=True)

    texts = [make_job_text(r) for _, r in df.iterrows()]
    print(f"Embedding {len(texts)} jobs...")
    vectors = embed_texts(texts)

    index = faiss.IndexFlatIP(vectors.shape[1])  # cosine similarity
    index.add(vectors)
    faiss.write_index(index, INDEX_PATH)
    df.to_pickle(META_PATH)
    print("Saved index with", index.ntotal, "jobs")


_index = None
_meta = None


def search_jobs(query_text, top_n=TOP_N):
    global _index, _meta
    if _index is None:
        _index = faiss.read_index(INDEX_PATH)
        _meta = pd.read_pickle(META_PATH)
    q = embed_texts([query_text])
    scores, ids = _index.search(q, top_n)
    results = []
    for score, i in zip(scores[0], ids[0]):
        row = _meta.iloc[int(i)].to_dict()
        row["score"] = round(float(score), 3)
        results.append(row)
    return results