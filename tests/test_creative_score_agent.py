from src.agents.creative_score_agent import CreativeScoreAgent

def test_creative_score_ranges():
    agent = CreativeScoreAgent()

    good = agent.score("Amazing winter sale – 40% off! Order now")
    bad = agent.score("hi")

    assert 70 <= good["score"] <= 100
    assert bad["score"] < good["score"]
