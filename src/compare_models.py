import time
import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer
from src.config import META_PATH, EMBED_MODEL
from src.eval_profiles import PROFILES
from src.evaluate import is_relevant, level_ok
from src.evaluate_tools import QUERIES, has_tool
from src.parsing.resume_parser import Profile
from src.search.job_search import make_job_text
from src.search.matching import make_query

MODELS = {
    "MiniLM (current)": EMBED_MODEL,
    "BGE small": "BAAI/bge-small-en-v1.5",
}
TOP = 5


def build(model_name, texts):
    model = SentenceTransformer(model_name)
    start = time.time()
    vectors = model.encode(texts, batch_size=64, show_progress_bar=False,
                           normalize_embeddings=True).astype("float32")
    seconds = time.time() - start
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    return model, index, seconds, vectors.shape[1]


def search(model, index, meta, text):
    start = time.time()
    q = model.encode([text], show_progress_bar=False,
                     normalize_embeddings=True).astype("float32")
    _, ids = index.search(q, TOP)
    rows = [meta.iloc[int(i)] for i in ids[0]]
    return rows, time.time() - start


def run(out_path="reports/model_compare_results.md"):
    meta = pd.read_pickle(META_PATH)
    texts = [make_job_text(r) for _, r in meta.iterrows()]
    skill_lists = meta["Skills_Required"].tolist()
    scored_tools = [t for t in QUERIES
                    if any(all(has_tool(s, x) for x in t) for s in skill_lists)]

    out = {}
    for label, name in MODELS.items():
        print("Working on", label, "...")
        model, index, build_s, dim = build(name, texts)
        res = {"build_s": build_s, "dim": dim, "times": []}
        for variant in ("role", "skills"):
            hit = rel_n = good_n = 0
            for pf in PROFILES:
                profile = Profile(name=pf["id"], skills=pf["skills"],
                                  target_role=pf["role"] if variant == "role" else "")
                rows, secs = search(model, index, meta, make_query(profile))
                res["times"].append(secs)
                rel = [is_relevant(r["Job_Title"], pf["accept"]) for r in rows]
                lev = [level_ok(r["Experience_Level"]) for r in rows]
                hit += int(any(rel))
                rel_n += sum(rel)
                good_n += sum(a and b for a, b in zip(rel, lev))
            res[variant] = (hit, rel_n, good_n)
        t_hit = t_full = 0
        for tools in scored_tools:
            rows, secs = search(model, index, meta, ", ".join(tools))
            full = [all(has_tool(r["Skills_Required"], x) for x in tools) for r in rows]
            t_hit += int(any(full))
            t_full += sum(full)
        res["tools"] = (t_hit, t_full)
        out[label] = res

    n_p, n_t = len(PROFILES), len(scored_tools)

    def pct(a, b):
        return f"{a} / {b} ({100 * a / b:.0f}%)"

    measures = [
        ("Role + skills: profiles with 1+ relevant job", lambda r: pct(r["role"][0], n_p)),
        ("Role + skills: relevant jobs", lambda r: pct(r["role"][1], n_p * TOP)),
        ("Skills only: profiles with 1+ relevant job", lambda r: pct(r["skills"][0], n_p)),
        ("Skills only: relevant jobs", lambda r: pct(r["skills"][1], n_p * TOP)),
        ("Skills only: relevant AND Fresher or Junior", lambda r: pct(r["skills"][2], n_p * TOP)),
        ("Exact tools: searches with 1+ job listing ALL tools", lambda r: pct(r["tools"][0], n_t)),
        ("Exact tools: jobs listing ALL tools", lambda r: pct(r["tools"][1], n_t * TOP)),
        ("Time to turn all jobs into numbers", lambda r: f"{r['build_s']:.0f} seconds"),
        ("Average time per search", lambda r: f"{1000 * sum(r['times']) / len(r['times']):.0f} ms"),
        ("Length of each job's list of numbers", lambda r: str(r["dim"])),
    ]
    labels = list(MODELS)
    lines = ["# Search Model Comparison", "",
             f"Jobs: {len(texts)}. Test profiles: {n_p}. Tool searches: {n_t}.", "",
             "| Measure | " + " | ".join(labels) + " |",
             "|---|" + "---|" * len(labels)]
    for name, fn in measures:
        lines.append(f"| {name} | " + " | ".join(fn(out[l]) for l in labels) + " |")
    text = "\n".join(lines)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("\n" + text)
    print(f"\nSaved to {out_path}")