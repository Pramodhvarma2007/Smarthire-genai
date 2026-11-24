# Resume Rewrite Notes (Day 17)

**Date:** 24 Nov 2026
**What was built:** a tool that rewrites a resume for a chosen job and saves it as a Word file
**AI requests:** about 4 rewrites

## How it keeps the resume honest
- The AI model never sees the name, email or wanted role. Code adds the name and email back.
- The AI may change only the wording of the summary and bullet lines.
- Companies, dates, degrees and schools are copied by code from the real resume.
- The skills list is filtered by code to the student's own skills, and none is dropped.
- A check fails the rewrite if it contains a number that is not in the original resume, or names a skill that the job wants and the student lacks.
- The phone number is never stored, so the file has "[add phone number]" to fill in by hand.

## Results

| Resume | Job chosen | Level | Checks | Word file readable |
|---|---|---|---|---|
| resume1_data_analyst | Data Analyst | Fresher | Passed | Yes |
| resume2_ml_engineer | Machine Learning Engineer | Fresher | Passed | Yes |
| resume3_web_developer | Full Stack Developer | Junior | Passed | Yes |
| resume4_fresher_mixed | Software Engineer | Fresher | Passed | Yes |

**Rewrites passing all automatic checks: 4 / 4. Word files readable: 4 / 4.**
All four jobs suit a student (Fresher or Junior), which shows the Day 12 level score at work.

## Other fix tested
For resume3, the main model was busy and the tool moved to the next model at once, instead of waiting through three tries. The test finished normally.

## Still to check by reading (tick when done)
- [ ] Opened one Word file in Word: it looks tidy and fits on one page
- [ ] Compared Before and After for at least two resumes: no invented facts
- [ ] The wording sounds natural for a student

## Problems and limits
1. **The checks do not cover everything.** They catch new numbers and skills the student lacks, but not an invented sentence or tool that the job does not list.
2. **Only 4 resumes were tried, and each once.** The Word file for a resume that was read from a .docx has not been tested.
3. **The page layout depends on resume length.** A long resume may run past one page.
4. **Results were judged by an automatic check and by me alone.**