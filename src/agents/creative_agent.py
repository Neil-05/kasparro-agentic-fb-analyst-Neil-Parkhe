from loguru import logger
from src.agents.creative_score_agent import CreativeScoreAgent


class CreativeAgent:
    def __init__(self):
        self.scorer = CreativeScoreAgent()   # scoring engine added

    def generate_creatives(self, df):
        logger.bind(agent="creative", step="start").info("Generating creative suggestions")

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

            # FIX: score correct variable
            scored = self.scorer.score(msg)
            suggestion["score"] = scored["score"]

            logger.bind(agent="creative", suggestion=suggestion).info("Suggestion created")
            results.append(suggestion)

        logger.bind(agent="creative", step="end", total=len(results)).info("Creative generation completed")
        return results
