import json

from backend.app.rag.knowledge_base import KnowledgeBase
from backend.app.services.llm_service import LLMService


class SkillGapAgent:

    def __init__(self):

        self.llm = LLMService()

        self.knowledge_base = KnowledgeBase(
            "backend/app/data/knowledge_base"
        )

    def analyze(self, matching_result: dict) -> dict:

        missing_skills = matching_result.get(
            "missing_skills",
            []
        )

        partial_matches = matching_result.get(
            "partial_matches",
            []
        )

        # Retrieve relevant resume guidelines
        query = (
            "How should missing and partially matched "
            "skills be handled when tailoring a resume?"
        )

        retrieved_knowledge = self.knowledge_base.retrieve(
            query,
            top_k=2
        )

        knowledge_text = "\n\n".join(
            result["content"]
            for result in retrieved_knowledge
        )

        prompt = f"""
You are a Skill Gap Analysis Agent.

Analyze the skill gaps between a candidate's resume
and a job description.

IMPORTANT RULES:

1. Do not invent candidate skills.
2. Missing skills must remain missing.
3. Clearly distinguish missing skills from partial matches.
4. Give practical learning recommendations.
5. Follow the retrieved resume-writing guidelines.
6. Return ONLY valid JSON.
7. Do not use markdown.

Use exactly this structure:

{{
    "high_priority_gaps": [],
    "medium_priority_gaps": [],
    "low_priority_gaps": [],
    "learning_recommendations": [],
    "summary": ""
}}

MATCHING RESULT:
----------------
{json.dumps(matching_result, indent=2)}
----------------

RETRIEVED RESUME GUIDELINES:
----------------
{knowledge_text}
----------------

Now perform the skill gap analysis.
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
                "Gemini returned invalid JSON for skill gap analysis."
            )