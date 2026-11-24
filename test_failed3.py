from src.mentor.rag_chain import retrieve

questions = [
    "Which jobs need React and Node.js?",
    "Show me data analyst jobs that need Power BI.",
    "What should I learn to become a backend developer?",
]
for q in questions:
    r = retrieve(q)
    print("\nQ:", q)
    if not r["sources"]:
        print("   Nothing passed the closeness cut-off, so the mentor refuses without asking the AI.")
    for s in r["sources"]:
        print("  ", s["label"], s["type"], s["title"], s["score"])