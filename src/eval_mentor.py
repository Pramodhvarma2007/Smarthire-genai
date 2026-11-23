import re
import time
from src.eval_questions import IN_SCOPE, UNRELATED, NOT_IN_DOCS
from src.mentor.rag_chain import ask_mentor, retrieve

CITE = re.compile(r"\[([\d,\s;]+)\]")


def is_refusal(answer):
    a = answer.strip().lower().replace("\u2019", "'")
    return a.startswith("i don't have")


def cited_numbers(answer):
    nums = set()
    for m in CITE.findall(answer):
        nums |= {int(x) for x in re.findall(r"\d+", m)}
    return nums


def plain_numbers(text):
    text = CITE.sub(" ", text)
    text = re.sub(r"(?m)^\s*\d+\.\s", " ", text)   # list numbering
    return set(re.findall(r"\d+(?:\.\d+)?", text))


def check(item, group):
    q = item["q"]
    found = retrieve(q)                 # local search, no AI request
    start = time.time()
    try:
        r = ask_mentor(q)
        error = ""
    except Exception as e:
        r, error = {"answer": "", "sources": []}, str(e)[:100]
    seconds = time.time() - start
    answer, sources = r["answer"], r["sources"]
    row = {"group": group, "q": q, "answer": answer, "seconds": seconds, "error": error,
           "refused": is_refusal(answer), "before_ai": not found["sources"],
           "sources": [f"[{s['label']}] {s['title']}" for s in sources]}
    if group == "in_scope":
        cites = cited_numbers(answer)
        valid = {s["label"] for s in sources}
        row["cites_ok"] = bool(cites) and cites <= valid
        titles = " ".join(s["title"].lower() for s in sources)
        row["hit"] = any(k in titles for k in item["expect"])
        row["invented"] = sorted(plain_numbers(answer) - plain_numbers(found["context"]) - plain_numbers(q))
        row["pass"] = (not error and not row["refused"] and row["cites_ok"]
                       and row["hit"] and not row["invented"])
    return row


def run(out_path="reports/mentor_eval_results.md"):
    rows = []
    for group, items in (("in_scope", IN_SCOPE), ("unrelated", UNRELATED), ("not_in_docs", NOT_IN_DOCS)):
        for i, item in enumerate(items, 1):
            row = check(item, group)
            rows.append(row)
            print(f"{group} {i}/{len(items)} done", f"(NOT RUN: {row['error']})" if row["error"] else "")

    def part(g):
        return [r for r in rows if r["group"] == g and not r["error"]]

    ins, unr, nid = part("in_scope"), part("unrelated"), part("not_in_docs")
    not_run = [r for r in rows if r["error"]]
    slow = [r["seconds"] for r in rows if not r["error"] and not r["before_ai"] and r["seconds"] > 0.5]

    def frac(a, n):
        return f"{a} / {n}"

    summary = [
        "# Mentor Evaluation Results", "",
        "| Measure | Result |", "|---|---|",
        f"| Questions not run (AI limit reached) | {len(not_run)} |",
        f"| In-scope: answered (not refused) | {frac(sum(not r['refused'] for r in ins), len(ins))} |",
        f"| In-scope: source numbers present and valid | {frac(sum(r['cites_ok'] for r in ins), len(ins))} |",
        f"| In-scope: a source on the right topic was used | {frac(sum(r['hit'] for r in ins), len(ins))} |",
        f"| In-scope: no possible invented numbers | {frac(sum(not r['invented'] for r in ins), len(ins))} |",
        f"| In-scope: passed ALL automatic checks | {frac(sum(r['pass'] for r in ins), len(ins))} |",
        f"| Unrelated: refused | {frac(sum(r['refused'] for r in unr), len(unr))} |",
        f"| Unrelated: refused before any AI call | {frac(sum(r['before_ai'] for r in unr), len(unr))} |",
        f"| Not in our documents: refused | {frac(sum(r['refused'] for r in nid), len(nid))} |",
        f"| Not in our documents: stopped before any AI call | {frac(sum(r['before_ai'] for r in nid), len(nid))} |",
        "| Average time for a new AI answer | " +
        (f"{sum(slow) / len(slow):.1f} seconds ({len(slow)} answers)" if slow else "n/a (answers were already saved)") + " |",
    ]
    details = ["", "## Details"]
    for r in rows:
        details += ["", f"### [{r['group']}] {r['q']}"]
        if r["error"]:
            details.append(f"NOT RUN: {r['error']}")
            continue
        details += [f"**Answer:** {r['answer']}", "", f"**Sources:** {', '.join(r['sources']) or 'none'}"]
        if r["group"] == "in_scope":
            details.append(f"Automatic checks: source numbers ok = {r['cites_ok']}, right topic = {r['hit']}, "
                           f"possible invented numbers = {r['invented'] or 'none'}, passed = {r['pass']}")
        else:
            details.append(f"Refused = {r['refused']}, stopped before AI = {r['before_ai']}")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(summary + details))
    print("\n" + "\n".join(summary))
    print(f"\nFull answers saved to {out_path}")


if __name__ == "__main__":
    run()