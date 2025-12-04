# src/agents/creative_agent.py

from loguru import logger
from src.agents.creative_score_agent import CreativeScoreAgent


class CreativeAgent:
    def __init__(self):
        self.scorer = CreativeScoreAgent()  # FIXED — ensure not None

    def generate_creatives(self, df, hypotheses=None):
        logger.info("Generating creative suggestions tied to insights")

        low_ctr_ads = df[df["ctr"] < 0.015].head(5)
        results = []

        for _, row in low_ctr_ads.iterrows():
            campaign_name = row.get("campaign_name", row.get("campaign", "Unknown Campaign"))
            msg = row.get("message", row.get("creative_message", ""))

            suggestion = {
                "campaign": campaign_name,
                "old_message": msg,
                "new_creatives": [
                    f"Try highlighting benefits: {msg}",
                    "Add urgency-based CTA: 'Limited Time Offer!'",
                    "Use more emotional storytelling in copy"
                ]
            }

            # Apply scoring
            scored = self.scorer.score(msg)
            suggestion["score"] = scored["score"]

            logger.bind(agent="creative", suggestion=suggestion).info("Suggestion created")
            results.append(suggestion)

        return results
