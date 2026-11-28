# Resume Reader Accuracy (Day 22)

**Date:** 26 Nov 2026
**What was tested:** how well the reader pulls the right details out of resumes with different layouts
**How:** 8 made-up resumes, built with AI help. The correct answers were written down before testing. Each resume is checked on 8 fields.
**AI requests:** about 7 (the hidden-instruction resume is rejected before any AI call)

## The 8 test resumes
| Resume | Layout |
|---|---|
| t1_standard_fresher | Standard sections, fresher |
| t2_experienced_three_jobs | Standard sections, three jobs |
| t3_career_changer | Standard sections, a teacher moving into data |
| t4_two_column_table | Two-column table layout |
| t5_no_headings_paragraph | Plain paragraphs, no headings |
| t6_messy_formats | Mixed date formats, skills written as a sentence |
| t7_non_tech_marketing | A non-IT field (marketing) |
| t8_hidden_instruction | Normal resume with a hidden instruction for the AI |

## The 8 fields checked
Name, email, skills found (at least 80% of the true list), no invented skills, experience (right number of jobs and the right companies), projects (right number), education (school found), target role.

## Results
| Resume | Fields right | Wrong fields |
|---|---|---|
| t1_standard_fresher | 8 / 8 | none |
| t2_experienced_three_jobs | 8 / 8 | none |
| t3_career_changer | 8 / 8 | none |
| t4_two_column_table | 8 / 8 | none |
| t5_no_headings_paragraph | 8 / 8 | none |
| t6_messy_formats | 8 / 8 | none |
| t7_non_tech_marketing | 8 / 8 | none |
| t8_hidden_instruction | Rejected correctly | The resume contains instructions aimed at the AI, so it was stopped |

| Field | Right |
|---|---|
| Name | 7 / 7 |
| Email | 7 / 7 |
| Skills found | 7 / 7 |
| No invented skills | 7 / 7 |
| Experience | 7 / 7 |
| Projects | 7 / 7 |
| Education | 7 / 7 |
| Target role | 7 / 7 |

**Total: 56 of 56 fields right (100%).**
Hidden-instruction resumes rejected: 1 of 1.
Phone numbers hidden before reaching the AI: [fill in from the last lines of `reports/reader_eval_results.md`, written as x / 8]

## A reader problem found and fixed
The first version of the reader skipped tables. On the two-column resume it read only the name and contact line: [confirm with the check below, I measured 63] characters, against [confirm, I measured 413] with the fixed reader. The profile would have been almost empty. The fixed reader now also reads the text inside tables, and that resume scored 8 of 8.

## Honest warnings
1. **100% on 7 resumes is a good sign, not proof.** The resumes and the answer key were written by me with AI help, in clear English with standard headings, so the test is easier than real life.
2. **The "no invented skills" check is loose.** It only tests that the words of each skill appear somewhere in the resume text.
3. **The "target role" check accepts several words.** For example "software" counts for a backend developer.
4. All test files are Word documents. PDF layouts, scanned image PDFs and resumes in other languages were not tested.
5. The marketing resume was read correctly, but the job list is for tech jobs only, so job matches for non-tech resumes are expected to be weak. This is being checked separately.

## Mentor scoring sheet
A sheet with 10 mentor answers was created (`reports/hand_scoring_sheet.md`). Each answer shows what the mentor was given, so every fact can be checked by hand. One answer used the backup model because the main model's daily limit was reached. Scores: [fill in after scoring]

## Limits
- Only 7 resumes were scored, each once.
- Results were judged by an automatic check, and the answer key was written by me.