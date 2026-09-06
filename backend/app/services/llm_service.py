import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Project root:
# resume-jd-tailor-agent/
BASE_DIR = Path(__file__).resolve().parents[3]

# Load .env from project root
load_dotenv(BASE_DIR / ".env")


class LLMService:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(api_key=api_key)

        self.model = "gemini-3.6-flash"

    def generate(self, prompt: str) -> str:

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text