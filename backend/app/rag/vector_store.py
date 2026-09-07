import numpy as np


class VectorStore:

    def __init__(self):
        self.documents = []
        self.vectors = []

    def add(
        self,
        document: dict,
        vector: list[float]
    ):

        self.documents.append(document)

        self.vectors.append(
            np.array(vector, dtype=np.float32)
        )

    def search(
        self,
        query_vector: list[float],
        top_k: int = 3
    ) -> list[dict]:

        if not self.vectors:
            return []

        query = np.array(
            query_vector,
            dtype=np.float32
        )

        scores = []

        for index, vector in enumerate(self.vectors):

            similarity = np.dot(query, vector) / (
                np.linalg.norm(query)
                * np.linalg.norm(vector)
            )

            scores.append(
                (similarity, index)
            )

        scores.sort(
            reverse=True
        )

        results = []

        for score, index in scores[:top_k]:

            results.append({
                "score": float(score),
                "source": self.documents[index]["source"],
                "content": self.documents[index]["content"]
            })

        return results