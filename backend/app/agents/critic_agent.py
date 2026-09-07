import json

from backend.app.services.llm_service import LLMService


class CriticAgent:

    def __init__(self):
        self.llm = LLMService()

    def evaluate(
        self,
        resume_analysis: dict,
        jd_analysis: dict,
        skill_gap_analysis: dict,
        tailored_resume: dict
    ) -> dict:

        prompt = f"""
You are a Resume Critic Agent.

Your task is to critically evaluate a tailored resume
against the original resume analysis, job description analysis,
and skill gap analysis.

Evaluate the quality of the tailored resume.

IMPORTANT RULES:

1. Check whether the tailored resume contains only truthful information.
2. Detect invented skills, experience, projects, certifications, achievements,
   or metrics.
3. Check whether the resume is relevant to the job description.
4. Check whether important job-description keywords are covered.
5. Check whether the rewritten content preserves the original meaning.
6. Check whether missing skills were incorrectly presented as existing skills.
7. Identify weak or unclear resume sections.
8. Provide specific improvement suggestions.
9. Do not invent information yourself.
10. Return ONLY valid JSON.
11. Do not use markdown.

Use exactly this structure:

{{
    "overall_score": 0,
    "passed": false,
    "strengths": [],
    "issues": [],
    "hallucination_risks": [],
    "keyword_issues": [],
    "content_issues": [],
    "recommendations": [],
    "summary": ""
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

TAILORED RESUME:
----------------
{json.dumps(tailored_resume, indent=2)}
----------------

Now critically evaluate the tailored resume.
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
                "Gemini returned invalid JSON for critic evaluation."
            )