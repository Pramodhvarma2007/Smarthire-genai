from src.search.job_search import search_jobs
from src.search.hybrid import keyword_search, hybrid_search

queries = [
    "React Node.js MongoDB",
    "Power BI DAX data modeling",
    "Selenium Postman API testing",
    "Kotlin Android",
    "Frontend Developer",
]
for q in queries:
    print("\nQUERY:", q)
    for name, fn in (("Meaning", search_jobs), ("Keyword", keyword_search), ("Hybrid ", hybrid_search)):
        res = fn(q, top_n=5)
        print(f"  {name}:", [f"{r['Job_Title']} ({str(r['Experience_Level']).split(' ')[0]})" for r in res])