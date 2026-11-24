# Exact-Tool Search Notes (Day 14)

**Date:** 24 Nov 2026
**What was tested:** 25 searches made of exact tool names (for example DAX, Terraform, Airflow), with three search methods
**How a result was judged:** a job counts only if its skills list really contains the tools searched for
**Cost:** no AI requests

## Which profile fails when no job role is given
When the role is left out, 3 of the 20 test profiles lost relevant jobs:

| Profile | Skills given | Relevant in top 5 | What came back |
|---|---|---|---|
| P01 Data Analyst | Python, SQL, Excel, Power BI, Pandas, Statistics | 3 / 5 | 2 Data Scientist jobs, 3 Data Analyst jobs |
| P04 Machine Learning Engineer | Python, TensorFlow, Scikit-learn, Docker | 3 / 5 | 3 Machine Learning Engineer jobs, 2 Python Developer jobs |
| P08 Full Stack Developer | React, Node.js, MongoDB, REST APIs | 0 / 5 | 5 Node.js Developer jobs |

- The missed jobs add up to 2 + 2 + 5 = 9, which matches the Day 13 figure of 91 / 100 exactly.
- **P08 is probably a limit of my test, not a search failure.** My list of accepted titles only counts "full stack" or "MERN", so Node.js Developer jobs were marked wrong. Those jobs list the same skills, so they may suit this student. This is my reading and has not been checked job by job.
- The P01 and P04 results show the same thing: a Data Scientist job or a Python Developer job is close to the wanted role, but not on my word list.

## Results (23 searches scored, 5 jobs each, 115 jobs per method)

| Method | Searches with 1+ job listing ALL tools | Jobs listing ALL tools | Jobs listing at least one tool | Average different job titles in top 5 |
|---|---|---|---|---|
| Meaning search only | 20 / 23 (87%) | 91 / 115 (79%) | 114 / 115 (99%) | 1.1 |
| Keyword search only | 21 / 23 (91%) | 103 / 115 (90%) | 115 / 115 (100%) | 1.4 |
| Combined (meaning + keyword) | 22 / 23 (96%) | 101 / 115 (88%) | 115 / 115 (100%) | 1.1 |

2 of the 25 searches were skipped because no job in the data lists those tools together: Flutter + Dart, and Go + Microservices.

## What the numbers show
1. **Adding exact-word matching helps.** Compared with meaning search alone, the combined search put jobs that list ALL the tools in 10 more of the 115 slots (79% to 88%), and found at least one such job in 2 more searches (20 to 22 of 23).
2. **Keyword search and the combined search are almost equal.** The gap is 2 jobs out of 115 and 1 search out of 23, which is too small to call a winner.
3. **The combined search never missed all the tools.** It found a full match in 22 of 23 searches, the highest of the three.
4. **Job titles are still very narrow.** Every method averaged only 1.1 to 1.4 different titles in the top 5. Combining the searches did not add variety.
5. **Almost any method finds at least one of the tools** (99% to 100%), so that column cannot separate them.

## Honest warnings
- **The test favours keyword search.** It checks the skills list, and keyword search reads that same list directly. So the keyword result is partly built in.
- Only 23 searches were scored, and the three methods differ by a few jobs. These are small samples.
- Searches that no job could satisfy were skipped, which makes the numbers look better than a real user would see.

## Decision
Use the **combined search** in the app. It keeps the meaning search's understanding of similar words, and it cut the misses on exact tool names. The app will be switched over on Day 19.

## Problems still open
1. Results share one job title (the 1.1 to 1.4 average above).
2. The accepted-title list is strict, so P08 looks like a failure when it may not be.
3. The mentor fix (3 refused questions) has not been checked yet.

## Limits
- Tool lists were written by me, with common tool combinations.
- Results were judged by me alone.
- The job data has no job descriptions, only titles and skills.