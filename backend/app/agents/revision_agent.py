import json

from backend.app.services.llm_service import LLMService


class RevisionAgent:

    def __init__(self):
        self.llm = LLMService()

    def revise(
        self,
        resume_analysis: dict,
        jd_analysis: dict,
        skill_gap_analysis: dict,
        tailored_resume: dict,
        critic_result: dict
    ) -> dict:

        prompt = f"""
You are a Resume Revision Agent.

Your task is to improve a tailored resume based on
the feedback provided by a Resume Critic Agent.

The revised resume must remain completely truthful.

IMPORTANT RULES:

1. Only use information present in the original resume analysis.
2. You may improve wording, structure, relevance, and clarity.
3. Do NOT invent skills, experience, projects, certifications,
   achievements, responsibilities, or metrics.
4. Do NOT add missing skills as if the candidate possesses them.
5. Preserve the factual meaning of the original resume.
6. Address the issues identified by the critic.
7. Follow the critic's recommendations where appropriate.
8. Do not make changes that are unrelated to the critic feedback.
9. Keep relevant job-description keywords when they accurately
   represent the candidate's existing skills.
10. Do not add fake numbers or achievements.
11. Return ONLY valid JSON.
12. Do not use markdown.

Use exactly this structure:

{{
    "tailored_summary": "",
    "tailored_skills": [],
    "rewritten_projects": [],
    "rewritten_experience": [],
    "keywords_emphasized": [],
    "notes": []
}}

ORIGINAL RESUME ANALYSIS:
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

CURRENT TAILORED RESUME:
----------------
{json.dumps(tailored_resume, indent=2)}
----------------

CRITIC FEEDBACK:
----------------
{json.dumps(critic_result, indent=2)}
----------------

Now revise the tailored resume based on the critic feedback.
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
                "Gemini returned invalid JSON for resume revision."
            )