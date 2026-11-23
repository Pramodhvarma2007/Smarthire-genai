# Mentor Evaluation Notes (Day 11)

**Date:** 20 Nov 2026
**What was tested:** 30 questions, written in advance, asked to the career mentor
**Cost:** about 19 AI requests (the other questions were stopped earlier or already saved)

## The 30 questions
1. **20 career questions** the documents can answer: careers, skills, resumes, interviews, job levels and questions about the job list.
2. **5 unrelated questions** (weather, science, politics, translation, maths). The mentor should refuse.
3. **5 career-sounding questions our documents cannot answer** (for example a salary at Google, visa rules, labour law). The mentor should refuse, and it must not invent an answer.

## Automatic checks on the 20 career questions
An answer passes only if all four are true: it is not a refusal, every [1] style source number points to a real source, at least one source is on the right topic, and it contains no number that is missing from the documents.

## Results

| Measure | Result |
|---|---|
| Questions not run (AI limit reached) | 0 |
| Career questions answered (not refused) | 17 / 20 (85%) |
| Source numbers present and valid | 17 / 20 (85%) |
| A source on the right topic was used | 17 / 20 (85%) |
| No possible invented numbers | 20 / 20 (100%) |
| **Passed ALL automatic checks** | **17 / 20 (85%)** |
| Unrelated questions refused | 5 / 5 (100%) |
| Unrelated questions refused before any AI call | 5 / 5 (100%) |
| Questions our documents cannot answer: refused | 5 / 5 (100%) |
| Of those, stopped before any AI call | 3 / 5 |
| Average time for a new AI answer | 23.5 seconds (19 answers) |

## What the numbers show
1. **No invented answers were found.** All 10 questions that should be refused were refused, and no answer contained a number missing from our documents.
2. **Unrelated questions cost nothing.** All 5 were stopped before any AI call, so they used no daily limit.
3. **The AI model also refuses by itself.** For 2 of the 5 questions that our documents cannot answer, the search found documents that were somewhat close, so the AI model was asked. It still replied that it did not have that information. This shows the instruction "use only the information given" works, not just the closeness cut-off.
4. **85% of career questions were answered correctly by the automatic checks.** 17 answers had valid source numbers and a source on the right topic.
5. **The 3 failures were all refusals.** The three counts match exactly (17, 17, 17, 17), so every answered question passed, and the 3 that failed are the 3 refused career questions. The mentor was too careful on those, which is the safer kind of mistake, but still a weakness.

## Problems found
1. **3 career questions were wrongly refused.** Which ones, and why, is not checked yet. The list is in the results file under "passed = False".
2. **New answers take 23.5 seconds on average.** This is too slow for a chat. The likely cause is waiting while the helper moves through backup models when daily limits run out (the terminal showed "limit reached, trying next model"). This is a guess and has not been confirmed.
3. **The automatic checks do not judge quality.** They check sources and numbers. They cannot tell whether an answer is correct or helpful, so I still need to read the answers.
4. **The "invented numbers" check only looks at numbers.** An invented skill name or company would not be caught.

## Still to do
- Read the answers myself and score at least 10 of them for correctness, sticking to the documents, and helpfulness (0 to 2 each).
- Find the 3 refused questions and fix the cause.
- Find out what is making new answers slow.

## Limits of this test
- The questions were written by me, so they may be easier than real students' questions.
- Only the first answer to each question was checked, with no follow-up messages.
- Questions were judged by words in source titles, so a good answer with an unusual source title could be marked as failing.
- Answers were judged by me alone.