from src.eval_questions import IN_SCOPE
from src.mentor.rag_chain import ask_mentor, retrieve

PICK = [0, 1, 2, 3, 4, 5, 7, 8, 10, 11]      # 10 of the 20 career questions
out = ["# Hand scoring sheet", ""]
for n, i in enumerate(PICK, 1):
    q = IN_SCOPE[i]["q"]
    found = retrieve(q)
    r = ask_mentor(q)
    out += [f"## {n}. {q}", "", "**Answer:**", r["answer"], "", "**What the mentor was shown:**"]
    out += [piece[:400] for piece in found["context"].split("\n\n")]
    out += ["", "| Correct (0-2) | Sticks to documents (0-2) | Helpful (0-2) | Note |",
            "|---|---|---|---|", "|  |  |  |  |", ""]
with open("reports/hand_scoring_sheet.md", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("Saved reports/hand_scoring_sheet.md")