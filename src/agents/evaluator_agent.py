# src/agents/evaluator_agent.py
from loguru import logger


class EvaluatorAgent:
    def __init__(self, config):
        self.config = config

    def evaluate(self, df, hypotheses, deltas=None):
        """
        Backwards-compatible evaluator.

        - If `deltas` is None -> legacy threshold validation used by older tests:
          returns list of {"issue","value","threshold","valid"} items.

        - If `deltas` is provided -> advanced evaluation returns list of:
          {"hypothesis","evidence","impact","confidence"} items.
        """
        # If no deltas provided, run legacy simple threshold checks
        if deltas is None:
            logger.info("Evaluator (legacy): running threshold-based validation")
            validated = []

            for h in hypotheses:
                if h.get("issue") == "Low CTR":
                    avg_ctr = float(df["ctr"].mean())
                    threshold = float(self.config["thresholds"]["low_ctr"])
                    validated.append({
                        "issue": "Low CTR",
                        "value": avg_ctr,
                        "threshold": threshold,
                        "valid": bool(avg_ctr < threshold)
                    })

                if h.get("issue") == "Low ROAS":
                    avg_roas = float(df["roas"].mean())
                    threshold = float(self.config["thresholds"]["low_roas"])
                    validated.append({
                        "issue": "Low ROAS",
                        "value": avg_roas,
                        "threshold": threshold,
                        "valid": bool(avg_roas < threshold)
                    })

            return validated

        # Advanced evaluator (deltas provided)
        logger.info("Evaluator (advanced): running quantitative evaluation with deltas")
        results = []
        # defensive guards
        d = deltas.get("deltas", {}) if isinstance(deltas, dict) else {}

        for h in hypotheses:
            issue = h.get("issue", "Unknown")
            evidence = {}
            confidence = 0.0
            impact = "low"

            if issue in ("CTR Drop Detected", "Low CTR"):
                pct = d.get("ctr_delta_pct", 0.0)
                seg_ctr = deltas.get("segment_ctr", {}) if isinstance(deltas, dict) else {}
                worst_segment = None
                worst_val = None
                if seg_ctr:
                    # seg_ctr is dict sorted ascending (worst first) in DataAgent
                    try:
                        worst_segment, worst_val = next(iter(seg_ctr.items()))
                    except Exception:
                        worst_segment = None
                        worst_val = None

                evidence = {
                    "ctr_delta_pct": float(pct),
                    "worst_segment": worst_segment,
                    "segment_ctr": float(worst_val) if worst_val is not None else None
                }

                if pct is None:
                    pct = 0.0

                if pct < -30:
                    impact = "high"; confidence = 0.9
                elif pct < -15:
                    impact = "medium"; confidence = 0.75
                else:
                    impact = "low"; confidence = 0.5

            elif issue in ("ROAS Decline", "Low ROAS"):
                pct = d.get("roas_delta_pct", 0.0)
                evidence = {"roas_delta_pct": float(pct)}
                if pct < -30:
                    impact = "high"; confidence = 0.85
                elif pct < -10:
                    impact = "medium"; confidence = 0.65
                else:
                    impact = "low"; confidence = 0.4

            else:
                evidence = {"deltas_found": d}
                confidence = 0.25
                impact = "low"

            result = {
                "hypothesis": issue,
                "evidence": evidence,
                "impact": impact,
                "confidence": round(float(confidence), 3)
            }
            logger.info("Evaluator result: {}", result)
            results.append(result)

        return results
