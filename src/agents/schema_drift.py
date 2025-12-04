from loguru import logger
from typing import List, Dict

def detect_schema_drift(prev_columns: List[str], current_columns: List[str]) -> Dict:
    prev_set = set(prev_columns or [])
    curr_set = set(current_columns or [])

    missing = list(prev_set - curr_set)
    new = list(curr_set - prev_set)

    drift = {
        "missing_columns": missing,
        "new_columns": new,
        "drifted": bool(missing or new)
    }

    if drift["drifted"]:
        logger.warning("Schema drift detected: missing=%s new=%s", missing, new)
    else:
        logger.info("No schema drift detected")

    return drift
