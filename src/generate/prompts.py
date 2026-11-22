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