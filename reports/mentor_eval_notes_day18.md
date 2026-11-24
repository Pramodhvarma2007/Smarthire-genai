# Mentor Re-check and Notebooks (Day 18)

**Date:** 24 Nov 2026
**What changed in the mentor:** a rewritten instruction. Job listings now count as information, the mentor answers with what the documents show and says what is missing, and it refuses only when the main thing asked for is absent.
**Cost:** 18 new AI answers. The rest were already saved or stopped before any AI call.

## Mentor: the same 30 questions, before and after

| Measure | Day 11 (before) | Day 18 (after) |
|---|---|---|
| Questions not run (AI limit reached) | 0 | 0 |
| Career questions answered (not refused) | 17 / 20 (85%) | 20 / 20 (100%) |
| Source numbers present and valid | 17 / 20 | 20 / 20 |
| A source on the right topic was used | 17 / 20 | 20 / 20 |
| No possible invented numbers | 20 / 20 | 20 / 20 |
| **Passed ALL automatic checks** | **17 / 20 (85%)** | **20 / 20 (100%)** |
| Unrelated questions refused | 5 / 5 | 5 / 5 |
| Unrelated, refused before any AI call | 5 / 5 | 5 / 5 |
| Not in our documents: refused | 5 / 5 | 5 / 5 |
| Not in our documents: stopped before any AI call | 3 / 5 | 3 / 5 |
| Average time for a new AI answer | 23.5 seconds (19 answers) | 3.5 seconds (18 answers) |

## What the numbers show
1. **The 3 wrongly refused questions are fixed.** They are the same three from Day 11: React and Node.js jobs, Power BI data analyst jobs, and what to learn for a backend developer. Passing went from 85% to 100%.
2. **The new instruction did not make the mentor answer things it should refuse.** All 5 unrelated and all 5 "not in our documents" questions were still refused, with the same 3 stopped before any AI call.
3. **No invented numbers in any answer** (20 of 20, as before).
4. **New answers were faster: 3.5 seconds against 23.5.** The likely reasons are the Day 17 change (a busy model hands over to the next one at once, instead of waiting through three tries) and fewer daily-limit waits. This is a guess. Speed also depends on how busy the AI service is at that moment.

## Honest warning: 100% is not 20 good answers
The automatic checks only look at three things: valid source numbers, topic words in a source title, and numbers that are not in the documents. They cannot judge quality. Two answers from the 5-question re-check passed that kind of check but had real weaknesses:
- The React and Node.js answer said no job lists both, but that was true only of the 5 jobs shown. The job data does list them together.
- The Power BI answer returned jobs titled Power BI Developer whose skills lists had no Power BI.

## Notebooks
All three notebooks were created and run:

| Notebook | Size after running |
|---|---|
| 01_embeddings_explore | 10,987 bytes |
| 02_build_faiss | 14,016 bytes |
| 03_rag_prototype | 14,553 bytes |

The running tool stops at the first cell that fails. Nothing was reported and all three files were written, so every cell ran. The warnings in the terminal (event loop, unencrypted local connection) are harmless and come from running notebooks on Windows.

## Problems still open
1. Mentor job lists are found by meaning only, so some answers miss jobs that exist in the data (see the React example).
2. Mentor job lists ignore the student's level: in the 5-question re-check, only 4 of 15 jobs listed were Fresher or Junior.
3. The career notes have no backend developer guide and no QA guide.
4. Answer quality has only been checked automatically.

## Still to do
- [ ] Score at least 10 answers by hand (correct, sticks to documents, helpful: 0 to 2 each)
- [ ] Change the job order and level for mentor answers, then re-run the 5 questions
- [ ] Add the two missing career guides and rebuild the notes search
- [ ] Open the notebooks on GitHub and check the outputs show

## Limits
- The 30 questions were written by me, and only the first answer to each was checked.
- No follow-up questions were tested in this run.
- Answers were judged by an automatic check and by me alone.