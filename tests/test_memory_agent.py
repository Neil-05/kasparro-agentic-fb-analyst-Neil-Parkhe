import json
import tempfile
from pathlib import Path

from src.agents.memory_agent import MemoryAgent

def test_memory_create_tmp_file(tmp_path):
    mem_file = tmp_path / "mem.json"
    agent = MemoryAgent(path=str(mem_file))
    state = agent.load()
    assert isinstance(state, dict)
    assert "runs" in state
    assert state["runs"] == []

def test_memory_update_and_persist(tmp_path):
    mem_file = tmp_path / "mem.json"
    agent = MemoryAgent(path=str(mem_file))
    initial = agent.load()
    summary = {"date_range": ["2025-01-01", "2025-01-02"], "avg_ctr": 0.01}
    insights = [{"issue": "Low CTR", "value": 0.01, "threshold": 0.015, "valid": True}]
    agent.update_from_run(summary, insights)

    agent2 = MemoryAgent(path=str(mem_file))
    state = agent2.load()
    assert state["last_run"]["summary"]["avg_ctr"] == 0.01
    assert len(state["runs"]) == 1
    assert state["campaign_stats"]["low_ctr_count"] >= 1
