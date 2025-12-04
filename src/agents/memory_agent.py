from pathlib import Path
import json
from datetime import datetime
from typing import Any, Dict, List
from loguru import logger

MEMORY_DIR = Path("memory")
MEMORY_FILE = MEMORY_DIR / "short_term_memory.json"
RUNS_FILE = MEMORY_DIR / "runs_history.json"


class MemoryAgent:
    def __init__(self, path: str = None):
        MEMORY_DIR.mkdir(exist_ok=True)

        self.path = Path(path) if path else MEMORY_FILE

        if not self.path.exists():
            self.path.write_text(json.dumps({
                "runs": [],
                "failures": [],
                "campaign_stats": {},
                "last_run": None
            }, indent=2))

        if not RUNS_FILE.exists():
            RUNS_FILE.write_text(json.dumps({"runs": []}, indent=2))


    def load(self) -> Dict[str, Any]:
        try:
            return json.loads(self.path.read_text())
        except Exception as e:
            logger.error("MemoryAgent.load failed: {}", e)
            return {"runs": [], "failures": [], "campaign_stats": {}, "last_run": None}

    def save(self, state: Dict[str, Any]):
        self.path.write_text(json.dumps(state, indent=2))

    def record_failure(self, message: str):
        state = self.load()
        state.setdefault("failures", []).append({
            "time": datetime.utcnow().isoformat(),
            "message": message
        })
        self.save(state)

    def update_from_run(self, summary: Dict[str, Any], insights: List[Dict[str, Any]]):
        state = self.load()

        run_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "summary": summary,
            "insights": insights
        }

        state.setdefault("runs", []).append(run_entry)
        state["last_run"] = run_entry

        for x in insights:
            if x.get("issue") == "Low CTR" and x.get("valid", False):
                stats = state.setdefault("campaign_stats", {})
                stats["low_ctr_count"] = stats.get("low_ctr_count", 0) + 1

        if len(state["runs"]) > 20:
            state["runs"] = state["runs"][-20:]

        self.save(state)

        self.append_run(run_entry)

    def load_runs(self):
        try:
            return json.loads(RUNS_FILE.read_text()).get("runs", [])
        except Exception as e:
            logger.error("MemoryAgent.load_runs failed: {}", e)
            return []

    def append_run(self, run_summary: dict):
        runs = self.load_runs()
        runs.append(run_summary)
        RUNS_FILE.write_text(json.dumps({"runs": runs}, indent=2))

    def prune_runs(self, max_runs=100):
        runs = self.load_runs()
        if len(runs) > max_runs:
            runs = runs[-max_runs:]
            RUNS_FILE.write_text(json.dumps({"runs": runs}, indent=2))
