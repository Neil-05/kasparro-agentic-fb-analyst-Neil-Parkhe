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

## ⚠️ Running Tests — Important Note

If you installed packages inside a virtual environment (.venv) but your system still runs the global pytest (Anaconda/macOS), your tests may fail with import errors.

### ✅ Always run tests like this:

```bash
python -m pytest
```

This ensures:

* Virtual environment Python is used
* `src/` package resolves correctly
* All dependencies (pandas, loguru, etc.) load properly

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

Required columns (validated by schema):

```
date, country, spend, ctr, roas, campaign, message
```

If a dataset uses alternate names (`campaign_name`, `creative_message`), automatic normalization applies.

---

## Config

### Primary config (`config/config.yaml`)

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

### Small dataset config (`config/sample_small.yaml`)

```yaml
data:
  dataset_path: "data/sample_small.csv"

thresholds:
  low_ctr: 0.012
  low_roas: 1.5
```

### CLI override

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

### Full system

```bash
make run
```

### With custom config

```bash
python3 src/orchestrator/run.py --config config/sample_small.yaml
```

---

## Outputs

Generated on each run:

```
reports/report.md
reports/insights.json
reports/creatives.json
logs/system.json
```

---

## Observability

Structured logs include:

* agent name
* stage
* retries
* errors
* dataset path
* success/failure markers

Stored at:

```
logs/system.json
```

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

### 5. Insight fallback

```
{"issue": "Unknown", "reason": "Insufficient data", "confidence": 0.0}
```

---

## P1 Enhancements

* Dynamic config switching (`--config` flag)
* Automatic schema validation
* Column normalization layer
* Sample dataset included
* Documentation of failure modes
* Test coverage for retry logic, schema validation, and alternate configs

## P2 Enchancements

* Memory for short runs
* Basic quality scoring agent

---

## Release

```
v2.0.0
```

---

## Self-Review Checklist

* [x] Correct repo name format
* [x] README includes quick start + commands
* [x] Config system implemented
* [x] All agents implemented
* [x] Prompts stored in `/prompts`
* [x] Reports generated
* [x] JSON logs included
* [x] Unit tests for all agents
* [x] Schema validation
* [x] Retry logic
* [x] Makefile
* [x] Release tag
* [x] PR with self-review
* [x] Dynamic config switching
* [x] Sample dataset included
* [x] Memory for short runs
* [x] Basic quality scoring logic

---

# End of README
