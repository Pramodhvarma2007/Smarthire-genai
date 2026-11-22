# Resume Parser: Test Notes

**Model:** gemini-3.5-flash (with JSON mode and Pydantic validation)
**Test date:** 27 OCT 2026
**Resumes tested:** 4

| Resume | Name | Skills | Experience | Education | Target role | Verdict |
|---|---|---|---|---|---|---|
| resume1_data_analyst | Ananya Reddy | 9 skills | 1 internship | B.Tech CS | Data Analyst | Good |
| resume2_ml_engineer | Rahul Verma | 10 skills | 1 internship | B.E. CS | Machine Learning Engineer | Good |
| resume3_web_deve
## Results
loper | Sneha Kulkarni | 10 skills | 1 internship | B.Sc CS | Full Stack Developer | Good |
| resume4_fresher_mixed | Kiran Patel | 7 skills | Empty | B.Tech IT | "Data and Software" | Needs work |

## What worked
- All 4 resumes returned valid JSON that passed Pydantic validation.
- Name, email and education were extracted for every resume.
- Experience entries had role, company, duration and summary filled in.
- Target role was sensible for 3 of 4 resumes.

## Problems found
1. **Empty experience on the fresher resume.** Check whether resume4 has projects or training that was missed. (Verified: [ x ])
2. **Vague target role.** Resume4 gave "Data and Software", which is two roles mixed together. (Verified: [ x ])
3. **Soft skills mixed with technical skills.** "Communication" and "Teamwork" appear in the skills list, which can weaken job matching later. (Verified: [ x ])
4. **No projects field.** Projects are not captured at all, which hurts fresher resumes the most.

## Planned improvements (Day 3 prompt work)
- Add a `projects` field to the profile.
- Tell the model to put soft skills in a separate list.
- Tell the model to give one specific job title for target_role.
- Re-test resume4 and record the before/after result.

## Accuracy summary (fill in after checking)
- Fields correct: 22 / 24
- Resumes fully correct: 3 / 4