import pandas as pd
from loguru import logger

def compute_percentile_thresholds(df: pd.DataFrame, q: float = 0.2) -> dict:
    thresholds = {}
    try:
        thresholds["low_ctr"] = float(df["ctr"].quantile(q))
    except Exception:
        thresholds["low_ctr"] = None
        logger.warning("Failed to compute adaptive low_ctr")

    try:
        thresholds["low_roas"] = float(df["roas"].quantile(q))
    except Exception:
        thresholds["low_roas"] = None
        logger.warning("Failed to compute adaptive low_roas")

    logger.info("Adaptive thresholds computed: {}", thresholds)
    return thresholds
