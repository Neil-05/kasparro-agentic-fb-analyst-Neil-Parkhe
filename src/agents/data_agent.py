import pandas as pd
import time

class DataAgent:
    def load_data(self, path, retries=3, delay=1):
        attempt = 0
        while attempt < retries:
            try:
                return pd.read_csv(path)
            except Exception as e:
                attempt += 1
                if attempt == retries:
                    raise e
                time.sleep(delay)

    def summarize(self, df):
        return {
            "date_range": [df["date"].min(), df["date"].max()],
            "total_spend": float(df["spend"].sum()),
            "avg_ctr": float(df["ctr"].mean()),
            "avg_roas": float(df["roas"].mean()),
            "top_countries": df["country"].value_counts().head(3).to_dict()
        }
