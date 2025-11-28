from src.orchestrator.run import Orchestrator

def test_orchestrator_uses_custom_config(tmp_path):
    # create a temp sample config
    sample_conf = tmp_path / "config.yaml"
    sample_conf.write_text("""
data:
  dataset_path: data/dummy.csv
thresholds:
  low_ctr: 0.01
  low_roas: 1.0
""")

    orch = Orchestrator(config_path=str(sample_conf))
    assert orch.config["thresholds"]["low_ctr"] == 0.01
