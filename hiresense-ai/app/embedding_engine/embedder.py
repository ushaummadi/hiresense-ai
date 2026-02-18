from sentence_transformers import SentenceTransformer
from app.config import EMBED_MODEL

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(EMBED_MODEL)

    def embed(self, texts: list[str]) -> list[list[float]]:
        vecs = self.model.encode(texts, normalize_embeddings=True)
        return vecs.tolist()
