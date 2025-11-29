# src/agents/creative_score_agent.py
from loguru import logger

class CreativeScoreAgent:

    EMOTION_WORDS = {"amazing", "premium", "exciting", "new", "exclusive", "limited"}
    CTA_WORDS = {"buy", "shop", "save", "discover", "order", "get", "try"}

    def score(self, message: str) -> dict:
        logger.bind(agent="creative_score").info("Scoring creative")

        score = 50  
        if 20 <= len(message) <= 80:
            score += 10
        if "%" in message or any(char.isdigit() for char in message):
            score += 10
        if any(word in message.lower() for word in self.EMOTION_WORDS):
            score += 10
        if any(word in message.lower() for word in self.CTA_WORDS):
            score += 10

        return {
            "message": message,
            "score": min(score, 100)
        }
