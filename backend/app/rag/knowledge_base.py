from backend.app.rag.document_loader import DocumentLoader
from backend.app.rag.embeddings import EmbeddingService
from backend.app.rag.vector_store import VectorStore


class KnowledgeBase:

    def __init__(self, knowledge_base_path: str):

        self.loader = DocumentLoader(
            knowledge_base_path
        )

        self.embedding_service = None

        self.vector_store = VectorStore()

        self._built = False

    def _get_embedding_service(self):

        if self.embedding_service is None:
            self.embedding_service = EmbeddingService()

        return self.embedding_service

    def _build(self):

        if self._built:
            return

        documents = self.loader.load_documents()

        embedding_service = self._get_embedding_service()

        for document in documents:

            chunks = self.loader.chunk_document(
                document["content"],
                chunk_size=500
            )

            for chunk in chunks:

                vector = embedding_service.embed(
                    chunk
                )

                self.vector_store.add(
                    {
                        "source": document["source"],
                        "content": chunk
                    },
                    vector
                )

        self._built = True

    def retrieve(
        self,
        query: str,
        top_k: int = 3
    ) -> list[dict]:

        self._build()

        embedding_service = self._get_embedding_service()

        query_vector = embedding_service.embed(
            query
        )

        return self.vector_store.search(
            query_vector,
            top_k=top_k
        )