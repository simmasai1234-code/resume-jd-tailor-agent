import json

from backend.app.services.llm_service import LLMService


class CoverLetterAgent:

    def __init__(self):
        self.llm = LLMService()

    def generate(
        self,
        resume_analysis: dict,
        jd_analysis: dict,
        skill_gap_analysis: dict
    ) -> dict:

        prompt = f"""
You are a Cover Letter Generation Agent.

Generate a professional, personalized cover letter
based on the candidate's resume and the target job description.

IMPORTANT RULES:

1. Only use information present in the resume analysis.
2. Do NOT invent skills, experience, projects, certifications,
   achievements, or metrics.
3. Do NOT claim missing skills as existing skills.
4. Focus on skills that match the job description.
5. Keep the cover letter professional and concise.
6. Mention relevant candidate strengths.
7. Do not exaggerate the candidate's experience.
8. Missing skills may be acknowledged as areas for development,
   but must not be presented as existing skills.
9. Return ONLY valid JSON.
10. Do not use markdown.

Use exactly this structure:

{{
    "opening": "",
    "body": "",
    "closing": "",
    "full_cover_letter": ""
}}

RESUME ANALYSIS:
----------------
{json.dumps(resume_analysis, indent=2)}
----------------

JOB DESCRIPTION ANALYSIS:
----------------
{json.dumps(jd_analysis, indent=2)}
----------------

SKILL GAP ANALYSIS:
----------------
{json.dumps(skill_gap_analysis, indent=2)}
----------------

Now generate the personalized cover letter.
"""

        response = self.llm.generate(prompt)

        response = response.strip()

        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            raise ValueError(
                "Gemini returned invalid JSON for cover letter generation."
            )