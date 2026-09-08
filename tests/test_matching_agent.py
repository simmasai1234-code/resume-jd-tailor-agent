from backend.app.agents.matching_agent import (
    MatchingAgent
)


def test_matching_agent():

    agent = MatchingAgent()


    resume = {

        "skills": [
            "Java",
            "Python",
            "SQL"
        ]

    }


    jd = {

        "required_skills": [
            "Java",
            "Python",
            "Docker"
        ]

    }


    result = agent.analyze(
        resume,
        jd
    )


    assert result is not None