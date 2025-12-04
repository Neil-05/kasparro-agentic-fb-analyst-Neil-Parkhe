# src/agents/insight_agent.py

from loguru import logger
import math


class InsightAgent:
    def generate_hypotheses(self, summary, retries=1):
        logger.info("Generating insights using baseline/current deltas")

        # ------------- REQUIRED FALLBACK FOR TESTS -------------
        # Must return {"issue": "Unknown"} when:
        # - summary is empty
        # - summary missing avg_ctr
        # - avg_ctr is NaN
        if (
            not summary
            or "avg_ctr" not in summary
            or (isinstance(summary.get("avg_ctr"), float)
                and math.isnan(summary.get("avg_ctr")))
        ):
            return [{
                "issue": "Unknown",
                "reason": "Insufficient or invalid summary",
                "confidence": 0.0
            }]

        # ------------- V2 LOGIC (your real system) -------------
        deltas = summary.get("deltas", {})
        seg_ctr = summary.get("segment_ctr", {})

        hypotheses = []

        # CTR hypothesis
        if "ctr_delta_pct" in deltas:
            pct = deltas["ctr_delta_pct"]
            worst_seg = next(iter(seg_ctr.items()), ("unknown", None))

            hypotheses.append({
                "issue": "CTR Drop Detected",
                "reason": f"CTR dropped in {worst_seg[0]} segment.",
                "evidence": {
                    "ctr_delta_pct": pct,
                    "worst_segment": worst_seg[0],
                    "segment_ctr": worst_seg[1]
                },
                "confidence": max(0.2, min(0.9, abs(pct) / 100))
            })

        # ROAS hypothesis
        if "roas_delta_pct" in deltas:
            pct = deltas["roas_delta_pct"]

            hypotheses.append({
                "issue": "ROAS Decline",
                "reason": "ROAS fell significantly in the current period.",
                "evidence": {"roas_delta_pct": pct},
                "confidence": max(0.2, min(0.9, abs(pct) / 100))
            })

        # If nothing significant found
        if not hypotheses:
            return [{
                "issue": "Unknown",
                "reason": "No significant drift",
                "confidence": 0.0
            }]

        return hypotheses
