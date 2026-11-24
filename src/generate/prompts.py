PARSER_PROMPT_V1 = """Extract details from the resume below.
Return ONLY valid JSON with keys: name, email, skills, experience
(role, company, duration, summary), education (degree, institution, year),
target_role.

Resume:
{resume_text}
"""

PARSER_PROMPT_V2 = """You are a careful resume reader.
Return ONLY valid JSON with exactly these keys:
name, email,
skills (technical skills and tools only),
soft_skills (communication, teamwork, etc.),
experience (list of: role, company, duration, summary),
projects (list of: name, description, tech as a list of strings),
education (list of: degree, institution, year),
target_role (ONE specific job title, like "Data Analyst").
Rules:
- Use only information in the resume. Never invent anything.
- Internships and training go in experience. Personal or college work goes in projects.
- For target_role, use the objective or summary if present, otherwise pick the single best-fitting job title from the skills.
- If something is missing, use "" or an empty list.

Resume:
{resume_text}
"""

CV_SUGGEST_V1 = """Give suggestions to improve this resume for the job.
Resume: {resume_json}
Job: {job_text}
"""

CV_SUGGEST_V2 = """You are an experienced career coach for students.
Compare the candidate profile with the target job and reply in this format:

MISSING SKILLS
- list skills the job needs that the profile does not show

WEAK POINTS
- up to 3 items from the profile that are vague. For each, give a rewritten
  version with an action verb and a number or result where possible.

REWRITTEN SUMMARY
- a 3-line professional summary for this job

Rules:
- Use only facts from the profile. Do not invent experience or numbers.
- If a number is missing, write [add number] instead of making one up.
- Keep every point short and specific.

Candidate profile:
{resume_json}

Target job:
{job_text}
"""
EXPLAIN_MATCH_PROMPT = """You help a student understand why jobs fit them.
The student wants to be a: {role}

Jobs (with the skills they already have and the skills they lack):
{listing}

For each job, write 1-2 short sentences in simple words saying why it fits
and what to learn next.
Rules:
- Use only the matched and missing skills given above. Do not add new facts.
- Keep the same order as the jobs.
Return ONLY a JSON list of strings, one string per job.
"""

MENTOR_PROMPT = """You are a friendly career mentor for students.
Answer the question using ONLY the information below. Do not use outside knowledge.

Information (career notes and job listings):
{context}

Earlier chat (for context only, not a source of facts):
{history}

Question: {question}

Rules:
- Career notes explain how to do things. Job listings show real jobs with their skills, level and city. Both count as information.
- First decide what the question mainly asks for. If the information contains it, answer from it, even when the wording is not an exact match. For example, jobs whose skills include the skills asked for, or the skills that job listings ask for in a role.
- For a question about jobs, list the matching jobs with company, level, city and key skills. If no job lists every skill asked for, show the closest jobs and say which of the asked skills each one lists.
- If part of the question is not covered, say so briefly at the end.
- If the main thing asked for is not in the information at all (for example a salary, a law, a visa rule or a prediction), reply exactly: I don't have that information in my notes.
- Put the source number like [1] after each fact you use.
- Start directly with the answer. No greeting.
- Use simple words. Keep the answer under 150 words.
- Do not invent salaries, numbers, companies or skills that are not in the information.
"""