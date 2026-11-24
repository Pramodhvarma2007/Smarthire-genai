from src.mentor.rag_chain import ask_mentor

questions = [
    "Which jobs need React and Node.js?",
    "Show me data analyst jobs that need Power BI.",
    "What should I learn to become a backend developer?",
    "What is the salary of a Data Analyst at Google?",
    "What is the notice period rule under Indian labour law?",
]
for q in questions:
    r = ask_mentor(q)
    print("\nQ:", q)
    print("A:", r["answer"])
    print("Sources:", [(s["label"], s["title"]) for s in r["sources"]])