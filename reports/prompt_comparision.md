# Prompt Comparison: Before and After

**Model:** gemini-3.5-flash (fallback: gemini-3.5-flash-lite)
**Test date:** 30 OCT 2026
**Test resume:** resume4_fresher_mixed.pdf (Kiran Patel, B.Tech IT fresher)
**Target job:** Data Analyst (SQL, Excel, Power BI, Python/Pandas, dashboards, communication)

---

## 1. Resume Parser: V1 vs V2

| | V1 (basic prompt) | V2 (improved prompt) |
|---|---|---|
| Projects captured | No (no field for it) | Yes: Expense Tracker and Student Marks Manager |
| Soft skills | Mixed into the skills list (Communication, Teamwork) | Kept in a separate `soft_skills` field |
| Target role | "Data and Software" (two roles mixed, vague) | "Software Developer" (one clear job title) |
| Experience | Empty list | 1 entry: Online Python course (30 hours) |

**What changed in the prompt:**
- Added a `projects` field.
- Split soft skills from technical skills.
- Asked for ONE specific job title.
- Added the rule "use only information in the resume."

**Result:** V2 captured the projects that V1 missed completely, and the target role became a single job title instead of a vague mix. One weakness remains: the 30-hour course was placed under experience, and the CV suggestions later flagged this as weak. A future fix is a separate "certifications and training" field.

---

## 2. CV Suggestions: V1 vs V2

### V1 prompt (weak)
> "Give suggestions to improve this resume for the job."

**What the output did:**
- Very long, with 5 loose sections plus a full rewritten resume in JSON.
- Mostly generic advice ("add a summary", "learn Power BI").
- **Invented a lot of content that is not in the resume:**
  - Claimed the Expense Tracker has an "interactive Power BI dashboard" that forecasts monthly savings.
  - Claimed the Student Marks app uses "JOINs, Group By, Window Functions" and visual charts.
  - Listed "Python (Pandas, NumPy)", "Excel (Advanced)" and "Power BI" as skills, although Power BI and Pandas are listed as missing.
  - Created a certification, "Python for Data Analysis", from an "Online Course Platform".
  - Added "relevant coursework" (DBMS, Applied Statistics, Data Analytics) that the resume does not mention.
  - Wrote a summary saying "experienced in data cleaning, exploratory data analysis, and building interactive dashboards".
- Told the candidate to de-emphasize Java and HTML, which is questionable advice for a fresher.

**Risk:** a student who copies this resume would be claiming skills and projects they do not have.

### V2 prompt (improved)
> Fixed three-part format (Missing Skills, Weak Points, Rewritten Summary), plus the rules "use only facts from the profile" and "write [add number] instead of making one up."

**What the output did:**
- Short and structured, with exactly the 3 requested sections.
- **Missing skills** listed honestly: Power BI, Python (Pandas), Dashboard creation.
- **Weak points** picked 3 real lines (the Python course, the expense script, the Java console app) and rewrote each with an action verb. Missing numbers became `[add number]` instead of made-up figures.
- The rewritten summary mentions only skills the candidate has (Python, SQL, Excel) and the real projects.

### Side-by-side

| Criteria | V1 | V2 |
|---|---|---|
| Follows a clear format | No | Yes |
| Length | Very long | Short and easy to scan |
| Invents skills, projects or certificates | Yes (many) | No |
| Uses placeholders for missing facts | No | Yes (`[add number]`) |
| Admits missing skills honestly | Partly, then contradicts itself | Yes |
| Safe to copy into a real resume | No | Mostly |

### Why V2 is better
Three prompt changes made the difference:
1. A **fixed output format** made the answer short and readable.
2. A **grounding rule** ("only facts from the profile") stopped invented skills, projects and certificates.
3. A **placeholder rule** (`[add number]`) kept the advice honest instead of fabricated.

### Limitations still seen in V2
- Some rewrites add mild wording that the resume does not state, such as "to master foundational Python programming concepts" and the word "detail-oriented" in the summary.
- The tool can still be wrong, so the portal should tell users to check every suggestion against their real experience.
- Only one resume and one target job were tested so far. More tests are planned in the evaluation stage.

---

## 3. Reliability note
The Gemini API returned `503 UNAVAILABLE (high demand)` during development. I added a retry helper in `src/llm.py` (3 attempts per model, then a fallback model), so the app does not crash during overload.

---

## 4. Conclusion
Better prompts improved output quality without changing the model. The biggest gain was **grounding**: V1 produced a polished but partly fake resume, while V2 stayed honest about what the candidate has and what is missing. This matters for a tool that gives career advice.