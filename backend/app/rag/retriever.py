from backend.app.rag.embeddings import EmbeddingService
from backend.app.rag.vector_store import VectorStore


class Retriever:

    def __init__(self, vector_store: VectorStore):

        self.vector_store = vector_store
        self.embedding_service = EmbeddingService()

    def retrieve(
        self,
        query: str,
        top_k: int = 3
    ) -> list[dict]:

        query_vector = self.embedding_service.embed(
            query
        )

        results = self.vector_store.search(
            query_vector,
            top_k=top_k
        )

        return results