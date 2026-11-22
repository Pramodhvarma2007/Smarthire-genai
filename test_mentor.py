from src.mentor.rag_chain import ask_mentor

in_scope = [
    "How do I switch to Data Analyst?",
    "What skills do I need to become a Machine Learning Engineer?",
    "How should I write my resume as a fresher?",
    "What is the difference between junior and senior level jobs?",
    "Which jobs need React and Node.js?",
]
out_of_scope = [
    "What is the capital of France?",
    "Give me a recipe for pasta.",
    "Who won the cricket world cup?",
    "Write a poem about the moon.",
    "What is the best phone to buy?",
]

for title, questions in [("IN SCOPE", in_scope), ("OUT OF SCOPE", out_of_scope)]:
    print("\n" + "#" * 20, title)
    for q in questions:
        r = ask_mentor(q)
        print("\nQ:", q)
        print("A:", r["answer"])
        print("Sources:", [(s["label"], s["title"], s["score"]) for s in r["sources"]])