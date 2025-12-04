import pandas as pd
from src.agents.adaptive_thresholds import compute_percentile_thresholds

def test_percentile_thresholds_basic():
    df = pd.DataFrame({"ctr":[0.01,0.02,0.03,0.04,0.05],"roas":[1,2,3,4,5]})
    t = compute_percentile_thresholds(df, q=0.2)
    assert 0 <= t["low_ctr"] <= 0.03
    assert 1 <= t["low_roas"] <= 2
