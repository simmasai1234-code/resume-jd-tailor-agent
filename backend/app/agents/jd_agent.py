import json

from backend.app.services.llm_service import LLMService


class JDAgent:

    def __init__(self):
        self.llm = LLMService()

    def analyze(self, jd_text: str) -> dict:

        prompt = f"""
You are a Job Description Analysis Agent.

Analyze the following job description.

Return ONLY valid JSON.
Do not use markdown.
Do not add explanations before or after the JSON.

Use exactly this structure:

{{
    "title": "",
    "required_skills": [],
    "preferred_skills": [],
    "programming_languages": [],
    "frameworks_and_technologies": [],
    "databases": [],
    "experience": "",
    "education": "",
    "responsibilities": [],
    "keywords": []
}}

JOB DESCRIPTION:
----------------
{jd_text}
----------------
"""

        response = self.llm.generate(prompt)

        # Remove possible markdown code fences
        response = response.strip()

        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            raise ValueError(
                "Gemini returned invalid JSON for JD analysis."
            )