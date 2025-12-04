import time
import yaml
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
    def __init__(self):
        self.load_schema()

    def load_schema(self):
        schema_path = Path("schema/data_schema.yaml")
        if not schema_path.exists():
            raise FileNotFoundError("Schema file missing at schema/data_schema.yaml")
        with open(schema_path, "r") as f:
            schema = yaml.safe_load(f)
        self.required_cols = schema.get("required_columns", [])
        self.type_map = schema.get("types", {})

    def load_data(self, path, retries=3, delay=1):
        logger.bind(agent="data", step="load_start", path=path).info("Loading data")
        last_error = None

        for attempt in range(1, retries + 1):
            try:
                df = pd.read_csv(path)
                if df.empty:
                    raise ValueError("Dataset is empty")

                df = df.rename(columns=COLUMN_MAP)

                missing_cols = [c for c in self.required_cols if c not in df.columns]
                if missing_cols:
                    raise KeyError(f"Schema mismatch: missing columns {missing_cols}")

                df = df.replace([float("inf"), float("-inf")], pd.NA)

                if df[["spend", "ctr", "roas"]].isna().any(axis=None):
                    df = df.dropna(subset=["spend", "ctr", "roas"])
                    if df.empty:
                        raise ValueError("All rows dropped after cleaning numeric NaNs")

                for col, expected_type in self.type_map.items():
                    if expected_type == "float":
                        df[col] = pd.to_numeric(df[col], errors="raise")
                    elif expected_type == "str":
                        df[col] = df[col].astype(str)

                logger.bind(agent="data", step="load_success", rows=len(df)).info("Data loaded")
                return df

            except Exception as e:
                last_error = e
                logger.bind(agent="data", step="load_retry", attempt=attempt, error=str(e)).warning("Load failed — retrying")
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

        try:
            ctr_delta_pct = ((curr["ctr"] - base["ctr"]) / base["ctr"]) * 100 if base["ctr"] else 0.0
        except Exception:
            ctr_delta_pct = 0.0

        try:
            roas_delta_pct = ((curr["roas"] - base["roas"]) / base["roas"]) * 100 if base["roas"] else 0.0
        except Exception:
            roas_delta_pct = 0.0

        try:
            spend_delta_pct = ((curr["spend"] - base["spend"]) / base["spend"]) * 100 if base["spend"] else 0.0
        except Exception:
            spend_delta_pct = 0.0

        deltas = {
            "ctr_delta_pct": ctr_delta_pct,
            "roas_delta_pct": roas_delta_pct,
            "spend_delta_pct": spend_delta_pct,
        }

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

        logger.bind(agent="data", step="compute_deltas", deltas=deltas, worst_segment=worst_segment).info("Deltas computed")

        return {
            "baseline": base,
            "current": curr,
            "deltas": deltas,
            "segment_ctr": seg_ctr,
            "worst_segment": worst_segment,
            "worst_value": worst_value
        }

 
    def compute_deltas(self, df):
     
        logger.info("Computing baseline vs current performance")

      
        mid = len(df) // 2
        baseline = df.iloc[:mid]
        current = df.iloc[mid:]

        def avg_metrics(d):
            return {
                "ctr": d["ctr"].mean(),
                "roas": d["roas"].mean(),
                "spend": d["spend"].mean(),
            }

        base = avg_metrics(baseline)
        curr = avg_metrics(current)

   
        deltas = {
            "ctr_delta_pct": ((curr["ctr"] - base["ctr"]) / base["ctr"]) * 100 if base["ctr"] != 0 else 0,
            "roas_delta_pct": ((curr["roas"] - base["roas"]) / base["roas"]) * 100 if base["roas"] != 0 else 0,
            "spend_delta_pct": ((curr["spend"] - base["spend"]) / base["spend"]) * 100 if base["spend"] != 0 else 0,
        }
        seg = (
            df.groupby("country")["ctr"]
            .mean()
            .sort_values()
            .to_dict()
        )

        return {
            "baseline": base,
            "current": curr,
            "deltas": deltas,
            "segment_ctr": seg
        }
