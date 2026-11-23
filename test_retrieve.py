from src.mentor.rag_chain import retrieve, make_search_text

questions = [
    "Which jobs need React and Node.js?",
    "How do I become a Data Analyst?",
    "What is the capital of France?",
    "What is the salary of a Data Analyst at Google?",
]
for q in questions:
    r = retrieve(q)
    print("\nQ:", q)
    for s in r["sources"]:
        print("  ", s["label"], s["type"], s["title"], s["score"])
    if not r["sources"]:
        print("   (nothing found, so the mentor will refuse)")

history = [{"role": "user", "text": "How do I become a Data Analyst?"}]
print("\nMemory check:", make_search_text("What skills do I need for it?", history))