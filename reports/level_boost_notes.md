# Level Boost Notes (Day 12)

**Date:** 24 Nov 2026
**What was done:** added a job-level score to the job ranking, then ran the same 20 test profiles again
**Cost:** no AI requests (local search only)

## The change
- **Before (Day 9 system):** jobs were chosen by the wanted role, then ranked 60% by closeness and 40% by how many of the job's skills the student already has. Job level was ignored.
- **After (Day 12 system):** the 50 closest jobs for the role are ranked 40% closeness, 25% skills the student has and 35% job level. Level scores: Fresher 1.0, Junior 0.8, Mid 0.2, Senior 0, Lead 0.
- The weights were fixed before the test.

## Results (20 profiles, top 5 jobs each, 100 jobs per method)

| Method | Profiles with 1+ relevant job | Relevant jobs | Suitable level (Fresher or Junior) | Relevant AND suitable level | Average skills the student has |
|---|---|---|---|---|---|
| Meaning search only | 20 / 20 (100%) | 97 / 100 (97%) | 60 / 100 (60%) | 57 / 100 (57%) | 69% |
| Day 9 system (role first, then skills) | 20 / 20 (100%) | 100 / 100 (100%) | 52 / 100 (52%) | 52 / 100 (52%) | 76% |
| Day 12 system (with level boost) | 20 / 20 (100%) | 100 / 100 (100%) | 100 / 100 (100%) | 100 / 100 (100%) | 62% |

## What the numbers show
1. **Jobs that suit a student rose from 52% to 100%.** The 48 Mid, Senior and Lead jobs that were shown on Day 10 no longer appear.
2. **Relevance was kept.** All 100 jobs still have a relevant title.
3. **The test is repeatable.** The Day 9 row gave exactly the Day 10 numbers (52%, 52%, 76%), so the test gives the same answer every time.
4. **Example, profile P01 (Data Analyst).** Day 9 system: only 1 of 5 jobs suited a student (Senior, Senior, Fresher, Lead, Mid). Day 12 system: all 5 of 5.
5. **There is a cost.** The average share of required skills the student already has fell from 76% to 62%. This is probably because fresher and junior jobs ask for different skills than the senior jobs that matched this student's skills. This is a guess and is not confirmed.

## Honest warnings
- **100% is not a proof that the search is perfect.** The level score rewards exactly what the test measures, so the test was always going to show a big rise.
- The 20 test profiles all assume a fresher. An experienced person would be shown the wrong jobs by this setting.
- A lower skills score means more to learn for each job. That is useful for a student, but it should be shown clearly in the app.

## Mentor: the 3 questions that failed on Day 11
The Day 11 counts (17 answered, 17 passed) mean these three were all refusals:

| Question | Type | Automatic checks |
|---|---|---|
| Which jobs need React and Node.js? | job question | source numbers not valid, wrong topic, failed |
| Show me data analyst jobs that need Power BI. | job question | source numbers not valid, wrong topic, failed |
| What should I learn to become a backend developer? | career guide question | source numbers not valid, wrong topic, failed |

- The React question has been refused on Day 6, Day 7 and Day 11, even after the Day 7 fix.
- **The cause is not confirmed.** Possible causes: nothing passed the closeness cut-off, so the AI model was never asked; or jobs were found but the AI model judged they do not answer the question; or, for the backend question, there may be no backend developer guide in the career notes.
- A free check on Day 13 will tell these causes apart.

## Problems still open
1. 3 of 20 career questions are wrongly refused (cause not confirmed).
2. New mentor answers take 23.5 seconds on average, which is too slow for a chat.
3. The level setting assumes the user is a student.
4. Results for each role often share one job title, so related titles rarely appear (planned for the keyword search).

## Fixes planned
1. Day 13: run a free check on the 3 refused questions, then build a search that also uses exact keywords, and test it.
2. If confirmed, add a backend developer guide to the career notes.
3. Day 19: add a "your level" choice to the app, so experienced users can see senior jobs.
4. Find out where the 23.5 seconds go, and shorten it.

## Limits of this test
- "Relevant" means the job title contains one of my listed words.
- The profiles are made up and tidy, and all assume a fresher.
- Only the top 5 results were checked, and results were judged by me alone.