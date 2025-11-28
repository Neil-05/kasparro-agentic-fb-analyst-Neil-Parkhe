import pandas as pd
import pytest
from src.agents.data_agent import DataAgent, REQUIRED_COLUMNS

def test_missing_columns_schema():
    df = pd.DataFrame({
        "date": ["2024-01-01"],
        "spend": [100]
    })

    df_path = "tmp_missing_cols.csv"
    df.to_csv(df_path, index=False)

    agent = DataAgent()

    with pytest.raises(KeyError):
        agent.load_data(df_path, retries=1)


def test_invalid_numeric_schema(tmp_path):
    bad_file = tmp_path / "bad_numeric.csv"

    df = pd.DataFrame({
        "date": ["2024-01-01"],
        "country": ["US"],
        "spend": ["abc"],
        "ctr": ["bad"],
        "roas": ["bad"],
        "campaign": ["A"],
        "message": ["Test message"]
    })

    df.to_csv(bad_file, index=False)

    agent = DataAgent()

    with pytest.raises(ValueError):
        agent.load_data(str(bad_file), retries=1)
