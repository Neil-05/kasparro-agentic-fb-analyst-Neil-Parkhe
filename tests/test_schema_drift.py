from src.agents.schema_drift import detect_schema_drift

def test_detect_schema_no_drift():
    prev = ["a","b","c"]
    curr = ["a","b","c","d"]
    r = detect_schema_drift(prev, curr)
    assert r["drifted"] is True
    assert "d" in r["new_columns"]

def test_detect_schema_missing():
    prev = ["date","ctr","roas"]
    curr = ["ctr","roas"]
    r = detect_schema_drift(prev, curr)
    assert r["drifted"] is True
    assert "date" in r["missing_columns"]
