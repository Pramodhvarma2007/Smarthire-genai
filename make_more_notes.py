from src.llm import call_llm

TOPICS = ["How to become a Backend Developer",
          "How to become a QA and Software Testing Engineer"]

PROMPT = """Write a career guide for students on this topic: {topic}
Rules:
- 300 to 400 words, simple words, short headings.
- Practical steps, tools to learn, and a suggested order.
- Do NOT include salary numbers, statistics or company names.
"""

for topic in TOPICS:
    text = call_llm(PROMPT.format(topic=topic), temperature=0.4)
    name = topic.lower().replace(" ", "_")
    with open(f"data/career_notes/{name}.txt", "w", encoding="utf-8") as f:
        f.write(topic + "\n\n" + text)
    print("saved", name)