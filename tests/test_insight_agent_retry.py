from src.agents.insight_agent import InsightAgent

def test_insight_agent_retry_non_empty():
    agent = InsightAgent()

    summary = {"avg_ctr": 0.01}
    output = agent.generate_hypotheses(summary, retries=2)

    assert len(output) > 0
