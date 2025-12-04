import yaml
import json
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

     
        logger.add(
            "logs/system.json",
            rotation="1 MB",
            serialize=True,
            backtrace=True,
            diagnose=True,
        )

        logger.bind(stage="orchestrator").info("Pipeline started")
        logger.info(f"Starting Agentic Pipeline Run for query: {query}")

     
        logger.info("Memory: loading existing memory (if any)")
        mem_state = self.memory.load()
        logger.info("Memory loaded: {} past runs", len(mem_state.get("runs", [])))

      
        plan = self.planner.plan(query)
        print("Planner Output:", plan)

        dataset_path = self.config["data"]["dataset_path"]
        df = self.data_agent.load_data(dataset_path)

        summary = self.data_agent.summarize(df)
        print("Data Summary:", summary)

        hypotheses = self.insight_agent.generate_hypotheses(summary)
        print("Hypotheses:", hypotheses)
       
        deltas = self.data_agent.compute_deltas(df)
        validated = self.evaluator.evaluate(df, hypotheses, deltas)

        print("Validated Insights:", validated)

        creatives = self.creative_agent.generate_creatives(df)
        print("Creative Suggestions:", creatives)

        scored_output = [
            {
                **c,
                "score": self.creative_agent.scorer.score(c["old_message"])["score"],
            }
            for c in creatives
        ]

        creatives = scored_output  

        logger.info("Memory: updating memory with this run's insights")
        try:
            self.memory.update_from_run(summary, validated)
        except Exception as e:
            logger.error("Memory update failed: {}", e)

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

        print("\nOutputs saved to reports/ directory\n")


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default=None)
    args = parser.parse_args()

    config_path = (
        args.config
        or os.environ.get("DATA_CONFIG")
        or "config/config.yaml"
    )

    orchestrator = Orchestrator(config_path=config_path)
    orchestrator.run("Analyze ROAS drop")
