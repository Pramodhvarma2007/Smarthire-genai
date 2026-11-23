# Mentor Notes (Day 6)

**Date:** 18 Nov 2026
**AI model used:** gemini-3.5-flash (backup: gemini-3.5-flash-lite)
**Closeness cut-off (MIN_SCORE):** 0.30
**Sources the mentor can use:** career notes (written with AI help, then checked by me, plus extra notes such as "common resume mistakes for freshers") and the 5,000 job listings

## How the mentor works
1. The question is compared with the career notes and the job listings, and the closest ones are picked.
2. Anything below the cut-off score is thrown away.
3. If nothing is left, the mentor refuses right away, **without asking the AI model at all**. This is the strongest protection against made-up answers.
4. Otherwise the AI model answers using only the picked pieces, with a source number like [1] after each fact.

## Test results

| Test | Result |
|---|---|
| Good questions answered correctly | 4 / 5 |
| Answers that showed source numbers | 4 / 4 |
| Out-of-scope questions refused | 5 / 5 |
| Out-of-scope questions that wrongly got an answer | 0 / 5 |

## In-scope questions

| Question | Answer quality | Sources used | Best note score | Best job score |
|---|---|---|---|---|
| How do I switch to Data Analyst? | Good: 4 clear steps, all from the notes | [1] to [4] | 0.647 | 0.663 |
| What skills do I need to become a Machine Learning Engineer? | Good: maths, coding, data tools, core ML, deep learning | [1], [3] | 0.728 | 0.723 |
| How should I write my resume as a fresher? | Mostly good, but one odd sentence (see problems) | [1] to [3] | 0.831 | 0.421 |
| What is the difference between junior and senior level jobs? | Good: clear levels from the notes | [2] | 0.569 | 0.424 |
| Which jobs need React and Node.js? | **Wrong refusal** ("I don't have that information") | none | 0.445 | 0.666 |

## Judging the answers
Each answer was judged on correctness, sticking to the documents, and helpfulness.

| Question | Correct | Sticks to documents | Helpful |
|---|---|---|---|
| Data Analyst switch | Yes | Yes | Yes |
| ML Engineer skills | Yes | Yes | Yes |
| Fresher resume | Partly | Yes | Yes |
| Junior vs senior | Yes | Yes | Yes |
| React and Node.js jobs | No | n/a | No |

## Out-of-scope questions (made-up answer check)

| Question | Result |
|---|---|
| What is the capital of France? | Refused |
| Give me a recipe for pasta. | Refused |
| Who won the cricket world cup? | Refused |
| Write a poem about the moon. | Refused |
| What is the best phone to buy? | Refused |

**Refused 5 / 5.** All five were refused before any AI call, because nothing in our documents came close enough. They also showed an empty source list.

## Problems found
1. **Wrong refusal on a job question.** For "Which jobs need React and Node.js?", the search found three good React Developer jobs (scores around 0.66), yet the mentor said it had no information. The instruction says "if the information does not answer the question", and the model did not treat the job listings as information.
2. **Sources shown after a refusal.** The refused React question still displayed 6 sources, which is confusing.
3. **Unrelated jobs counted as sources.** In the resume question, jobs like Product Manager at Razorpay (score 0.42) passed the cut-off, though they have nothing to do with resumes. A cut-off of 0.30 is too low for jobs.
4. **One odd sentence.** The resume answer included "an unprofessional email address? No, use your name for your email", which reads badly. The AI model made a small wording slip.
5. **Every answer starts with "Hello!".** It is repeated and adds nothing.
6. **Daily limit reached on the free plan.** The Google free plan allows only 20 requests per day for this model. Many retries failed with "quota exceeded" (429) or "high demand" (503) before the backup model answered. The retry helper waited on errors that cannot clear for about 16 hours, which wasted time and requests.

## Fixes planned (Day 7)
1. Change the instruction so job listings count as information, and job questions return matching jobs.
2. Hide the sources when the answer is a refusal.
3. Raise the cut-off for jobs (to about 0.45) and keep 0.30 for notes, then re-test.
4. Add the rule "do not start with a greeting".
5. On a daily-limit error, switch straight to the backup model instead of retrying. Save answers already given, so repeated questions cost nothing.
6. Test harder questions: career-related but not in our notes (for example "What is the salary of a Data Analyst at Google?").

## Limits of this test
- Only 5 good and 5 unrelated questions were tested.
- The unrelated questions were easy, because they have nothing to do with careers. Questions close to careers but missing from our notes will be tested next.
- Answers were judged by me alone, without a second person checking.