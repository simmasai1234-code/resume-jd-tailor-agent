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

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            if not response.text:
                raise ValueError(
                    "Gemini returned an empty response."
                )

            return response.text

        except Exception as e:

            error_message = str(e)

            if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:

                raise RuntimeError(
                    "Gemini API quota exceeded. "
                    "Please wait for the quota to reset or "
                    "check your Gemini API plan and billing."
                ) from e

            raise RuntimeError(
                f"Gemini API request failed: {error_message}"
            ) from e