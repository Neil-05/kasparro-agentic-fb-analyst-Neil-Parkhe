class EvaluatorAgent:
   

    def __init__(self, config):
        self.config = config

    def evaluate(self, df, hypotheses):
        validated = []

        for h in hypotheses:
            if h["issue"] == "Low CTR":
                avg_ctr = df["ctr"].mean()
                threshold = self.config["thresholds"]["low_ctr"]

                validated.append({
                    "issue": "Low CTR",
                    "value": float(avg_ctr),
                    "threshold": float(threshold),
                    "valid": bool(avg_ctr < threshold)   
                })

            if h["issue"] == "Low ROAS":
                avg_roas = df["roas"].mean()
                threshold = self.config["thresholds"]["low_roas"]

                validated.append({
                    "issue": "Low ROAS",
                    "value": float(avg_roas),
                    "threshold": float(threshold),
                    "valid": bool(avg_roas < threshold)   
                })

        return validated
