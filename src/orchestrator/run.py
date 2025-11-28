import yaml
import json
from pathlib import Path

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

        logger.add("logs/system.json", rotation="1 MB", backtrace=True, diagnose=True, serialize=True)
        logger.info(f"Starting Agentic Pipeline Run for query: {query}")

        plan = self.planner.plan(query)
        print("Planner Output:", plan)

        logger.info("Loading dataset with retry logic enabled")
        dataset_path = self.config["data"]["dataset_path"]
        df = self.data_agent.load_data(dataset_path)
        summary = self.data_agent.summarize(df)
        print("Data Summary:", summary)

        logger.info("Generating hypotheses with retry logic")
        hypotheses = self.insight_agent.generate_hypotheses(summary)
        print("Hypotheses:", hypotheses)

        validated = self.evaluator.evaluate(df, hypotheses)
        print("Validated Insights:", validated)

        creatives = self.creative_agent.generate_creatives(df)
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

        print("\nOutputs saved to reports/ directory\n")


if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.run("Analyze ROAS drop")
