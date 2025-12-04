import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict
from loguru import logger

DEFAULT_PATH = "memory/short_term_memory.json"


class MemoryAgent:
    def __init__(self, path: str = DEFAULT_PATH):
        self.path = Path(path)
        self.state: Dict[str, Any] = {"runs": [], "campaign_stats": {}, "last_run": None}
        self._ensure_file()

    def _ensure_file(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            logger.info("MemoryAgent: creating memory file at {}", self.path)
            self.save()

    def load(self) -> Dict[str, Any]:
        try:
            with open(self.path, "r") as f:
                self.state = json.load(f)
            logger.info("MemoryAgent: loaded memory from {}", self.path)
        except Exception as e:
            logger.warning("MemoryAgent: failed to load memory (will use empty). Error: {}", e)
            self.state = {"runs": [], "campaign_stats": {}, "last_run": None}
        return self.state

    def save(self) -> None:
        try:
            with open(self.path, "w") as f:
                json.dump(self.state, f, indent=2, default=str)
            logger.info("MemoryAgent: saved memory to {}", self.path)
        except Exception as e:
            logger.error("MemoryAgent: failed to save memory: {}", e)

    def update_from_run(self, summary: Dict[str, Any], validated_insights: list) -> None:
        run_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "summary": summary,
            "insights": validated_insights,
        }
        self.state.setdefault("runs", []).append(run_entry)
        self.state["last_run"] = run_entry

       
        for insight in validated_insights:
            if insight.get("issue") == "Low CTR" and insight.get("valid"):
               
                self.state.setdefault("campaign_stats", {}).setdefault("low_ctr_count", 0)
                self.state["campaign_stats"]["low_ctr_count"] += 1

     
        max_runs = 20
        if len(self.state["runs"]) > max_runs:
            self.state["runs"] = self.state["runs"][-max_runs:]

        logger.info("MemoryAgent: updated memory (runs: {})", len(self.state["runs"]))
        self.save()
