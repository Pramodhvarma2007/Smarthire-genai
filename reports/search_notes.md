# Job Search Notes

**Date:** 17 Nov 2026

## Setup
- **Jobs used:** 5,000 job postings (Kaggle India tech jobs dataset)
- **Information used for each job:** job title, required skills, industry, experience level, education
- **Matching tool:** a free text-matching tool called all-MiniLM-L6-v2, which runs on my own laptop (no paid service)
- **How it works:** every job is turned into a list of numbers that captures its meaning. The same is done for the search text. The jobs whose numbers are closest to the search text come first.
- **Setup time:** about 27 seconds, done once. The result is saved, so it never has to be repeated.

## Test results

| Search text | Relevant jobs in top 5 | Top match |
|---|---|---|
| Python SQL Excel Power BI data analyst fresher | 5 / 5 | Data Analyst (Leadsquared) |
| React Node.js JavaScript web developer | 5 / 5 | React Developer (Oracle) |
| machine learning TensorFlow Python NLP | 5 / 5 | NLP Engineer (InMobi) |

**Overall hit rate: 15 / 15 (100%)**

A job counted as relevant when its title and skills matched what the search asked for.

## What I noticed
- **Skills lined up.** The jobs found for the data analyst search all asked for SQL, Excel and Power BI. The web developer results all asked for JavaScript, React or Next.js. The machine learning results all asked for TensorFlow, Python, BERT or similar.
- **Match scores differed by search.** Scores were about 0.57 to 0.58 for the data analyst search, 0.68 for the web developer search, and 0.52 to 0.54 for the machine learning search. A higher score does not always mean better results, because the scale is different for each search.
- **Little variety in results.** The data analyst search returned four Power BI Developer jobs and only one Data Analyst job. The machine learning search returned only NLP Engineer jobs. The results are correct but similar to each other.
- **Easy to read.** Each result shows the company and the skills, so a user can quickly see why a job was chosen.

## Limitations
- Only 3 searches were tested, so the 100% result is a small sample and not a final score. A bigger test with more profiles is planned for evaluation day.
- The searches asked for a fresher, but I did not check whether the returned jobs were for freshers. Experience level is not used to filter yet.
- The dataset looks very tidy (clear titles and short skill lists), so real-world job postings may give lower accuracy.
- The jobs are fixed, from one dataset. New job postings will not appear unless the dataset is updated.

## Next steps
- Show which of my skills match each job and which skills are missing.
- Add a short explanation of why each job was chosen.
- Test with the profiles from my four sample resumes.