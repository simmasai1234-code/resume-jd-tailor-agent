from backend.app.agents.jd_agent import JDAgent
from backend.app.agents.resume_agent import ResumeAgent
from backend.app.agents.matching_agent import MatchingAgent
from backend.app.agents.skill_gap_agent import SkillGapAgent
from backend.app.agents.resume_tailoring_agent import ResumeTailoringAgent
from backend.app.agents.critic_agent import CriticAgent
from backend.app.agents.revision_agent import RevisionAgent
from backend.app.agents.interview_agent import InterviewAgent
from backend.app.agents.cover_letter_agent import CoverLetterAgent


class AgentOrchestrator:

    def __init__(self):

        self.jd_agent = JDAgent()
        self.resume_agent = ResumeAgent()
        self.matching_agent = MatchingAgent()
        self.skill_gap_agent = SkillGapAgent()
        self.tailoring_agent = ResumeTailoringAgent()
        self.critic_agent = CriticAgent()
        self.revision_agent = RevisionAgent()
        self.interview_agent = InterviewAgent()
        self.cover_letter_agent = CoverLetterAgent()

    def run(
        self,
        resume_text: str,
        jd_text: str,
        max_revisions: int = 2
    ) -> dict:

        # --------------------------------
        # Step 1: Analyze Resume
        # --------------------------------

        resume_analysis = self.resume_agent.analyze(
            resume_text
        )

        # --------------------------------
        # Step 2: Analyze Job Description
        # --------------------------------

        jd_analysis = self.jd_agent.analyze(
            jd_text
        )

        # --------------------------------
        # Step 3: Match Resume with JD
        # --------------------------------

        matching_result = self.matching_agent.analyze(
            resume_analysis,
            jd_analysis
        )

        # --------------------------------
        # Step 4: Analyze Skill Gaps
        # --------------------------------

        skill_gap_analysis = self.skill_gap_agent.analyze(
            matching_result
        )

        # --------------------------------
        # Step 5: Tailor Resume
        # --------------------------------

        tailored_resume = self.tailoring_agent.tailor(
            resume_analysis,
            jd_analysis,
            skill_gap_analysis
        )

        # --------------------------------
        # Step 6: Critic + Revision Loop
        # --------------------------------

        critic_result = self.critic_agent.evaluate(
            resume_analysis,
            jd_analysis,
            skill_gap_analysis,
            tailored_resume
        )

        revision_count = 0

        while (
            not critic_result.get("passed", False)
            and revision_count < max_revisions
        ):

            tailored_resume = self.revision_agent.revise(
                resume_analysis,
                jd_analysis,
                skill_gap_analysis,
                tailored_resume,
                critic_result
            )

            revision_count += 1

            critic_result = self.critic_agent.evaluate(
                resume_analysis,
                jd_analysis,
                skill_gap_analysis,
                tailored_resume
            )

        # --------------------------------
        # Step 7: Generate Interview Prep
        # --------------------------------

        interview_preparation = self.interview_agent.generate(
            resume_analysis,
            jd_analysis,
            skill_gap_analysis,
            tailored_resume
        )

        # --------------------------------
        # Step 8: Generate Cover Letter
        # --------------------------------

        cover_letter = self.cover_letter_agent.generate(
            resume_analysis,
            jd_analysis,
            skill_gap_analysis
        )

        # --------------------------------
        # Final Result
        # --------------------------------

        return {
            "resume_analysis": resume_analysis,
            "jd_analysis": jd_analysis,
            "matching_result": matching_result,
            "skill_gap_analysis": skill_gap_analysis,
            "tailored_resume": tailored_resume,
            "critic_result": critic_result,
            "revision_count": revision_count,
            "interview_preparation": interview_preparation,
            "cover_letter": cover_letter
        }