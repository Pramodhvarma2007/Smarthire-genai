from src.llm import call_llm

TOPICS = {
    "interview_day_basics": "Interview day basics for freshers: what to wear, when to arrive, how to calm nerves, and what to do if you forget a name or a question",
    "common_interview_questions": "How freshers can answer common interview questions, including 'Tell me about yourself', strengths and weaknesses, and 'Why should we hire you'",
    "job_application_forms": "How to fill in a job application form: required and optional fields, what to write, and mistakes to avoid",
}

PROMPT = """Write a career guide for students on this topic: {topic}
Rules:
- 300 to 400 words, simple words, short headings.
- Practical steps and a suggested order.
- Do NOT include salary numbers, statistics or company names.
"""

for name, topic in TOPICS.items():
    text = call_llm(PROMPT.format(topic=topic), temperature=0.4)
    with open(f"data/career_notes/{name}.txt", "w", encoding="utf-8") as f:
        f.write(topic + "\n\n" + text)
    print("saved", name)