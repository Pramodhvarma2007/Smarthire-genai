import glob
from src.eval_attacks import ATTACKS, BENIGN
from src.mentor.rag_chain import ask_mentor, retrieve
from src.parsing.loader import load_resume
from src.safety.guardrails import check_input, has_injection


def run(heldout=False, use_ai=False):
    attacks, benign, out_path = ATTACKS, BENIGN, "reports/attack_results.md"
    if heldout:
        from src.eval_attacks_heldout import ATTACKS as attacks, BENIGN as benign
        out_path = "reports/attack_results_heldout.md"

    kinds, reached, detail = {}, [], []
    for kind, text in attacks:
        c = check_input(text)
        if not c["ok"]:
            stage = "rules"
        elif not retrieve(c["clean_text"])["sources"]:
            stage = "nothing close"
        else:
            stage = "reached AI"
            reached.append(text)
        kinds.setdefault(kind, {"rules": 0, "nothing close": 0, "reached AI": 0})[stage] += 1
        detail.append(f"- [{stage}] ({kind}) {text}")

    blocked, wrongly_refused, answered = [], [], 0
    for text in benign:
        c = check_input(text)
        if not c["ok"]:
            blocked.append(text)
        elif not retrieve(c["clean_text"])["sources"]:
            wrongly_refused.append(text)
        else:
            answered += 1

    flagged = []
    for p in glob.glob("data/resumes/*"):
        if p.lower().endswith((".pdf", ".docx")) and has_injection(load_resume(p)):
            flagged.append(p)

    n = len(attacks)
    totals = {s: sum(k[s] for k in kinds.values()) for s in ("rules", "nothing close", "reached AI")}
    lines = ["# Safety Attack Test", "",
             f"Attack messages: {n}. Normal messages: {len(benign)}.", "",
             "| Attack type | Stopped by safety rules | Refused: nothing close found (no AI call) | Reached the AI model |",
             "|---|---|---|---|"]
    for k, v in kinds.items():
        lines.append(f"| {k} | {v['rules']} | {v['nothing close']} | {v['reached AI']} |")
    lines += [f"| **Total** | **{totals['rules']} / {n}** | **{totals['nothing close']} / {n}** | **{totals['reached AI']} / {n}** |",
              "", f"Normal messages wrongly blocked by the rules: {len(blocked)} / {len(benign)}",
              f"Normal messages wrongly refused (nothing close found): {len(wrongly_refused)} / {len(benign)}",
              f"Normal messages that went through: {answered} / {len(benign)}",
              f"Sample resumes wrongly flagged as hidden instructions: {len(flagged)}"]
    if blocked:
        lines += ["", "Wrongly blocked:"] + [f"- {t}" for t in blocked]
    if wrongly_refused:
        lines += ["", "Wrongly refused:"] + [f"- {t}" for t in wrongly_refused]
    lines += ["", "## Every attack", *detail]
    if use_ai and reached:
        lines += ["", "## Messages that reached the AI model, and what it answered"]
        for t in reached:
            lines += ["", f"**{t}**", ask_mentor(t)["answer"]]
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n".join(lines[:16 + len(kinds)]))
    print("\nSaved to", out_path)
