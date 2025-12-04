import yaml
import json
import argparse
import os
from datetime import datetime
from pathlib import Path
from loguru import logger

from src.agents.planner_agent import PlannerAgent
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.creative_agent import CreativeAgent
from src.agents.memory_agent import MemoryAgent

from src.agents.schema_drift import detect_schema_drift
from src.agents.adaptive_thresholds import compute_percentile_thresholds
from src.agents.experiment_agent import summarize_run


run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
log_dir = Path(f"logs/run_{run_id}")
log_dir.mkdir(parents=True, exist_ok=True)

logger.add(log_dir / "system.json", serialize=True, rotation="1 MB")
logger.add(log_dir / "system.log", rotation="1 MB")


class Orchestrator:
    def __init__(self, config_path="config/config.yaml"):
        self.config = yaml.safe_load(open(config_path, "r"))

        self.planner = PlannerAgent()
        self.data_agent = DataAgent()
        self.insight_agent = InsightAgent()
        self.evaluator = EvaluatorAgent(self.config)
        self.creative_agent = CreativeAgent()
        self.memory = MemoryAgent()

    def run(self, query="Analyze ROAS drop"):

        logger.bind(stage="orchestrator").info("Pipeline started")
        mem_state = self.memory.load()

        plan = self.planner.plan(query)
        logger.bind(stage="planner", output=plan).info("Planner completed")

        dataset_path = self.config.get("data", {}).get("dataset_path", "data/sample_small.csv")
        df = self.data_agent.load_data(dataset_path)
        logger.bind(stage="data_agent", output=f"{len(df)} rows").info("Data loading completed")

        summary = self.data_agent.summarize(df)
        deltas_full = self.data_agent.compute_deltas(df)

        summary_with_deltas = {**summary, **deltas_full}

        print("Data Summary:", summary)

    
        prev_runs = self.memory.load_runs()
        prev_columns = prev_runs[-1].get("schema_columns") if prev_runs else None

        drift = detect_schema_drift(prev_columns or [], list(df.columns))
        if drift.get("drifted"):
            logger.bind(stage="schema_drift", drift=drift).warning("Schema drift detected")

   
        hypotheses = self.insight_agent.generate_hypotheses(summary_with_deltas)
        logger.bind(stage="insight_agent", output=hypotheses).info("Insight generation completed")
        print("Hypotheses:", hypotheses)

 
        if self.config.get("system", {}).get("adaptive_thresholds", False):
            adaptive = compute_percentile_thresholds(
                df, q=self.config.get("system", {}).get("adaptive_quantile", 0.2)
            )
            temp_config = dict(self.config)
            temp_config.setdefault("thresholds", {}).update(adaptive)
            evaluator = EvaluatorAgent(temp_config)
        else:
            evaluator = self.evaluator

    
        validated = evaluator.evaluate(df, hypotheses, deltas=deltas_full.get("deltas"))
        logger.bind(stage="evaluator", output=validated).info("Evaluation completed")
        print("Validated Insights:", validated)

        creatives = self.creative_agent.generate_creatives(df, validated)
        logger.bind(stage="creative_agent", output=f"{len(creatives)}").info("Creative generation completed")
        print("Creative Suggestions:", creatives)

        Path("reports").mkdir(exist_ok=True)
        with open("reports/insights.json", "w") as f:
            json.dump(validated, f, indent=2)
        with open("reports/creatives.json", "w") as f:
            json.dump(creatives, f, indent=2)
        with open("reports/report.md", "w") as f:
            f.write("# Final Marketing Report\n\n")
            f.write("## Validated Insights\n")
            f.write(json.dumps(validated, indent=2))
            f.write("\n\n## Creative Suggestions\n")
            f.write(json.dumps(creatives, indent=2))
        run_summary = summarize_run(
            deltas_full.get("baseline"),
            deltas_full.get("current"),
            deltas_full.get("deltas")
        )
        run_summary["schema_columns"] = list(df.columns)
        run_summary["validated_insights"] = validated

        self.memory.append_run(run_summary)
        self.memory.prune_runs(max_runs=self.config.get("system", {}).get("max_saved_runs", 500))

        logger.bind(
            stage="pipeline_summary",
            hypotheses_count=len(hypotheses),
            validated_count=len(validated),
            creatives_count=len(creatives),
            run_id=run_id
        ).info("Pipeline summary saved")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default=None)
    args = parser.parse_args()

    config_path = args.config or os.environ.get("DATA_CONFIG") or "config/config.yaml"

    orchestrator = Orchestrator(config_path=config_path)
    orchestrator.run("Analyze ROAS drop")
