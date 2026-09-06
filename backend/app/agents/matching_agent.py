class MatchingAgent:

    def analyze(self, resume_analysis: dict, jd_analysis: dict) -> dict:

        resume_skills = set(
            skill.lower()
            for skill in resume_analysis.get("skills", [])
        )

        jd_required_skills = set(
            skill.lower()
            for skill in jd_analysis.get("required_skills", [])
        )

        matched_skills = resume_skills.intersection(jd_required_skills)

        missing_skills = jd_required_skills - resume_skills

        total_required = len(jd_required_skills)

        if total_required > 0:
            match_score = round(
                (len(matched_skills) / total_required) * 100,
                2
            )
        else:
            match_score = 0

        return {
            "match_score": match_score,
            "matched_skills": sorted(matched_skills),
            "missing_skills": sorted(missing_skills),
            "partial_matches": [],
            "keyword_gaps": [],
            "strengths": [],
            "recommendations": []
        }