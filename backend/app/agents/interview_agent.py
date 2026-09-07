import json

from backend.app.services.llm_service import LLMService


class InterviewAgent:

    def __init__(self):
        self.llm = LLMService()

    def generate(
        self,
        resume_analysis: dict,
        jd_analysis: dict,
        skill_gap_analysis: dict,
        tailored_resume: dict
    ) -> dict:

        prompt = f"""
You are an Interview Preparation Agent.

Your task is to generate personalized interview questions
based on the candidate's resume and the target job description.

The questions must help the candidate prepare for the actual role.

IMPORTANT RULES:

1. Only use information present in the resume analysis,
   tailored resume, job description analysis, and skill gap analysis.
2. Do NOT invent candidate experience, projects, skills,
   certifications, achievements, or technologies.
3. Do NOT assume the candidate knows a missing skill.
4. Questions about missing skills may be included as
   learning or conceptual questions, but clearly identify them
   as skill-gap topics.
5. Generate technical questions based on the candidate's
   actual skills and the job requirements.
6. Generate questions about the candidate's projects.
7. Generate behavioral questions relevant to the role.
8. Include questions related to identified skill gaps.
9. Provide a concise expected answer or preparation guidance
   for every question.
10. Questions should be realistic interview questions.
11. Do not provide answers that claim the candidate has
    experience they do not have.
12. Return ONLY valid JSON.
13. Do not use markdown.

Use exactly this structure:

{{
    "technical_questions": [
        {{
            "question": "",
            "expected_answer": "",
            "topic": ""
        }}
    ],
    "project_questions": [
        {{
            "question": "",
            "expected_answer": "",
            "topic": ""
        }}
    ],
    "behavioral_questions": [
        {{
            "question": "",
            "expected_answer": "",
            "topic": ""
        }}
    ],
    "skill_gap_questions": [
        {{
            "question": "",
            "expected_answer": "",
            "topic": ""
        }}
    ],
    "preparation_tips": [],
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

Now generate a personalized interview preparation plan.
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
                "Gemini returned invalid JSON for interview preparation."
            )