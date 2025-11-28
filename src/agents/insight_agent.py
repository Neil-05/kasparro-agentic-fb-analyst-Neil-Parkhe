class InsightAgent:
    def generate_hypotheses(self, summary, retries=3):
        for _ in range(retries):
            hypotheses = []

            if summary.get("avg_ctr", None) is not None and summary["avg_ctr"] < 0.015:
                hypotheses.append({
                    "issue": "Low CTR",
                    "reason": "Users are less engaged with creatives.",
                    "confidence": 0.78,
                })

            if hypotheses:
                return hypotheses

        return [{"issue": "Unknown", "reason": "Insufficient data", "confidence": 0.0}]
