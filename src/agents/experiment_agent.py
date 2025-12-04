from loguru import logger
from datetime import datetime
import pandas as pd

def summarize_run(baseline: dict, current: dict, deltas: dict, top_n_segments=3):
    summary = {
        "time": datetime.utcnow().isoformat(),
        "baseline": baseline,
        "current": current,
        "deltas": deltas,
    }

 
    highlights = []
    if deltas.get("ctr_delta_pct") is not None:
        highlights.append(f"CTR change: {deltas['ctr_delta_pct']:.2f}%")
    if deltas.get("roas_delta_pct") is not None:
        highlights.append(f"ROAS change: {deltas['roas_delta_pct']:.2f}%")
    summary["highlights"] = highlights

    seg_ctr = deltas.get("segment_ctr") or {}
    try:
        sorted_seg = sorted(seg_ctr.items(), key=lambda x: x[1])
        summary["worst_segments"] = sorted_seg[:top_n_segments]
    except Exception:
        summary["worst_segments"] = []

    logger.info("Run summary created: {}", summary["highlights"])
    return summary
