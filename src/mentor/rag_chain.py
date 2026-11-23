import glob
import os
import pickle
import faiss
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import NOTES_DIR, NOTES_INDEX_PATH, NOTES_META_PATH, NOTE_MIN_SCORE, JOB_MIN_SCORE
from src.generate.prompts import MENTOR_PROMPT
from src.llm import call_llm
from src.search.embed import embed_texts
from src.search.job_search import search_jobs
from src.safety.guardrails import check_input

NO_ANSWER = ("I don't have information about that in my career notes or job "
             "data. Try asking about career paths, skills, resumes, "
             "interviews or the jobs in our list.")


def build_notes_index():
    splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
    docs = []
    for path in sorted(glob.glob(os.path.join(NOTES_DIR, "*.txt"))):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        name = os.path.splitext(os.path.basename(path))[0].replace("_", " ")
        for chunk in splitter.split_text(text):
            docs.append(Document(page_content=chunk, metadata={"source": name}))
    if not docs:
        raise ValueError("No .txt files found in data/career_notes")
    vectors = embed_texts([d.page_content for d in docs])
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    faiss.write_index(index, NOTES_INDEX_PATH)
    with open(NOTES_META_PATH, "wb") as f:
        pickle.dump(docs, f)
    print(f"Saved {len(docs)} note pieces from {len(set(d.metadata['source'] for d in docs))} notes")


_index = None
_docs = None


def search_notes(question, top_n=3):
    global _index, _docs
    if _index is None:
        _index = faiss.read_index(NOTES_INDEX_PATH)
        with open(NOTES_META_PATH, "rb") as f:
            _docs = pickle.load(f)
    scores, ids = _index.search(embed_texts([question]), top_n)
    return [(_docs[int(i)], float(s)) for s, i in zip(scores[0], ids[0])]


def retrieve(question, n_notes=3, n_jobs=5):
    parts, sources = [], []
    for doc, score in search_notes(question, n_notes):
        if score >= NOTE_MIN_SCORE:
            n = len(sources) + 1
            parts.append(f"[{n}] Career note ({doc.metadata['source']}): {doc.page_content}")
            sources.append({"label": n, "type": "note",
                            "title": doc.metadata["source"], "score": round(score, 3)})
    for job in search_jobs(question, top_n=n_jobs):
        if job["score"] >= JOB_MIN_SCORE:
            n = len(sources) + 1
            title = f"{job['Job_Title']} at {job['Company']}"
            parts.append(f"[{n}] Job ({title}): skills {job['Skills_Required']}; "
                         f"level {job['Experience_Level']}; city {job['City']}; "
                         f"industry {job['Industry']}")
            sources.append({"label": n, "type": "job",
                            "title": title, "score": job["score"]})
    return {"context": "\n\n".join(parts), "sources": sources}


prompt = PromptTemplate.from_template(MENTOR_PROMPT)
chain = prompt | RunnableLambda(lambda p: call_llm(p.to_string(), temperature=0.2))


def format_history(history, turns=3):
    if not history:
        return "None"
    lines = []
    for m in history[-2 * turns:]:
        who = "Student" if m["role"] == "user" else "Mentor"
        lines.append(f"{who}: {m['text'][:300]}")
    return "\n".join(lines)


def make_search_text(question, history):
    """Short or vague follow-ups borrow the last question."""
    words = question.lower().replace("?", "").split()
    vague = {"it", "that", "this", "they", "them", "there", "those"}
    if history and (len(words) <= 6 or vague & set(words)):
        earlier = [m["text"] for m in history if m["role"] == "user"]
        if earlier:
            return earlier[-1] + " " + question
    return question


def ask_mentor(question, history=None):
    check = check_input(question)
    if not check["ok"]:
        return {"answer": check["message"], "sources": [], "blocked": check["reason"]}
    question = check["clean_text"]

    found = retrieve(make_search_text(question, history))
    if not found["sources"]:
        return {"answer": NO_ANSWER, "sources": []}
    text = chain.invoke({"question": question, "context": found["context"],
                         "history": format_history(history)}).strip()
    if text.lower().startswith("i don't have that information"):
        return {"answer": text, "sources": []}
    return {"answer": text, "sources": found["sources"]}