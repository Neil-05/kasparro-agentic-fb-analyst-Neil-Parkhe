import yaml
import json
import argparse
import os
from pathlib import Path
from loguru import logger

from src.agents.planner_agent import PlannerAgent
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.creative_agent import CreativeAgent
from src.agents.memory_agent import MemoryAgent


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
        print("\n--- Running Agentic System ---\n")
        logger.add("logs/system.json", rotation="1 MB", backtrace=True, diagnose=True, serialize=True)
        logger.bind(stage="orchestrator").info("Pipeline started")
        logger.info("Memory: loading existing memory (if any)")
        mem_state = self.memory.load()
        logger.info("Memory loaded: {} past runs", len(mem_state.get("runs", [])))

        try:
            plan = self.planner.plan(query)
            logger.bind(stage="planner", output=plan).info("Planner completed")
            print("Planner Output:", plan)
        except Exception as e:
            logger.error("Planner failed: {}", e)
            self.memory.record_failure(str(e))
            raise

        dataset_path = self.config.get("data", {}).get("dataset_path", "data/sample_small.csv")
        try:
            logger.bind(stage="data_agent", input=dataset_path).info("Data loading started")
            df = self.data_agent.load_data(dataset_path)
            logger.bind(stage="data_agent", output=f"{len(df)} rows").info("Data loading completed")
        except Exception as e:
            logger.error("DataAgent failed: {}", e)
            self.memory.record_failure(str(e))
            raise

        try:
            summary = self.data_agent.summarize(df)
            logger.bind(stage="data_summary", output=summary).info("Summary completed")
            print("Data Summary:", summary)
        except Exception as e:
            logger.error("Summarize failed: {}", e)
            self.memory.record_failure(str(e))
            raise

        try:
            deltas_full = self.data_agent.compute_deltas(df)
            logger.bind(stage="data_deltas", output=deltas_full).info("Deltas computed")
        except Exception as e:
            logger.error("compute_deltas failed: {}", e)
            deltas_full = {"deltas": {}, "segment_ctr": {}, "worst_segment": "unknown"}

        try:
            hypotheses = self.insight_agent.generate_hypotheses(deltas_full)
            logger.bind(stage="insight_agent", output=hypotheses).info("Insight generation completed")
            print("Hypotheses:", hypotheses)
        except Exception as e:
            logger.error("InsightAgent failed: {}", e)
            hypotheses = [{"issue": "Unknown", "reason": "insight failure", "confidence": 0.0}]
            self.memory.record_failure(str(e))

        try:
            validated = self.evaluator.evaluate(df, hypotheses, deltas=deltas_full.get("deltas"))
            logger.bind(stage="evaluator", output=validated).info("Evaluation completed")
            print("Validated Insights:", validated)
        except Exception as e:
            logger.error("Evaluator failed: {}", e)
            validated = []
            self.memory.record_failure(str(e))

        try:
            creatives = self.creative_agent.generate_creatives(df, hypotheses)
            # optional scoring: if creative agent added scores, keep them
            logger.bind(stage="creative_agent", output=f"{len(creatives)} items").info("Creative generation completed")
            print("Creative Suggestions:", creatives)
        except Exception as e:
            logger.error("CreativeAgent failed: {}", e)
            creatives = []
            self.memory.record_failure(str(e))

        # persist reports & memory
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

        try:
            self.memory.update_from_run(summary, validated)
        except Exception as e:
            logger.warning("Memory update failed: {}", e)

        logger.bind(stage="orchestrator").info("Pipeline finished successfully")
        print("\nOutputs saved to reports/ directory\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default=None, help="Path to config YAML")
    args = parser.parse_args()
    config_path = args.config or os.environ.get("DATA_CONFIG") or "config/config.yaml"
    orchestrator = Orchestrator(config_path=config_path)
    orchestrator.run("Analyze ROAS drop")
