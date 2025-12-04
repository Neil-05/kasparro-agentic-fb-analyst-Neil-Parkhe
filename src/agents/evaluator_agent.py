from loguru import logger

class EvaluatorAgent:
    def __init__(self, config):
        self.config = config

    def evaluate(self, df, hypotheses, deltas):
        """
        Evaluate hypotheses using:
        - baseline vs current deltas
        - segment-level CTR/ROAS drops
        - severity scoring
        """

        logger.info("Evaluator: running quantitative evaluation")
        results = []

        for h in hypotheses:
            issue = h["issue"]
            evidence = {}
            confidence = 0.0
            impact = "low"

            if issue == "CTR Drop Detected":
                pct = deltas["deltas"]["ctr_delta_pct"]
                seg = list(deltas["segment_ctr"].items())[0]  

                evidence = {
                    "ctr_delta_pct": pct,
                    "worst_segment": seg[0],
                    "segment_ctr": seg[1]
                }

                if pct < -30:
                    impact = "high"
                    confidence = 0.9
                elif pct < -15:
                    impact = "medium"
                    confidence = 0.75
                else:
                    impact = "low"
                    confidence = 0.5

            elif issue == "ROAS Decline":
                pct = deltas["deltas"]["roas_delta_pct"]
                evidence = {"roas_delta_pct": pct}

                if pct < -30:
                    impact = "high"
                    confidence = 0.85
                elif pct < -10:
                    impact = "medium"
                    confidence = 0.65
                else:
                    impact = "low"
                    confidence = 0.4

            result = {
                "hypothesis": issue,
                "evidence": evidence,
                "impact": impact,
                "confidence": round(confidence, 3)
            }

            logger.info(f"Evaluator result: {result}")
            results.append(result)

        return results
