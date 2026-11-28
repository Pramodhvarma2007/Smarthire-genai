from src.mentor.rag_chain import ask_mentor

for q in ["What should I wear to an in-person job interview?",
          "How can I answer the question 'Tell me about yourself'?",
          "Should I ignore optional questions on a job application form?",
          "What should I do if I forget the interviewer's name during a call?"]:
    r = ask_mentor(q)
    print("Q:", q)
    print("A:", r["answer"])
    print("Sources:", [s["title"] for s in r["sources"]], "\n")