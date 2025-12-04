# src/agents/creative_score_agent.py

class CreativeScoreAgent:
    """
    Deterministic creative scoring engine.
    Produces scores in the 0–100 range, required by tests.
    """

    def score(self, text: str):
        if not text or len(text.strip()) == 0:
            return {"score": 10}  

        length = len(text)


        if length < 10:
            score = 25
        elif length < 20:
            score = 45
        elif length < 40:
            score = 65
        else:
            score = 85 + (length % 5) 

      
        score = max(0, min(score, 100))

        return {"score": score}
