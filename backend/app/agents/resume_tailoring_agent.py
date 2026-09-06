import json

from backend.app.services.llm_service import LLMService


class ResumeTailoringAgent:

    def __init__(self):
        self.llm = LLMService()

    def tailor(
        self,
        resume_analysis: dict,
        jd_analysis: dict,
        skill_gap_analysis: dict
    ) -> dict:

        prompt = f"""
You are a Resume Tailoring Agent.

Your task is to tailor an existing resume for a specific job description.

IMPORTANT RULES:
1. Only use information that already exists in the resume.
2. Do NOT invent skills, projects, experience, certifications, or achievements.
3. Do NOT claim the candidate has a missing skill unless it exists in the resume.
4. Improve wording to better match the job description.
5. Prioritize relevant skills and experience.
6. Use strong action verbs.
7. Keep the meaning of the original experience.
8. Do not add fake numbers or metrics.
9. Return ONLY valid JSON.
10. Do not use markdown.

Use exactly this structure:

{{
    "tailored_summary": "",
    "tailored_skills": [],
    "rewritten_projects": [],
    "rewritten_experience": [],
    "keywords_emphasized": [],
    "notes": []
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

Now generate the tailored resume content.
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
                "Gemini returned invalid JSON for resume tailoring."
            )