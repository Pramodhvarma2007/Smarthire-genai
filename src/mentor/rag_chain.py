import glob
import os
import pickle
import faiss
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import NOTES_DIR, NOTES_INDEX_PATH, NOTES_META_PATH, MIN_SCORE
from src.generate.prompts import MENTOR_PROMPT
from src.llm import call_llm
from src.search.embed import embed_texts
from src.search.job_search import search_jobs

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


def retrieve(question, n_notes=3, n_jobs=3):
    parts, sources = [], []
    for doc, score in search_notes(question, n_notes):
        if score >= MIN_SCORE:
            n = len(sources) + 1
            parts.append(f"[{n}] Career note ({doc.metadata['source']}): {doc.page_content}")
            sources.append({"label": n, "type": "note",
                            "title": doc.metadata["source"], "score": round(score, 3)})
    for job in search_jobs(question, top_n=n_jobs):
        if job["score"] >= MIN_SCORE:
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


def ask_mentor(question):
    found = retrieve(question)
    if not found["sources"]:
        return {"answer": NO_ANSWER, "sources": []}
    text = chain.invoke({"question": question, "context": found["context"]})
    return {"answer": text.strip(), "sources": found["sources"]}