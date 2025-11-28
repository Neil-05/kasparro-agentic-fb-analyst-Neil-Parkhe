import pytest
import pandas as pd
from src.agents.data_agent import DataAgent, REQUIRED_COLUMNS


def test_data_agent_missing_columns(tmp_path):
    bad_file = tmp_path / "bad.csv"
    df = pd.DataFrame({"date": ["2024-01-01"], "spend": [100]})
    df.to_csv(bad_file, index=False)

    agent = DataAgent()
    with pytest.raises(KeyError):
        agent.load_data(str(bad_file), retries=1)


def test_data_agent_empty_file(tmp_path):
    empty_file = tmp_path / "empty.csv"
    pd.DataFrame().to_csv(empty_file, index=False)

    agent = DataAgent()
    with pytest.raises(ValueError):
        agent.load_data(str(empty_file), retries=1)


def test_data_agent_invalid_numeric(tmp_path):
    bad_numeric_file = tmp_path / "bad_numeric.csv"
    df = pd.DataFrame({
    "date": ["2024-01-01"],
    "country": ["US"],
    "spend": ["not_number"],
    "ctr": ["bad"],
    "roas": ["bad"],
    "campaign": ["A"],
    "message": ["sample creative"]
})

    df.to_csv(bad_numeric_file, index=False)

    agent = DataAgent()
    with pytest.raises(ValueError):
        agent.load_data(str(bad_numeric_file), retries=1)


def test_data_agent_retry_fail(tmp_path):
    missing_file = tmp_path / "no_file.csv"

    agent = DataAgent()
    with pytest.raises(Exception):
        agent.load_data(str(missing_file), retries=2, delay=0)
