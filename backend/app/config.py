import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")


class Settings:
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

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY"
    )

    ALLOWED_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "ALLOWED_ORIGINS",
            "http://127.0.0.1:8000,http://localhost:8000"
        ).split(",")
        if origin.strip()
    ]

    def __init__(self):
        # Validate environment
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

        # Validate port
        try:
            self.PORT = int(os.getenv("PORT", "8000"))
        except ValueError:
            raise ValueError(
                "PORT must be a valid integer."
            )

        if not 1 <= self.PORT <= 65535:
            raise ValueError(
                "PORT must be between 1 and 65535."
            )

        # Production requires API key
        if self.ENVIRONMENT == "production":
            if not self.GEMINI_API_KEY:
                raise ValueError(
                    "GEMINI_API_KEY is required in production."
                )

            # Prevent accidental insecure wildcard CORS
            if "*" in self.ALLOWED_ORIGINS:
                raise ValueError(
                    "Wildcard CORS (*) is not allowed in production."
                )


settings = Settings()