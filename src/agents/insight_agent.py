from loguru import logger
import math


class InsightAgent:
    def generate_hypotheses(self, summary, retries=1):
        logger.bind(agent="insight", step="start").info("Generating insights")

        if (
            not summary
            or "avg_ctr" not in summary
            or (isinstance(summary.get("avg_ctr"), float)
                and math.isnan(summary.get("avg_ctr")))
        ):
            logger.bind(agent="insight", reason="invalid_summary").warning(
                "Fallback triggered: summary missing or invalid"
            )
            return [{
                "issue": "Unknown",
                "reason": "Insufficient or invalid summary",
                "confidence": 0.0
            }]

        deltas = summary.get("deltas", {})
        seg_ctr = summary.get("segment_ctr", {})

        logger.bind(
            agent="insight",
            deltas=deltas,
            segments=list(seg_ctr.keys())
        ).info("Received performance deltas and segment CTR")

        hypotheses = []

        if "ctr_delta_pct" in deltas:
            pct = deltas["ctr_delta_pct"]
            worst_seg = next(iter(seg_ctr.items()), ("unknown", None))

            logger.bind(
                agent="insight",
                metric="CTR",
                delta_pct=pct,
                worst_segment=worst_seg
            ).info("Evaluating CTR drift")

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

     
        if "roas_delta_pct" in deltas:
            pct = deltas["roas_delta_pct"]

            logger.bind(
                agent="insight",
                metric="ROAS",
                delta_pct=pct
            ).info("Evaluating ROAS drift")

            hypotheses.append({
                "issue": "ROAS Decline",
                "reason": "ROAS fell significantly in the current period.",
                "evidence": {"roas_delta_pct": pct},
                "confidence": max(0.2, min(0.9, abs(pct) / 100))
            })

        if not hypotheses:
            logger.bind(agent="insight").info("No drift detected; returning fallback hypothesis")
            return [{
                "issue": "Unknown",
                "reason": "No significant drift",
                "confidence": 0.0
            }]

        logger.bind(agent="insight", count=len(hypotheses)).info(
            "Finished generating hypotheses"
        )

        return hypotheses



      