import os
from pathlib import Path

from dotenv import load_dotenv


# ============================================================
# Project root
# resume-jd-tailor-agent/
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]


# ============================================================
# Load environment variables
# ============================================================

load_dotenv(BASE_DIR / ".env")


class Settings:

    # ========================================================
    # Application
    # ========================================================

    APP_NAME = os.getenv(
        "APP_NAME",
        "Resume JD Tailor Agent"
    )

    ENVIRONMENT = os.getenv(
        "ENVIRONMENT",
        "development"
    ).lower()

    HOST = os.getenv(
        "HOST",
        "127.0.0.1"
    )

    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO"
    ).upper()


    # ========================================================
    # Gemini API Keys
    # ========================================================
    #
    # Add as many keys as you want:
    #
    # GEMINI_API_KEY_1
    # GEMINI_API_KEY_2
    # GEMINI_API_KEY_3
    # GEMINI_API_KEY_4
    #
    # Empty / missing keys are automatically ignored.
    # ========================================================

    GEMINI_API_KEYS = [
        os.getenv("GEMINI_API_KEY_1"),
        os.getenv("GEMINI_API_KEY_2"),
        os.getenv("GEMINI_API_KEY_3"),
        os.getenv("GEMINI_API_KEY_4"),
    ]

    GEMINI_API_KEYS = [
        key.strip()
        for key in GEMINI_API_KEYS
        if key and key.strip()
    ]


    # ========================================================
    # Gemini model
    # ========================================================

    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.6-flash"
    )


    # ========================================================
    # CORS
    # ========================================================

    ALLOWED_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "ALLOWED_ORIGINS",
            "http://127.0.0.1:8000,http://localhost:8000"
        ).split(",")
        if origin.strip()
    ]


    # ========================================================
    # Initialization / Validation
    # ========================================================

    def __init__(self):

        # ----------------------------------------------------
        # Validate environment
        # ----------------------------------------------------

        allowed_environments = {
            "development",
            "testing",
            "production"
        }

        if self.ENVIRONMENT not in allowed_environments:

            raise ValueError(
                f"Invalid ENVIRONMENT: {self.ENVIRONMENT}. "
                f"Allowed values: {allowed_environments}"
            )


        # ----------------------------------------------------
        # Validate port
        # ----------------------------------------------------

        try:

            self.PORT = int(
                os.getenv(
                    "PORT",
                    "8000"
                )
            )

        except ValueError:

            raise ValueError(
                "PORT must be a valid integer."
            )


        if not 1 <= self.PORT <= 65535:

            raise ValueError(
                "PORT must be between 1 and 65535."
            )


        # ----------------------------------------------------
        # Validate Gemini API keys
        # ----------------------------------------------------

        if self.ENVIRONMENT == "production":

            if not self.GEMINI_API_KEYS:

                raise ValueError(
                    "At least one GEMINI_API_KEY_* "
                    "is required in production."
                )


        # ----------------------------------------------------
        # Prevent insecure wildcard CORS
        # ----------------------------------------------------

        if self.ENVIRONMENT == "production":

            if "*" in self.ALLOWED_ORIGINS:

                raise ValueError(
                    "Wildcard CORS (*) is not allowed "
                    "in production."
                )


# ============================================================
# Global settings object
# ============================================================

settings = Settings()