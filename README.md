# Kasparro — Agentic Facebook Performance Analyst

A modular multi-agent system that analyzes Facebook Ads performance, detects CTR/ROAS issues, and generates improved creatives.  
Follows the Kasparro Agentic Assignment requirements: clean structure, agents, config, logs, tests, and reproducible pipeline.

---

## Quick Start

```bash
python -V   # should be >= 3.10
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 -m src.orchestrator.run "Analyze ROAS drop"
```

---

## Data

- Place your CSV under `data/`
- Default dataset:

```
data/synthetic_fb_ads_undergarments.csv
```

- Optional sample:

```
data/sample_fb_ads.csv
```

---

## Config

`config/config.yaml`:

```yaml
data:
  dataset_path: "data/synthetic_fb_ads_undergarments.csv"
  use_sample: false

thresholds:
  low_ctr: 0.015
  low_roas: 1.2
  fatigue_drop: 0.30

system:
  memory: false
  max_iterations: 3
```

---

## Repo Map

```
project/
├── config/
│   └── config.yaml
├── data/
│   └── synthetic_fb_ads_undergarments.csv
├── logs/
│   └── system.log
├── prompts/
├── reports/
│   ├── report.md
│   ├── insights.json
│   └── creatives.json
├── src/
│   ├── agents/
│   │   ├── planner_agent.py
│   │   ├── data_agent.py
│   │   ├── insight_agent.py
│   │   ├── evaluator_agent.py
│   │   └── creative_agent.py
│   ├── orchestrator/
│   │   └── run.py
├── tests/
│   └── test_evaluator.py
├── Makefile
├── requirements.txt
└── README.md
```

---

## Run

```bash
make run
```

or:

```bash
python3 -m src.orchestrator.run "Analyze ROAS drop"
```

---

## Outputs

```
reports/report.md
reports/insights.json
reports/creatives.json
logs/system.log
```

---

## Observability

Place any Langfuse or trace logs here:

```
reports/observability/
```

---

## Release

```
v1.0.0
```

---

## Self-Review Checklist

- [x] Repo structure correct  
- [x] config.yaml added  
- [x] Agents implemented  
- [x] Prompts stored in `/prompts`  
- [x] Reports generated  
- [x] Logs included  
- [x] Tests passing  
- [x] README complete  
- [x] v1.0.0 release published  
- [x] PR created  

---

# End of README
