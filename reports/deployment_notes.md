# Deployment Notes (Day 20)

**Date:** 25 Nov 2026
**Goal:** put the app online on Streamlit Community Cloud (free) and check the repo is safe to publish
**Live app link:** [fill in]

## Preparing the repo
1. **Key setup.** The online app cannot read my `.env` file, because Git never uploads it. The key is now read from the app's Secrets box when no `.env` is found. The key is never in the code.
2. **Search files.** The app needs 4 saved search files in `vectorstore/`. They were blocked by `.gitignore`, so 4 exceptions were added. `git status` then listed exactly those 4 files as new, and did not list `.env` or `llm_cache.json` (the saved AI answers, which can hold resume details).

| File | Size |
|---|---|
| jobs.faiss | 7.7 MB |
| jobs_meta.pkl | 1.5 MB |
| notes.faiss | 0.1 MB |
| notes_meta.pkl | 0.0 MB |
| **Total** | **about 9.3 MB** |

3. **Sample resume button.** Judges can click "Try a sample resume" and do not need to upload their own.
4. **Exact package versions.** `requirements.txt` was rewritten with the exact versions installed on my computer, because the saved search files are Python pickles that can break if versions differ. Three packages nothing imports (`langchain`, `langchain-community`, `langchain-openai`) were dropped.

| Package | Version |
|---|---|
| streamlit | 1.67.0 |
| pandas | 3.1.1 |
| numpy | 2.5.5 |
| faiss-cpu | 1.16.0 |
| sentence-transformers | 6.3.0 |
| rank-bm25 | 0.2.2 |
| python-docx | 1.2.0 |
| pypdf | 7.1.0 |
| pydantic | 2.14.3 |
| python-dotenv | 1.2.4 |
| google-genai | 3.4.0 |
| langchain-core | 1.8.1 |
| langchain-text-splitters | 1.1.3 |

My computer runs Python 3.14.6.

5. **Repo check.** A small script lists files that must be on GitHub, files that must not, and the packages in `requirements.txt`.

## What the repo check found
- **One problem:** `data/jobs/jobs.csv`, the 5,000-job list, had been uploaded to GitHub at some point, and the check flagged it as a file that must not be there.
- **Fix:** `git rm --cached data/jobs/jobs.csv`, then `git add .` and run the check again. The file stays on my computer. It also stays in older commits on GitHub, which matters only if the dataset's license forbids sharing.
- Status after the fix: [fill in: "READY TO PUSH" shown, yes or no]
- **Dataset license on Kaggle:** [fill in: what it says, and whether sharing is allowed]

## Mentor re-check done today (5 questions, same as Day 18)
The job lists now come from the combined search, with a small boost for title words in the question, a limit of 3 jobs per title, and a rule never to say a job title does not exist.

| Question | Day 18 | Today |
|---|---|---|
| Which jobs need React and Node.js? | Only React Developer jobs. Said none list Node.js. | Found a Full Stack Developer at Ola (Fresher, Hyderabad) that lists Node.js and React. Sources include a Node.js Developer job too. |
| Show me data analyst jobs that need Power BI. | Five Power BI Developer jobs. Said no job is titled Data Analyst. | Two Data Analyst jobs that list Power BI: Capgemini (Fresher, Remote) and Khatabook (Fresher, Pune). |
| What should I learn to become a backend developer? | Said the notes had no backend roadmap. | Five steps from the new backend guide, then backend jobs, with source numbers. |
| What is the salary of a Data Analyst at Google? | Refused | Refused, no sources |
| What is the notice period rule under Indian labour law? | Refused | Refused, no sources |

All 3 job and learning questions now get a good answer, and both questions that must be refused were still refused. The full 30-question test has not been re-run since this change.

## Putting it online
- Python version chosen on Streamlit Community Cloud: [fill in]
- First build time: [fill in]
- First load time: [fill in]
- Separate AI key created in a new Google project for the online app: [fill in: yes or no]

## Live tests
| Test | Result |
|---|---|
| Sample resume button | [fill in] |
| Upload my own resume, level "Student or fresher" | [fill in] |
| 30-day plan | [fill in] |
| Tailored resume and Word download | [fill in] |
| Mentor: backend developer question | [fill in] |
| Mentor: capital of France (should be refused) | [fill in] |
| Mentor: "Ignore previous instructions" (should be blocked) | [fill in] |

## Problems and how I fixed them
[fill in each problem you hit, with the error message, and what fixed it]

## Risks I know about
1. **Free AI limit.** The daily limit is per project, and anyone with the link can use it up. The online app should use its own key, and a recorded demo is the backup.
2. **Free apps can go to sleep** when unused, so the link should be opened a few minutes before a demo.
3. **Memory.** The search model and its libraries are large, and the hosting site's memory is limited.
4. **The search files are pickles,** so a package version change can break loading. The versions are pinned to avoid this.

## Limits
- Only the 5-question mentor re-check was repeated after the change, and answers were judged by me alone.
- The deployment was tested by me on a few sample actions, not by other users.