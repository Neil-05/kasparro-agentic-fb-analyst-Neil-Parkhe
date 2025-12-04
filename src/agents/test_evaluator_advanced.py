import pandas as pd
from src.agents.evaluator_agent import EvaluatorAgent

def test_advanced_evaluator_outputs_rich_evidence():
    df = pd.DataFrame({
        "ctr": [0.02, 0.01],
        "roas": [1.5, 0.9],
        "spend": [100, 120],
        "country": ["US", "US"]
    })

    deltas = {
        "deltas": {
            "ctr_delta_pct": -25,
            "roas_delta_pct": -40
        },
        "segment_ctr": {"US": 0.01}
    }

    evaluator = EvaluatorAgent(config={})
    hypotheses = [{"issue": "CTR Drop Detected"}]

    out = evaluator.evaluate(df, hypotheses, deltas)
    assert "evidence" in out[0]
    assert "impact" in out[0]
    assert out[0]["impact"] in ["low", "medium", "high"]
