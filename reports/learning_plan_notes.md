# Learning Plan Notes (Day 16)

**Date:** 23 Nov 2026
**What was built:** a 30-day learning plan that teaches only the skills a job asks for and the student lacks, plus an automatic check on every plan
**What the check looks for:** every missing skill is covered, all four weeks are present, no web links, and no salary or promise words
**AI requests:** 7 plans. The model was busy during the test, so several needed more than one try.

## Results

| Profile | Job | Skills to learn | Instruction | Result |
|---|---|---|---|---|
| P01 | Data Analyst | Tableau | V2 (better) | Passed |
| P01 | Data Analyst | Tableau | V1 (weak) | Failed: the Week 1 to Week 4 layout was missing |
| P03 | Data Scientist | Tableau | V2 | Passed |
| P06 | Frontend Developer | TypeScript | V2 | Passed |
| P09 | Backend Developer | Node.js, PostgreSQL | V2 | Failed: contains a web link |
| P14 | DevOps Engineer | Jenkins | V2 | Passed |
| P14 | DevOps Engineer | Jenkins | V1 | Failed: web link and a salary or promise word |

**V2 plans passing all checks: 4 / 5 (80%). V1 plans passing: 0 / 2.**

## What the numbers show
1. **V2 covered every missing skill in all 5 plans.** The "skill not covered" check never fired.
2. **The weak instruction (V1) failed both tests.** One plan had no week layout. The other had a link and a salary or promise word. Only 2 plans were tested, so this is a small sample.
3. **V2 still broke the "no links" rule once (P09), even though the instruction forbids it.** The code check caught it. An instruction alone is not enough, so the check is needed.
4. **Plans were built from the right skills.** The skills to learn came from the job's own list minus what the student already has.

## Problems found
1. **One plan contains a web link.** I have not looked at which link yet. A likely cause is an address like "http://localhost" in a project step, but this is not confirmed.
2. **The checks only test structure.** They cannot tell whether a plan is realistic or correct. Reading at least 2 plans is still to do.
3. **Four of the five plans teach just one skill.** A 30-day plan for one skill may be padded, and the "no more than two new skills per week" rule was barely tested (only P09 had two skills).
4. **Course and website names are not checked.** The check catches links and money words only.
5. **Slow answers.** The busy model returned errors, and each model was tried three times, with waits between tries. This is a likely reason for slow answers (such as the 23.5 seconds on Day 11), but it is a guess.

## Fixes planned
1. Open `plan_samples.md`, find the link in P09, and decide whether to tighten the instruction or remove links automatically.
2. When a check fails, ask again once, then show the second answer.
3. Move to the next model right away when one is busy, instead of retrying it (Day 17).
4. Read 2 plans and note whether they are realistic for 2 hours a day.

## Limits
- Only 5 profiles were tested, and each plan was generated once.
- The student skills and jobs are made up.
- Results were judged by the automatic check and by me alone.