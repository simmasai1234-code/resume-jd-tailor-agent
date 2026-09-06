import json

from backend.app.services.llm_service import LLMService


class ResumeAgent:

    def __init__(self):
        self.llm = LLMService()

    def analyze(self, resume_text: str) -> dict:

        prompt = f"""
You are a Resume Analysis Agent.

Analyze the following resume.

Return ONLY valid JSON.
Do not use markdown.
Do not add explanations before or after the JSON.

Use exactly this structure:

{{
    "name": "",
    "email": "",
    "phone": "",
    "summary": "",
    "education": [],
    "skills": [],
    "programming_languages": [],
    "frameworks_and_technologies": [],
    "databases": [],
    "projects": [],
    "experience": [],
    "certifications": [],
    "keywords": []
}}

RESUME:
----------------
{resume_text}
----------------
"""

        response = self.llm.generate(prompt)

        response = response.strip()

        # Remove possible markdown code fences
        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            raise ValueError(
                "Gemini returned invalid JSON for resume analysis."
            )