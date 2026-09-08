import time

from google import genai

from backend.app.config import settings


class LLMService:

    def __init__(self):

        # ----------------------------------------------------
        # Gemini API keys
        # ----------------------------------------------------

        self.api_keys = settings.GEMINI_API_KEYS

        self.model = settings.GEMINI_MODEL

        self.current_key_index = 0

        self.client = None

        # Do NOT create Gemini client here.
        # This keeps application imports and tests independent
        # from Gemini credentials/quota.

    # ========================================================
    # Create Gemini client
    # ========================================================

    def _create_client(self, api_key: str):

        return genai.Client(
            api_key=api_key
        )

    # ========================================================
    # Ensure client exists
    # ========================================================

    def _ensure_client(self):

        if self.client is not None:
            return

        if not self.api_keys:

            raise RuntimeError(
                "No Gemini API keys are configured. "
                "Add GEMINI_API_KEY_1, GEMINI_API_KEY_2, "
                "etc. to your .env file."
            )

        self.client = self._create_client(
            self.api_keys[self.current_key_index]
        )

    # ========================================================
    # Switch API key
    # ========================================================

    def _switch_to_next_key(self):

        # Make this safe for tests that use __new__()
        if not hasattr(self, "current_key_index"):
            self.current_key_index = 0

        if not hasattr(self, "api_keys"):
            self.api_keys = []

        if (
            self.current_key_index
            >= len(self.api_keys) - 1
        ):

            return False

        self.current_key_index += 1

        self.client = self._create_client(
            self.api_keys[self.current_key_index]
        )

        return True

    # ========================================================
    # Generate response
    # ========================================================

    def generate(
        self,
        prompt: str,
        retries: int = 2
    ) -> str:

        # ----------------------------------------------------
        # Make test-created instances safe
        # ----------------------------------------------------

        if not hasattr(self, "current_key_index"):
            self.current_key_index = 0

        if not hasattr(self, "api_keys"):
            self.api_keys = []

        if not hasattr(self, "model"):
            self.model = settings.GEMINI_MODEL

        if not hasattr(self, "client"):
            self.client = None

        # ----------------------------------------------------
        # If tests manually provide a mocked client,
        # don't require API keys.
        # ----------------------------------------------------

        if self.client is None:
            self._ensure_client()

        # ----------------------------------------------------
        # Try current key, then rotate on 429
        # ----------------------------------------------------

        while True:

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

                    # ================================================
                    # Gemini quota / rate limit
                    # ================================================

                    if (
                        "429" in error_message
                        or
                        "RESOURCE_EXHAUSTED" in error_message
                    ):

                        switched = (
                            self._switch_to_next_key()
                        )

                        if switched:

                            # Try next API key
                            break

                        raise RuntimeError(
                            "Gemini API quota exceeded. "
                            "All configured Gemini API keys "
                            "have exceeded their quota or rate limit."
                        ) from e

                    # ================================================
                    # Temporary server error
                    # ================================================

                    if (
                        "503" in error_message
                        or
                        "UNAVAILABLE" in error_message
                    ):

                        if attempt < retries:

                            time.sleep(
                                2 ** attempt
                            )

                            continue

                    # ================================================
                    # Other errors
                    # ================================================

                    raise RuntimeError(
                        "Gemini API request failed: "
                        f"{error_message}"
                    ) from e

            else:

                raise RuntimeError(
                    "Gemini API request failed after retries."
                )