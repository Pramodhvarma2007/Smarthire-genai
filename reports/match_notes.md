# Job Matching Notes (Day 5)

**Date:** 18 Nov 2026
**AI model used for the "why" lines:** gemini-3.5-flash (backup: gemini-3.5-flash-lite)
**Resumes tested:** 4 sample resumes, 5 jobs shown for each (20 jobs in total)

## How matching works
1. The resume is read and the candidate's skills are collected (the skills list plus tools used in projects).
2. The search finds the 15 jobs closest in meaning to the candidate.
3. Each job gets a **skill match %**: how many of the job's required skills the candidate already has.
4. The final ranking uses half the meaning score and half the skill match %.
5. Each job shows **Have** (matched skills), **Missing** (skills to learn) and a short **Why** line.

## Results

| Resume | Wants | Job title relevant | Experience level suitable | Skill match range |
|---|---|---|---|---|
| resume1_data_analyst | Data Analyst | 5 / 5 | 3 / 5 | 67% to 83% |
| resume2_ml_engineer | Machine Learning Engineer | 5 / 5 | 3 / 5 | 67% to 80% |
| resume3_web_developer | Full Stack Developer | 5 / 5 | 2 / 5 | 80% to 100% |
| resume4_fresher_mixed | Software Developer | 5 / 5 | 1 / 5 | 20% to 33% |

**Job title relevant: 20 / 20 (100%)**
**Title relevant AND level suitable (Fresher or Junior): 9 / 20 (45%)**

All candidates are students or recent graduates, so I counted only Fresher (0-1 yr) and Junior (1-3 yrs) jobs as suitable.

## What worked
- Job titles matched what each candidate wants in all 20 results.
- Skill splits were mostly correct. For example, the web developer resume showed React, Node.js, MongoDB and REST APIs as matched, and Python as the only missing skill for two jobs.
- Missing skills are specific and useful, such as Tableau, PyTorch, MLOps and Kubernetes.
- The "why" lines stayed within the given matched and missing skills and added no new facts.

## Problems found
1. **Senior jobs shown to students.** resume1 got a Senior job (HAL) and a Lead job (Meesho) at the top. resume2 got a Senior job (CRED). resume3 got a Senior job (Paytm) first. The ranking ignores experience level.
2. **Weak matches called a "good fit".** resume4 matches only 25% of skills for most jobs, yet the "why" lines say "this role is a good fit". This is misleading.
3. **Related skills not recognised.** resume1 lists Matplotlib, but "Data Visualization" is shown as missing for two jobs. The skill check only compares words, so it does not know Matplotlib counts as data visualization.
4. **resume4 results are too narrow.** The candidate lists Python, Java, SQL and HTML, but all 5 jobs are Python Developer roles, with only Python matched. Java and SQL jobs never appeared.
5. **The "why" lines sound repetitive.** Many start with "This job fits you well because you already know...".

## Fixes planned
1. Add an experience-level filter or score boost so Fresher and Junior jobs rank first for students.
2. Tell the AI model to say "partial match" when the skill match is below 50%, and never "good fit".
3. Add a small list of related skills (for example Matplot