import re
import pandas as pd
from rank_bm25 import BM25Okapi
from src.config import META_PATH
from src.search.job_search import search_jobs

_bm25 = None
_meta = None


def _words(text):
    found = re.findall(r"[a-z0-9+#.]+", str(text).lower())
    return [w.strip(".") for w in found if w.strip(".")]


def _load():
    global _bm25, _meta
    if _bm25 is None:
        _meta = pd.read_pickle(META_PATH)
        docs = [_words(f"{t} {t} {s}")   # title counted twice, then skills
                for t, s in zip(_meta["Job_Title"], _meta["Skills_Required"])]
        _bm25 = BM25Okapi(docs)
    return _bm25, _meta


def keyword_search(query_text, top_n=5):
    """Finds jobs by exact words."""
    bm25, meta = _load()
    scores = bm25.get_scores(_words(query_text))
    results = []
    for i in scores.argsort()[::-1][:top_n]:
        if scores[i] <= 0:
            break
        row = meta.iloc[int(i)].to_dict()
        row["keyword_score"] = round(float(scores[i]), 3)
        results.append(row)
    return results


def hybrid_search(query_text, top_n=5, wide_meaning=1000, wide_keyword=100, k=60):
    """Meaning search + keyword search, joined by adding up each job's rank points."""
    meaning = search_jobs(query_text, top_n=wide_meaning)
    keyword = keyword_search(query_text, top_n=wide_keyword)

    points, rows = {}, {}
    for rank, r in enumerate(meaning):
        key = r["Job_ID"]
        rows[key] = r
        points[key] = points.get(key, 0.0) + 1.0 / (k + rank + 1)
    for rank, r in enumerate(keyword):
        key = r["Job_ID"]
        if key in rows:
            rows[key]["keyword_score"] = r["keyword_score"]
        else:
            r["score"] = 0.0          # not in the meaning list
            rows[key] = r
        points[key] = points.get(key, 0.0) + 1.0 / (k + rank + 1)

    out = []
    for key in sorted(points, key=points.get, reverse=True)[:top_n]:
        row = dict(rows[key])
        row.setdefault("keyword_score", 0.0)
        row["points"] = round(points[key], 5)
        out.append(row)
    return out