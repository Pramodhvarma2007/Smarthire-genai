from src.search.job_search import search_jobs

queries = [
    "Python SQL Excel Power BI data analyst fresher",
    "React Node.js JavaScript web developer",
    "machine learning TensorFlow Python NLP",
]
for q in queries:
    print("\nQUERY:", q)
    for r in search_jobs(q):
        print(r["score"], "|", r["Job_Title"], "|", r["Company"], "|", r["Skills_Required"])