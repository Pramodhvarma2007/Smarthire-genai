## Follow-up check (Day 19)

**What changed:** job lists for the mentor now rank by skills named in the question and by student level. Two new career guides (backend developer, QA and software testing) were added, so there are now 13 notes, cut into 50 pieces for search.

| Question | Day 18 | Day 19 |
|---|---|---|
| Which jobs need React and Node.js? | Answered. Jobs shown were Fresher, Lead, Mid and Lead. | Answered. All 5 jobs shown are Fresher. Still says none list Node.js. |
| Show me data analyst jobs that need Power BI. | Answered with 5 Power BI Developer jobs. | Answered. All 5 jobs shown are Fresher. Still says no job is titled Data Analyst. |
| What should I learn to become a backend developer? | Said the notes have no backend roadmap. | Answered in 5 steps from the new backend guide, with source numbers. |
| What is the salary of a Data Analyst at Google? | Refused | Refused, no sources |
| What is the notice period rule under Indian labour law? | Refused | Refused, no sources |

## What improved
1. Jobs shown to students now suit them: all 10 jobs visible in the React and Power BI answers are Fresher (0-1 yr). On Day 18 only 4 of 15 jobs listed suited a student.
2. The missing backend guide is fixed.
3. Both questions that must be refused were still refused.

## Problems still open
1. **The React answer still says no job lists Node.js.** All sources were React Developer jobs. The data has Node.js Developer jobs and Full Stack jobs, so the answer is true only of the 5 jobs shown. The likely cause is that job questions are found by meaning only, and the exact-word search is not used.
2. **The Data Analyst answer says no job is titled "Data Analyst".** That is false for the data, because the search tests on Day 10 and Day 13 returned Data Analyst jobs. Again it is true only of the jobs shown.
3. **Five jobs from one title.** Answers show five jobs with the same title.

## Fix planned
Use the combined search for job questions, give a small boost to jobs whose title words appear in the question, allow at most 3 jobs per title, and add a rule: never say a job title does not exist, only say "among the jobs I found".