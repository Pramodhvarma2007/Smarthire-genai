# Search Accuracy Notes (Day 10)

**Date:** 19 Nov 2026
**What was tested:** how well the job search finds suitable jobs for a student
**Cost:** no AI requests, because this test only uses the local search

## How the test works
1. I wrote **20 test profiles** (data analyst, machine learning, web, backend, mobile, testing, cloud, security, design and more). Each has a wanted role and a list of skills.
2. For each profile I listed in advance which **job title words** count as relevant. These were written before the test was run.
3. For each profile, the search returned its **top 5 jobs**, so 100 jobs were checked per method.
4. Two methods were compared:
   - **Meaning search only:** searches with the role plus the skills, and shows the closest jobs.
   - **Current system:** searches by the wanted role, takes the 30 closest jobs, then ranks them by meaning and by how many of the job's skills the student already has.
5. Four things were measured:
   - **Profiles with 1+ relevant job:** did the top 5 contain at least one relevant job?
   - **Relevant jobs:** how many of the 100 jobs have a relevant title?
   - **Suitable level:** how many are Fresher or Junior jobs, which suit a student?
   - **Relevant AND suitable level:** both at once. This is the most useful number.

## Results

| Method | Profiles with 1+ relevant job | Relevant jobs | Suitable level (Fresher or Junior) | Relevant AND suitable level | Average skills the student has |
|---|---|---|---|---|---|
| Meaning search only | 20 / 20 (100%) | 97 / 100 (97%) | 60 / 100 (60%) | 57 / 100 (57%) | 69% |
| Current system (role first, then skills) | 20 / 20 (100%) | 100 / 100 (100%) | 52 / 100 (52%) | 52 / 100 (52%) | 76% |

All 20 profiles were scored. None were skipped, so the data has jobs for every profile type.

## What the numbers show
1. **Job titles are found very reliably.** Both methods found at least one relevant job for all 20 profiles. The current system got all 100 results relevant, against 97 for plain meaning search.
2. **The current system picks jobs that match the student's skills better.** On average the student already has 76% of the required skills, against 69%.
3. **The current system is worse at job level.** Only 52% of its jobs are Fresher or Junior, against 60% for plain meaning search. After ranking, the "relevant and suitable level" score is 52%, against 57%.
4. **Example, profile P01 (Data Analyst):**
   - Meaning search: 4 of 5 jobs suited a student (3 Fresher, 1 Junior, plus 1 Lead job).
   - Current system: only 1 of 5 suited a student. It showed Senior, Senior, Fresher, Lead and Mid jobs.

## Why this matters
The role fix on Day 9 solved a real bug: changing the role to Web Developer gave Data Analyst jobs. But choosing jobs by role alone also brings in more senior jobs. So fixing one problem made another one worse. This is the weakness already noted on Day 5, and it is now measured.

## Problems found
1. **The current system shows too many senior jobs to students.** Fewer than 6 in 10 results suit a fresher, and 48 of the 100 jobs shown were Mid, Senior or Lead.
2. **The cause of the drop in suitable jobs is a likely guess, not confirmed.** The most likely reason is that the role-first search ignores the student's level.
3. **Results are narrow.** The top 5 for a profile often share the same job title, so related titles (for example Full Stack for a Frontend profile) rarely appear.
4. **The "relevant" test is lenient.** It only checks title words. It does not check whether the student's skills really fit the job, so 100% does not mean 100% good matches.
5. **Only 20 profiles were tested.** A difference of 3 jobs out of 100 (97 against 100) is small and could change with other profiles.

## Fixes planned
1. **Day 12:** add a level boost so Fresher and Junior jobs rank higher for students, then run the same test again. The aim is to raise "relevant and suitable level" above the 57% from plain meaning search, without losing relevance.
2. **Days 13 and 14:** build a search that also uses keywords, so more job titles appear, then compare it with these numbers.
3. **Day 15:** compare two search models on the same 20 profiles.

## Limits of this test
- "Relevant" is judged only by words in the job title, with word lists I wrote.
- The profiles are made up and tidy. Real resumes are messier.
- Level suitability assumes the student is a fresher or junior, which fits most of this class but not everyone.
- The job data has no job descriptions, only titles and skills.
- Only the top 5 results were checked, and results were judged by me alone.