from src.agents.data_agent import DataAgent
import pytest

def test_data_agent_retry_failure():
    agent = DataAgent()
    with pytest.raises(Exception):
        agent.load_data("non_existing.csv", retries=2, delay=0)
