class SkillGapAgent:

    def analyze(self, matching_result: dict) -> dict:

        missing_skills = matching_result.get(
            "missing_skills", []
        )

        partial_matches = matching_result.get(
            "partial_matches", []
        )

        high_priority_gaps = []
        medium_priority_gaps = []
        low_priority_gaps = []

        # Required skills that are completely missing
        for skill in missing_skills:

            high_priority_gaps.append({
                "skill": skill,
                "reason": "Required skill is missing from the resume.",
                "recommendation": f"Learn and add relevant experience with {skill}."
            })

        # Skills where the resume has a partial match
        for skill in partial_matches:

            medium_priority_gaps.append({
                "skill": skill,
                "reason": "The resume shows a partial match for this skill.",
                "recommendation": f"Strengthen practical experience with {skill}."
            })

        if not high_priority_gaps and not medium_priority_gaps:
            summary = "No major skill gaps were identified."
        else:
            summary = (
                f"Identified {len(high_priority_gaps)} high-priority "
                f"and {len(medium_priority_gaps)} medium-priority skill gaps."
            )

        return {
            "high_priority_gaps": high_priority_gaps,
            "medium_priority_gaps": medium_priority_gaps,
            "low_priority_gaps": low_priority_gaps,
            "learning_recommendations": [],
            "summary": summary
        }