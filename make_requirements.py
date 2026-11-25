from importlib.metadata import version, PackageNotFoundError

PACKAGES = ["streamlit", "pandas", "numpy", "faiss-cpu", "sentence-transformers",
            "rank-bm25", "python-docx", "pypdf", "pydantic", "python-dotenv",
            "google-genai", "langchain-core", "langchain-text-splitters"]
lines = []
for name in PACKAGES:
    try:
        lines.append(f"{name}=={version(name)}")
    except PackageNotFoundError:
        print("NOT INSTALLED:", name)

with open("requirements.txt", "w") as f:
    f.write("\n".join(lines) + "\n")
print("\n".join(lines))