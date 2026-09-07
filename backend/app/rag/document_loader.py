from pathlib import Path


class DocumentLoader:

    def __init__(self, knowledge_base_path: str):
        self.knowledge_base_path = Path(knowledge_base_path)

    def load_documents(self) -> list[dict]:
        documents = []

        for file_path in self.knowledge_base_path.glob("*.txt"):

            content = file_path.read_text(
                encoding="utf-8"
            )

            documents.append({
                "source": file_path.name,
                "content": content
            })

        return documents

    def chunk_document(
        self,
        content: str,
        chunk_size: int = 500
    ) -> list[str]:

        words = content.split()
        chunks = []

        current_chunk = []
        current_length = 0

        for word in words:

            word_length = len(word) + 1

            if current_length + word_length > chunk_size:

                chunks.append(
                    " ".join(current_chunk)
                )

                current_chunk = []
                current_length = 0

            current_chunk.append(word)
            current_length += word_length

        if current_chunk:
            chunks.append(
                " ".join(current_chunk)
            )

        return chunks