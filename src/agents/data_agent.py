import time
from pathlib import Path
import pandas as pd
from loguru import logger

REQUIRED_COLUMNS = ["date", "country", "spend", "ctr", "roas", "campaign", "message"]

COLUMN_MAP = {
    "campaign_name": "campaign",
    "creative_message": "message",
    "adset_name": "adset",
    "creative_type": "creative_type"
}


class DataAgent:
    def load_data(self, path, retries=3, delay=1):
        logger.bind(agent="data", step="load_start", path=path).info("Loading data")
        last_error = None

        for attempt in range(1, retries + 1):
            try:
                df = pd.read_csv(path)
                if df.empty:
                    raise ValueError("Dataset is empty")

               
                df = df.rename(columns=COLUMN_MAP)

                missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
                if missing_cols:
                    msg = f"Missing required columns after normalization: {missing_cols}"
                    logger.error(msg)
                    raise KeyError(msg)

                df = df.replace([float("inf"), float("-inf")], pd.NA)

                if df[["spend", "ctr", "roas"]].isna().any(axis=None):
                    logger.warning("NaN detected in numeric columns; dropping NaN rows")
                    df = df.dropna(subset=["spend", "ctr", "roas"])
                    if df.empty:
                        raise ValueError("All rows dropped after cleaning numeric NaNs")

                for col in ["spend", "ctr", "roas"]:
                    try:
                        df[col] = pd.to_numeric(df[col], errors="raise")
                    except Exception as e:
                        logger.error(f"Invalid numeric value in '{col}': {e}")
                        raise ValueError(f"Invalid value in column '{col}'")

                logger.bind(agent="data", step="load_success", rows=len(df)).info("Data loaded")
                return df

            except Exception as e:
                last_error = e
                logger.bind(agent="data", step="load_retry", attempt=attempt, error=str(e)).warning(
                    "Load failed — retrying"
                )
                time.sleep(delay)

        logger.bind(agent="data", step="load_failed", error=str(last_error)).error("Failed after retries")
        raise last_error

    def summarize(self, df):
        try:
            return {
                "date_range": [str(df["date"].min()), str(df["date"].max())],
                "total_spend": float(df["spend"].sum()),
                "avg_ctr": float(df["ctr"].mean()),
                "avg_roas": float(df["roas"].mean()),
                "top_countries": df["country"].value_counts().head(3).to_dict(),
            }
        except Exception as e:
            logger.error("DataAgent.summarize failed: {}", e)
            raise

    def compute_deltas(self, df):
        logger.bind(agent="data", step="compute_deltas").info("Computing baseline vs current performance")
     
        if len(df) < 4:
            base = {"ctr": df["ctr"].mean(), "roas": df["roas"].mean(), "spend": df["spend"].mean()}
            curr = base
        else:
            mid = len(df) // 2
            baseline = df.iloc[:mid]
            current = df.iloc[mid:]
            base = {"ctr": baseline["ctr"].mean(), "roas": baseline["roas"].mean(), "spend": baseline["spend"].mean()}
            curr = {"ctr": current["ctr"].mean(), "roas": current["roas"].mean(), "spend": current["spend"].mean()}

        deltas = {}
        try:
            deltas["ctr_delta_pct"] = ((curr["ctr"] - base["ctr"]) / base["ctr"]) * 100 if base["ctr"] else 0.0
        except Exception:
            deltas["ctr_delta_pct"] = 0.0
        try:
            deltas["roas_delta_pct"] = ((curr["roas"] - base["roas"]) / base["roas"]) * 100 if base["roas"] else 0.0
        except Exception:
            deltas["roas_delta_pct"] = 0.0
        try:
            deltas["spend_delta_pct"] = ((curr["spend"] - base["spend"]) / base["spend"]) * 100 if base["spend"] else 0.0
        except Exception:
            deltas["spend_delta_pct"] = 0.0

      
        try:
            seg_ctr = df.groupby("country")["ctr"].mean().sort_values().to_dict()
        except Exception:
            seg_ctr = {}

        try:
            worst_segment = min(seg_ctr, key=seg_ctr.get) if seg_ctr else "unknown"
            worst_value = seg_ctr.get(worst_segment, None)
        except Exception:
            worst_segment = "unknown"
            worst_value = None

        logger.bind(agent="data", step="compute_deltas", deltas=deltas, worst_segment=worst_segment).info(
            "Deltas computed"
        )

        return {"baseline": base, "current": curr, "deltas": deltas, "segment_ctr": seg_ctr, "worst_segment": worst_segment, "worst_value": worst_value}
