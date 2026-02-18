import chromadb
from chromadb.config import Settings
from app.config import CHROMA_DIR

COLLECTION = "candidates"

class ChromaStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=CHROMA_DIR,
            settings=Settings(anonymized_telemetry=False)
        )
        self.col = self.client.get_or_create_collection(name=COLLECTION)

    def upsert_candidate(self, candidate_id: str, embedding: list[float], document: str, metadata: dict):
        self.col.upsert(
            ids=[candidate_id],
            embeddings=[embedding],
            documents=[document],
            metadatas=[metadata]
        )

    def query(self, query_embedding: list[float], top_k: int = 10):
        return self.col.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["metadatas", "documents", "distances", "ids"]
        )

    def get(self, candidate_id: str):
        res = self.col.get(ids=[candidate_id], include=["documents", "metadatas"])
        if not res["ids"]:
            return None
        return {
            "id": res["ids"][0],
            "document": res["documents"][0],
            "metadata": res["metadatas"][0],
        }
