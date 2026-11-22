from sentence_transformers import SentenceTransformer
from src.config import EMBED_MODEL

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def embed_texts(texts, batch_size=64):
    vectors = get_model().encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        normalize_embeddings=True,
    )
    return vectors.astype("float32")