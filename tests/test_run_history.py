from src.agents.memory_agent import MemoryAgent
import os
import json
from pathlib import Path

def test_append_run_and_prune(tmp_path):
    memfile = tmp_path / "runs_history.json"
    from src.agents import memory_agent as ma
    orig_runs_file = ma.RUNS_FILE
    ma.RUNS_FILE = tmp_path / "runs_history.json"

    mem = MemoryAgent()
    mem.append_run({"time":"t1"})
    mem.append_run({"time":"t2"})
    runs = mem.load_runs()
    assert len(runs) == 2

    mem.prune_runs(max_runs=1)
    runs2 = mem.load_runs()
    assert len(runs2) == 1

 
    ma.RUNS_FILE = orig_runs_file
