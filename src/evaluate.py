import pandas as pd
from src.config import META_PATH
from src.parsing.resume_parser import Profile
from src.eval_profiles import PROFILES
from src.search.job_search import search_jobs
from src.search.matching import match_jobs, make_query, candidate_skills, skill_gap
from src.search.hybrid import hybrid_search



TOP = 5


def is_relevant(title, accept):
    t = title.lower()
    return any(k in t for k in accept)


def level_ok(level):
    """Students should see Fresher and Junior jobs."""
    return str(level).lower().startswith(("fresher", "junior"))


def meaning_only(profile):
    return search_jobs(make_query(profile), top_n=TOP)


def day9_system(profile):
    return match_jobs(profile, top_n=TOP, pool=30, level_boost=False)


def day12_system(profile):
    return match_jobs(profile, top_n=TOP)

def no_role(profile):
    return profile.model_copy(update={"target_role": ""})


def day12_skills_only(profile):
    return match_jobs(no_role(profile), top_n=TOP)


def hybrid_with_role(profile):
    return match_jobs(profile, top_n=TOP, search_fn=hybrid_search)


def hybrid_skills_only(profile):
    return match_jobs(no_role(profile), top_n=TOP, search_fn=hybrid_search)

METHODS = {
    "Meaning search only": meaning_only,
    "Day 9 system (role first, then skills)": day9_system,
    "Day 12 system (with level boost)": day12_system,
    "Day 12 system, skills only (no role)": day12_skills_only,
    "Hybrid system, role given": hybrid_with_role,
    "Hybrid system, skills only (no role)": hybrid_skills_only,
}

def run(out_path="reports/search_eval_results.md"):
    meta = pd.read_pickle(META_PATH)
    titles = meta["Job_Title"].str.lower()
    stats = {m: dict(hit=0, rel=0, level=0, good=0, skill=0, slots=0, n=0) for m in METHODS}
    detail, skipped = [], []

    for pf in PROFILES:
        profile = Profile(name=pf["id"], skills=pf["skills"], target_role=pf["role"])
        available = int(titles.apply(lambda t: any(k in t for k in pf["accept"])).sum())
        if available == 0:
            skipped.append(f"{pf['id']} {pf['role']}")
            continue
        detail.append(f"\n### {pf['id']}: wants {pf['role']} ({available} matching jobs in the data)")
        my_skills = candidate_skills(profile)
        for name, fn in METHODS.items():
            res = fn(profile)
            rel = [is_relevant(r["Job_Title"], pf["accept"]) for r in res]
            lev = [level_ok(r["Experience_Level"]) for r in res]
            good = [a and b for a, b in zip(rel, lev)]
            sk = [skill_gap(my_skills, r["Skills_Required"])[2] for r in res]
            s = stats[name]
            s["n"] += 1
            s["slots"] += len(res)
            s["hit"] += int(any(rel))
            s["rel"] += sum(rel)
            s["level"] += sum(lev)
            s["good"] += sum(good)
            s["skill"] += sum(sk)
            shown = " | ".join(f"{r['Job_Title']} ({str(r['Experience_Level']).split(' ')[0]})" for r in res)
            detail.append(f"- **{name}**: relevant {sum(rel)}/5, suitable level {sum(lev)}/5, both {sum(good)}/5")
            detail.append(f"  - {shown}")

    def pct(a, b):
        return f"{100 * a / b:.0f}%" if b else "n/a"

    n = max(s["n"] for s in stats.values())
    table = ["| Method | Profiles with 1+ relevant job | Relevant jobs | Suitable level (Fresher or Junior) | Relevant AND suitable level | Average skills you have |",
             "|---|---|---|---|---|---|"]
    for name, s in stats.items():
        table.append(f"| {name} | {s['hit']} / {s['n']} ({pct(s['hit'], s['n'])}) | "
                     f"{s['rel']} / {s['slots']} ({pct(s['rel'], s['slots'])}) | "
                     f"{s['level']} / {s['slots']} ({pct(s['level'], s['slots'])}) | "
                     f"{s['good']} / {s['slots']} ({pct(s['good'], s['slots'])}) | "
                     f"{s['skill'] / s['slots']:.0f}% |" if s["slots"] else f"| {name} | no data |")
    text = ["# Search Accuracy Results", "", f"Profiles scored: {n} of {len(PROFILES)}"]
    if skipped:
        text.append(f"Skipped (no such jobs in the data): {', '.join(skipped)}")
    text += ["", *table, "", "## Details", *detail]
    out = "\n".join(text)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
    print("\n".join(text[:12 + len(table)]))
    print(f"\nFull details saved to {out_path}")


if __name__ == "__main__":
    run()