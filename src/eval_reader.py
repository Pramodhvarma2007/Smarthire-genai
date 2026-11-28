import os
from src.eval_resumes import RESUMES
from src.parsing.loader import load_resume
from src.search.matching import same_skill

FIELDS = ["name", "email", "skills found (80% or more)", "no invented skills",
          "experience (right count and companies)", "projects (right count)",
          "education (school found)", "target role"]
FOLDER = "data/resumes_test"


def score(r, profile, text):
    """Returns True or False for each of the 8 fields."""
    t, low = r["truth"], text.lower()
    found = [any(same_skill(s, p) for p in profile.skills) for s in r["skills"]]
    invented = [p for p in profile.skills
                if not all(w in low for w in p.lower().replace("/", " ").split() if len(w) > 2)]
    companies_ok = all(any(c.lower() in e.company.lower() or e.company.lower() in c.lower()
                           for e in profile.experience if e.company) for c in t["companies"])
    return {
        FIELDS[0]: profile.name.strip().lower() == r["name"].lower(),
        FIELDS[1]: profile.email.strip().lower() == r["email"].lower(),
        FIELDS[2]: sum(found) >= 0.8 * len(r["skills"]),
        FIELDS[3]: not invented,
        FIELDS[4]: len(profile.experience) == t["n_exp"] and companies_ok,
        FIELDS[5]: len(profile.projects) == t["n_proj"],
        FIELDS[6]: any(t["institution"].lower() in e.institution.lower() for e in profile.education),
        FIELDS[7]: any(w in profile.target_role.lower() for w in t["role_words"]),
    }


def run(out_path="reports/reader_eval_results.md"):
    from src.parsing.resume_parser import parse_resume
    from src.safety.guardrails import mask_pii
    rows, other, details = [], [], []
    totals = {f: 0 for f in FIELDS}
    scored = reject_ok = reject_n = masked_ok = masked_n = 0
    for r in RESUMES:
        path = f"{FOLDER}/{r['file']}.docx"
        if not os.path.exists(path):
            print("MISSING FILE:", path)
            continue
        text = load_resume(path)
        masked_n += 1
        masked_ok += (r["phone"].split(" ", 1)[1] not in mask_pii(text)[0])
        try:
            profile = parse_resume(text)
        except ValueError as e:
            if r.get("expect_reject") and "instructions aimed" in str(e):
                reject_n += 1
                reject_ok += 1
                other.append(f"- {r['file']}: rejected correctly (hidden instruction found)")
            else:
                other.append(f"- {r['file']}: NOT RUN: {str(e)[:60]}")
            print(r["file"], "->", str(e)[:70])
            continue
        except Exception as e:
            other.append(f"- {r['file']}: NOT RUN: {str(e)[:60]}")
            print(r["file"], "NOT RUN:", str(e)[:70])
            continue
        if r.get("expect_reject"):
            reject_n += 1
            other.append(f"- {r['file']}: NOT rejected (the hidden instruction was missed)")
            continue
        res = score(r, profile, text)
        scored += 1
        for f in FIELDS:
            totals[f] += res[f]
        wrong = [f for f in FIELDS if not res[f]]
        rows.append(f"| {r['file']} | {sum(res.values())} / 8 | {', '.join(wrong) or 'none'} |")
        details.append(f"\n### {r['file']} ({r['layout']})\nWrong: {wrong or 'none'}\n"
                       f"Got: name={profile.name!r}, email={profile.email!r}, skills={profile.skills}, "
                       f"experience={[(e.role, e.company) for e in profile.experience]}, "
                       f"projects={[p.name for p in profile.projects]}, "
                       f"education={[(e.degree, e.institution) for e in profile.education]}, "
                       f"target role={profile.target_role!r}")
        print(r["file"], sum(res.values()), "/ 8", "wrong:", wrong or "none")

    lines = ["# Resume Reader Accuracy", "", f"Resumes scored: {scored}. Fields per resume: 8.", "",
             "| Resume | Fields right | Wrong fields |", "|---|---|---|", *rows, "", *other,
             "", "| Field | Right |", "|---|---|"]
    lines += [f"| {f} | {totals[f]} / {scored} |" for f in FIELDS]
    if scored:
        total = sum(totals.values())
        lines += ["", f"**Total fields right: {total} / {scored * 8} ({100 * total / (scored * 8):.0f}%)**"]
    lines += [f"Hidden-instruction resumes rejected: {reject_ok} / {reject_n}",
              f"Phone numbers hidden before reaching the AI: {masked_ok} / {masked_n}", *details]
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n".join(lines[:18 + len(FIELDS)]))
    print("\nFull details saved to", out_path)