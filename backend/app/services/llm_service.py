import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# ============================================================
# Project root
# resume-jd-tailor-agent/
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[3]


# ============================================================
# Load environment variables
# ============================================================

load_dotenv(BASE_DIR / ".env")


class LLMService:

    def __init__(self):

        # ----------------------------------------------------
        # Read Gemini API key
        # ----------------------------------------------------

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        # ----------------------------------------------------
        # Gemini client
        # ----------------------------------------------------

        self.client = genai.Client(
            api_key=api_key
        )

        # ----------------------------------------------------
        # Model
        # ----------------------------------------------------

        self.model = "gemini-3.6-flash"


    # ========================================================
    # Generate response
    # ========================================================

    def generate(
        self,
        prompt: str,
        retries: int = 2
    ) -> str:

        for attempt in range(retries + 1):

            try:

                response = (
                    self.client
                    .models
                    .generate_content(
                        model=self.model,
                        contents=prompt
                    )
                )

                # ------------------------------------------------
                # Validate response
                # ------------------------------------------------

                if not response.text:

                    raise ValueError(
                        "Gemini returned an empty response."
                    )

                return response.text


            except Exception as e:

                error_message = str(e)


                # =================================================
                # Quota / Rate Limit
                # =================================================

                if (
                    "429" in error_message
                    or
                    "RESOURCE_EXHAUSTED" in error_message
                ):

                    raise RuntimeError(
                        "Gemini API quota exceeded. "
                        "Please wait for the quota "
                        "to reset or check your "
                        "Gemini API plan."
                    ) from e


                # =================================================
                # Temporary Gemini server error
                # =================================================

                if (
                    "503" in error_message
                    or
                    "UNAVAILABLE" in error_message
                ):

                    if attempt < retries:

                        # Exponential backoff:
                        # attempt 0 -> 1 second
                        # attempt 1 -> 2 seconds

                        time.sleep(
                            2 ** attempt
                        )

                        continue


                # =================================================
                # Other API errors
                # =================================================

                raise RuntimeError(
                    "Gemini API request failed: "
                    f"{error_message}"
                ) from e


        # ========================================================
        # Fallback
        # ========================================================

        raise RuntimeError(
            "Gemini API request failed after retries."
        )