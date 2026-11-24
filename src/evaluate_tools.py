import pandas as pd
from src.config import META_PATH
from src.search.job_search import search_jobs
from src.search.hybrid import keyword_search, hybrid_search
from src.search.matching import same_skill

TOP = 5

# Written before looking at any results
QUERIES = [
    ["Power BI", "DAX"], ["Power BI", "DAX", "Data Modeling"],
    ["Selenium", "Postman"], ["Selenium", "API Testing"],
    ["React", "Redux"], ["React", "Node.js", "MongoDB"], ["TypeScript", "Next.js"],
    ["Kotlin", "REST APIs"], ["Java", "Spring Boot"],
    ["Django", "PostgreSQL"], ["Django", "FastAPI"],
    ["Docker", "Kubernetes"], ["Docker", "Kubernetes", "AWS"], ["Terraform", "AWS"],
    ["TensorFlow", "Scikit-learn"], ["PyTorch", "MLOps"],
    ["BERT", "SpaCy"], ["BERT", "HuggingFace", "LLMs"],
    ["Tableau", "SQL"], ["Tableau", "Excel", "Data Visualization"],
    ["ETL", "SQL", "Python"], ["Azure", "ETL"], ["Spark", "Airflow"],
    ["Flutter", "Dart"], ["Go", "Microservices"],
]

METHODS = {
    "Meaning search only": search_jobs,
    "Keyword search only": keyword_search,
    "Combined (meaning + keyword)": hybrid_search,
}


def has_tool(skills_text, tool):
    skills = [s.strip() for s in str(skills_text).split(",") if s.strip()]
    return any(same_skill(tool, s) for s in skills)


def run(out_path="reports/tool_eval_results.md"):
    meta = pd.read_pickle(META_PATH)
    skill_lists = meta["Skills_Required"].tolist()
    stats = {m: dict(hit=0, all_tools=0, one_tool=0, titles=0, n=0) for m in METHODS}
    detail, skipped = [], []

    for tools in QUERIES:
        available = sum(all(has_tool(s, t) for t in tools) for s in skill_lists)
        if available == 0:
            skipped.append(" + ".join(tools))
            continue
        detail.append(f"\n### {' + '.join(tools)} ({available} jobs in the data list all of these)")
        for name, fn in METHODS.items():
            res = fn(", ".join(tools), top_n=TOP)
            full = [all(has_tool(r["Skills_Required"], t) for t in tools) for r in res]
            some = [any(has_tool(r["Skills_Required"], t) for t in tools) for r in res]
            s = stats[name]
            s["n"] += 1
            s["hit"] += int(any(full))
            s["all_tools"] += sum(full)
            s["one_tool"] += sum(some)
            s["titles"] += len({r["Job_Title"] for r in res})
            detail.append(f"- **{name}**: all tools {sum(full)}/5, at least one {sum(some)}/5, "
                          f"different titles {len({r['Job_Title'] for r in res})}")

    def pct(a, b):
        return f"{100 * a / b:.0f}%" if b else "n/a"

    table = ["| Method | Searches with 1+ job listing ALL tools | Jobs listing ALL tools | Jobs listing at least one tool | Average different job titles in top 5 |",
             "|---|---|---|---|---|"]
    for name, s in stats.items():
        slots = s["n"] * TOP
        table.append(f"| {name} | {s['hit']} / {s['n']} ({pct(s['hit'], s['n'])}) | "
                     f"{s['all_tools']} / {slots} ({pct(s['all_tools'], slots)}) | "
                     f"{s['one_tool']} / {slots} ({pct(s['one_tool'], slots)}) | "
                     f"{s['titles'] / s['n']:.1f} |")
    n = max(s["n"] for s in stats.values())
    text = ["# Exact-Tool Search Results", "", f"Searches scored: {n} of {len(QUERIES)}"]
    if skipped:
        text.append(f"Skipped (no job lists all these tools): {'; '.join(skipped)}")
    text += ["", *table, "", "## Details", *detail]
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(text))
    print("\n".join(text[:6 + len(table)]))
    print(f"\nFull details saved to {out_path}")