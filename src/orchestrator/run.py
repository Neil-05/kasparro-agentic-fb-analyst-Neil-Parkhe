import yaml
import json
import time
from pathlib import Path
import argparse
import os
from src.agents.planner_agent import PlannerAgent
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.creative_agent import CreativeAgent
from loguru import logger


class Orchestrator:
    def __init__(self, config_path="config/config.yaml"):
        self.config = yaml.safe_load(open(config_path, "r"))

        self.planner = PlannerAgent()
        self.data_agent = DataAgent()
        self.insight_agent = InsightAgent()
        self.evaluator = EvaluatorAgent(self.config)
        self.creative_agent = CreativeAgent()

    def run(self, query="Analyze ROAS drop"):
        print("\n--- Running Agentic System ---\n")

        # Structured JSON logging
        logger.add(
            "logs/system.json",
            rotation="1 MB",
            serialize=True,
            backtrace=True,
            diagnose=True,
        )

        try:
            logger.bind(stage="orchestrator").info("Pipeline started")
            logger.bind(stage="planner", input=query).info("Planner started")
            plan = self.planner.plan(query)
            logger.bind(stage="planner", output=plan).info("Planner completed")
            print("Planner Output:", plan)

           
            dataset_path = self.config["data"]["dataset_path"]
            logger.bind(stage="data_agent", input=dataset_path).info("Data loading started")

            df = self.data_agent.load_data(dataset_path)

            logger.bind(stage="data_agent", output=f"{len(df)} rows").info("Data loading completed")

         
            logger.bind(stage="data_summary").info("Summary generation started")

            summary = self.data_agent.summarize(df)

            logger.bind(stage="data_summary", output=summary).info("Summary completed")
            print("Data Summary:", summary)

            
            logger.bind(stage="insight_agent", input=summary).info("Insight generation started")

            hypotheses = self.insight_agent.generate_hypotheses(summary)

            logger.bind(stage="insight_agent", output=hypotheses).info("Insight generation completed")
            print("Hypotheses:", hypotheses)
            logger.bind(stage="evaluator", input=hypotheses).info("Evaluation started")

            validated = self.evaluator.evaluate(df, hypotheses)

            logger.bind(stage="evaluator", output=validated).info("Evaluation completed")
            print("Validated Insights:", validated)
            logger.bind(stage="creative_agent").info("Creative generation started")

            creatives = self.creative_agent.generate_creatives(df)

            logger.bind(stage="creative_agent", output=creatives).info("Creative generation completed")
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

            logger.bind(stage="orchestrator").info("Pipeline finished successfully")
            print("\nOutputs saved to reports/ directory\n")

        except Exception as e:
            logger.bind(stage="error", exception=str(e)).error("Pipeline failed with exception")
            raise e




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to config YAML"
    )
    args = parser.parse_args()

    # Priority: CLI > ENV > Default
    config_path = (
        args.config
        or os.environ.get("DATA_CONFIG")
        or "config/config.yaml"
    )

    orchestrator = Orchestrator(config_path=config_path)
    orchestrator.run("Analyze ROAS drop")

