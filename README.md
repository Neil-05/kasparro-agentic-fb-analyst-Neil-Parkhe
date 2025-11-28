# Kasparro — Agentic Facebook Performance Analyst

A modular multi-agent system that analyzes Facebook Ads performance, detects CTR/ROAS issues, performs schema validation, retries on failure, and generates improved creatives.  
Follows all Kasparro Agentic Assignment requirements: clean structure, agents, config, logs, tests, reproducibility, and dataset switching.

---

## Quick Start

```bash
python -V   # >= 3.10 recommended
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 -m src.orchestrator.run "Analyze ROAS drop"
```

---

## Data

### Default full dataset
```
data/synthetic_fb_ads_undergarments.csv
```

### Small sample (for testing)
```
data/sample_small.csv
```

### Data documentation
- Required columns enforced by schema validation:
```
date, country, spend, ctr, roas, campaign, message
```

If the dataset uses different names (example: `campaign_name`, `creative_message`), automatic column normalization is applied through mapping.

---

## Config

### Primary config
`config/config.yaml`:

```yaml
data:
  dataset_path: "data/synthetic_fb_ads_undergarments.csv"

thresholds:
  low_ctr: 0.015
  low_roas: 1.2
  fatigue_drop: 0.30

system:
  memory: false
```

### Secondary config for small dataset
`config/sample_small.yaml`:

```yaml
data:
  dataset_path: "data/sample_small.csv"

thresholds:
  low_ctr: 0.012
  low_roas: 1.5
```

### CLI config override

```bash
python3 src/orchestrator/run.py --config config/sample_small.yaml
```

---

## Repo Map

```
project/
├── config/
│   ├── config.yaml
│   └── sample_small.yaml
├── data/
│   ├── synthetic_fb_ads_undergarments.csv
│   └── sample_small.csv
├── logs/
│   └── system.json
├── prompts/
│   └── planner_prompt.md
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
│   ├── test_planner_agent.py
│   ├── test_data_agent.py
│   ├── test_data_agent_retry.py
│   ├── test_data_agent_errors.py
│   ├── test_insight_agent.py
│   ├── test_insight_agent_retry.py
│   ├── test_insight_agent_errors.py
│   ├── test_schema_validation.py
│   ├── test_logging_exists.py
│   └── test_evaluator.py
├── Makefile
├── requirements.txt
└── README.md
```

---

## Run

### Full system:
```bash
make run
```

### Using alternative config:
```bash
python3 src/orchestrator/run.py --config config/sample_small.yaml
```

---

## Outputs

Generated on every run:

```
reports/report.md
reports/insights.json
reports/creatives.json
logs/system.json
```

---

## Observability

Structured logs stored in:

```
logs/system.json
```

Each log entry includes:
- agent name  
- stage  
- retries  
- errors  
- dataset path  
- success/failure states  

---

## Failure Modes (Documented)

### 1. Missing columns
```
KeyError: Missing required columns: [...]
```

### 2. Invalid numeric values
```
ValueError: Non-numeric values found in spend/ctr/roas
```

### 3. Empty file
```
ValueError: Dataset is empty
```

### 4. Retry exhaustion
```
Exception: DataAgent: Failed to load CSV after retries
```

### 5. Insight generation fallback
If retries fail:
```
{"issue": "Unknown", "reason": "Insufficient data", "confidence": 0.0}
```

---

## Release

Version:
```
v1.0.0
```

---

## Self-Review Checklist

- [x] Correct repo name format  
- [x] README includes quick start + commands  
- [x] Config present with thresholds  
- [x] All agents implemented with I/O schema  
- [x] Prompts stored in `/prompts`  
- [x] Reports generated  
- [x] JSON logs included  
- [x] Unit tests for all agents  
- [x] Schema validation  
- [x] Retry logic implemented  
- [x] Makefile included  
- [x] v1.0.0 release tag  
- [x] PR with self-review  
- [x] Dynamic config switching  
- [x] Sample dataset provided  

---

# End of README
