# Hybrid Search Notes (Day 13)

**Date:** 21 Nov 2026
**What was done:** built a search that joins meaning search and exact-word search, then compared it with the Day 12 system on the same 20 test profiles
**Cost:** no AI requests

## How the combined search works
- **Meaning search** finds jobs with a similar sense, but can miss exact tool names such as Node.js or DAX.
- **Keyword search** (BM25) finds jobs that contain the exact words, but misses similar words. Job titles count double, then skills.
- Both lists are joined by giving each job points for its rank in each list. A job that ranks high in both gets the most points.

## Results (20 profiles, top 5 jobs each)

| Method | Profiles with 1+ relevant job | Relevant jobs | Suitable level (Fresher or Junior) | Relevant AND suitable level | Average skills the student has |
|---|---|---|---|---|---|
| Meaning search only | 20 / 20 | 97 / 100 | 60 / 100 | 57 / 100 | 69% |
| Day 9 system | 20 / 20 | 100 / 100 | 52 / 100 | 52 / 100 | 76% |
| Day 12 system (role given, level boost) | 20 / 20 | 100 / 100 | 100 / 100 | 100 / 100 | 68% |
| Day 12 system, skills only (no role) | 19 / 20 | 91 / 100 | 100 / 100 | 91 / 100 | 73% |
| Hybrid system, role given | 20 / 20 | 100 / 100 | 100 / 100 | 100 / 100 | 72% |
| Hybrid system, skills only (no role) | 19 / 20 | 91 / 100 | 100 / 100 | 91 / 100 | 77% |

The first three rows repeat the Day 10 and Day 12 numbers exactly, so the test is repeatable.

## What the numbers show
1. **Combining the searches gave a small, real gain: about 4 more points of the required skills the student already has.** That is 68% to 72% when the role is given, and 73% to 77% with skills only.
2. **Relevance and job level did not change.** With the role given, both systems are already at 100%, so this test cannot show any gain in relevance. It is at its ceiling.
3. **Leaving out the wanted role costs relevance.** With skills only, 19 of 20 profiles got a relevant job and 91 of 100 jobs were relevant, against 100 of 100 when the role is given. Both searches behave the same here.
4. **Job level stays suitable everywhere** because of the Day 12 level score.

## What the side-by-side check showed
I ran five short searches with three methods each (meaning, keyword, combined).
- For each search, all three methods returned jobs with the **same job title**. For example, "React Node.js MongoDB" gave only Node.js Developer jobs from every method, with no React or Full Stack titles.
- The methods differed only in **level and order**. For "React Node.js MongoDB", the combined search dropped the one Senior job. For "Kotlin Android" it moved a Lead and a Senior job to the top, which suits a student less.
- So the narrow results I noted earlier come mostly from the data: each role family seems to have one title, and jobs differ by company and level. This is my reading of five searches and has not been checked across the whole file.

## Problems found
1. **The test cannot separate the two systems on relevance**, because both score 100% with the role given. A harder test is needed.
2. **One profile fails when no role is given.** The details for the failing profile are in `search_eval_results_day13.md` (search for "relevant 0/5"). A likely reason is that its skills do not appear in the job data, but that is not confirmed.
3. **The combined search can promote senior jobs** when no level score is applied (seen for "Kotlin Android").
4. **A 4-point gain on 20 profiles is small** and may not hold on other profiles.

## Mentor check (3 questions refused on Day 11)
Searching with `test_failed3.py` showed that **all three questions found 8 sources** (3 notes and 5 jobs). So the search works, and the refusal comes from the AI step, which refuses when the documents only partly match the wording. This is a likely reason, not a confirmed one. The mentor instruction was changed to answer with whatever the documents show and say what is missing, and to refuse only when the main thing asked for is absent. It will be re-measured.

## Fixes planned
1. **Day 14:** a harder test with exact tool names (for example DAX, Terraform, Airflow). The check is whether the job's skills list really contains the tool. This should show whether the combined search helps.
2. Find the one profile that fails without a role, and say why.
3. Re-test the mentor on the 3 refused questions and 2 questions that must be refused.

## Limits of this test
- "Relevant" means the job title contains one of my listed words.
- The profiles are made up and tidy, and all assume a fresher.
- The 4-point gain comes from 20 profiles and 100 jobs per method.
- Results were judged by me alone.