# Search Model Comparison Notes (Day 15)

**Date:** 22 Nov 2026
**What was tested:** two search models, MiniLM (the current one) and BGE small, on the same 5,000 jobs, 20 test profiles and 23 exact-tool searches
**Cost:** no AI requests. My real job index was not touched.

## Switching rule (set before the test was run)
Switch to the new model only if it beats MiniLM by at least 3 points on BOTH "skills only: relevant jobs" and "exact tools: jobs listing ALL tools", and a search takes less than 3 times as long. Otherwise keep MiniLM.

## Results

| Measure | MiniLM (current) | BGE small |
|---|---|---|
| Role + skills: profiles with 1+ relevant job | 20 / 20 (100%) | 20 / 20 (100%) |
| Role + skills: relevant jobs | 97 / 100 (97%) | 100 / 100 (100%) |
| Skills only: profiles with 1+ relevant job | 18 / 20 (90%) | 20 / 20 (100%) |
| Skills only: relevant jobs | 86 / 100 (86%) | 97 / 100 (97%) |
| Skills only: relevant AND Fresher or Junior | 57 / 100 (57%) | 46 / 100 (46%) |
| Exact tools: searches with 1+ job listing ALL tools | 20 / 23 (87%) | 21 / 23 (91%) |
| Exact tools: jobs listing ALL tools | 91 / 115 (79%) | 87 / 115 (76%) |
| Time to turn all jobs into numbers (one time) | 27 seconds | 53 seconds |
| Average time per search | 8 ms | 12 ms |
| Length of each job's list of numbers | 384 | 384 |

## Applying the rule

| Condition | Result | Passed? |
|---|---|---|
| Skills only: relevant jobs better by 3+ points | 86% to 97% (+11) | Yes |
| Exact tools: jobs listing ALL tools better by 3+ points | 79% to 76% (3 points worse) | No |
| Search time under 3 times as long | 1.5 times | Yes |

**Decision: keep MiniLM.** One condition failed.

## What the numbers show
1. **When the job role is not given, BGE finds clearly more relevant job titles.** 97% against 86%, and every profile got at least one relevant job (20 of 20 against 18 of 20).
2. **When a role is given, both models do well.** BGE got all 100 jobs relevant against 97 for MiniLM, a small gap.
3. **For exact tool names, MiniLM lists all the tools in more jobs.** 91 against 87 jobs. BGE did find at least one such job in one more search (21 against 20 of 23).
4. **Both models are fast enough.** A search takes 8 to 12 milliseconds. Turning the jobs into numbers takes about twice as long for BGE, but this is done only once.
5. **Index size is the same** (384 numbers per job for both).
6. **BGE returned fewer Fresher and Junior jobs (46 against 57).** This comparison uses the raw search only, without the Day 12 level score, so it says nothing about the final ranking. The effect on the final system was not tested.

## Honest warnings
- The model differences on exact tools are small (4 jobs out of 115, 1 search out of 23).
- The skills-only gap (11 points) is the clearest finding, but it comes from 20 profiles whose accepted titles I wrote.
- The test compares raw search results, not the final ranking the app shows.
- One profile (P08, Full Stack) is marked wrong in both models because my accepted-title list is strict (noted on Day 14).

## Idea for later (not done)
Since BGE is better when no role is given, it could be tried only for resumes without a clear job goal. It would need a second index (about 53 seconds to build) and a test in the final ranking. This was not tested.

## Limits
- Only two models were compared, both of a similar small size.
- Relevance was judged by title words and tool lists I wrote.
- Results were judged by me alone.