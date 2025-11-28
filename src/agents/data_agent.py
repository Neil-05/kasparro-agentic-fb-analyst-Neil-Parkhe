import pandas as pd
import time
from loguru import logger

REQUIRED_COLUMNS = ["date", "country", "spend", "ctr", "roas", "campaign", "message"]

class DataAgent:

    def load_data(self, path, retries=3, delay=1):
        logger.bind(agent="data", step="load_start", path=path).info("Loading data")

        last_error = None

        for attempt in range(1, retries + 1):
            try:
                df = pd.read_csv(path)

                # Empty check
                if df.empty:
                    raise ValueError("Dataset is empty")

                # Required schema check
                missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
                if missing_cols:
                    raise KeyError(f"Missing required columns: {missing_cols}")

                # Validate numeric columns
                for col in ["spend", "ctr", "roas"]:
                    if not pd.api.types.is_numeric_dtype(df[col]):
                        raise ValueError(f"Invalid numeric value in column: {col}")

                logger.bind(agent="data", step="load_success", rows=len(df)).info("Data loaded")
                return df

            except Exception as e:
                last_error = e
                logger.bind(agent="data", step="load_retry", attempt=attempt, error=str(e)).warning(
                    "Load failed — retrying"
                )
                time.sleep(delay)

        logger.bind(agent="data", step="load_failed").error("Failed after retries")
        raise last_error

    def summarize(self, df):
        return {
            "date_range": [df["date"].min(), df["date"].max()],
            "total_spend": float(df["spend"].sum()),
            "avg_ctr": float(df["ctr"].mean()),
            "avg_roas": float(df["roas"].mean()),
            "top_countries": df["country"].value_counts().head(3).to_dict()
        }
