from backend.app.rag.document_loader import DocumentLoader
from backend.app.rag.embeddings import EmbeddingService
from backend.app.rag.vector_store import VectorStore


class KnowledgeBase:

    def __init__(self, knowledge_base_path: str):

        self.loader = DocumentLoader(
            knowledge_base_path
        )

        self.embedding_service = EmbeddingService()

        self.vector_store = VectorStore()

        self._build()

    def _build(self):

        documents = self.loader.load_documents()

        for document in documents:

            chunks = self.loader.chunk_document(
                document["content"],
                chunk_size=500
            )

            for chunk in chunks:

                vector = self.embedding_service.embed(
                    chunk
                )

                self.vector_store.add(
                    {
                        "source": document["source"],
                        "content": chunk
                    },
                    vector
                )

    def retrieve(
        self,
        query: str,
        top_k: int = 3
    ) -> list[dict]:

        query_vector = self.embedding_service.embed(
            query
        )

        return self.vector_store.search(
            query_vector,
            top_k=top_k
        )