import os

from google import genai
from dotenv import load_dotenv
from pathlib import Path
from backend.app.config import settings


BASE_DIR = Path(__file__).resolve().parents[3]
load_dotenv(BASE_DIR / ".env")


class EmbeddingService:

    def __init__(self):

        api_key = settings.GEMINI_API_KEYS[0] if settings.GEMINI_API_KEYS else None

        if not api_key:
             raise ValueError(
             "No Gemini API keys are configured."
        )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = "gemini-embedding-001"

    def embed(self, text: str) -> list[float]:

        response = self.client.models.embed_content(
            model=self.model,
            contents=text
        )

        return response.embeddings[0].values