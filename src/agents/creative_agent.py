from loguru import logger
from src.agents.creative_score_agent import CreativeScoreAgent


class CreativeAgent:
    def __init__(self):
        self.scorer = CreativeScoreAgent()

    def generate_creatives(self, df, hypotheses=None):
        logger.info("Generating creative suggestions tied to insights")

        logger.bind(
            agent="creative",
            low_ctr_count=len(df[df["ctr"] < 0.015]),
            hypotheses_used=len(hypotheses or [])
        ).info("CreativeAgent: Input summary")

        results = []

        # find worst segment if insights provide one
        worst_segment = None
        if hypotheses:
            for h in hypotheses:
                evidence = h.get("evidence", {})
                if "worst_segment" in evidence:
                    worst_segment = evidence["worst_segment"]

        if worst_segment:
            target_df = df[df["country"] == worst_segment]
        else:
            target_df = df[df["ctr"] < 0.015].head(5)

        for _, row in target_df.iterrows():
            campaign_name = row.get("campaign_name", row.get("campaign", "Unknown Campaign"))
            msg = row.get("message", row.get("creative_message", ""))

            logger.bind(
                agent="creative",
                campaign=campaign_name,
                ctr=float(row.get("ctr", 0.0))
            ).debug("Evaluating row for creative generation")

            suggestion = {
                "campaign": campaign_name,
                "old_message": msg,
                "new_creatives": [
                    f"Try highlighting benefits: {msg}",
                    "Add urgency-based CTA: 'Limited Time Offer!'",
                    "Use more emotional storytelling in copy"
                ]
            }

            score = self.scorer.score(msg)
            suggestion["score"] = score["score"]

            logger.bind(agent="creative", suggestion=suggestion).info("Suggestion created")
            results.append(suggestion)

        return results

