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

### MAKEFILE

make setup    # install dependencies
make run      # run full agentic system
make test     # run test suite
make clean    # clear logs + reports

---

## Repo Map

'''
project/
├── config/
│   ├── config.yaml
│   └── sample_small.yaml
├── schema/
│   └── data_schema.yaml
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
│   │   ├── creative_agent.py
│   │   ├── creative_score_agent.py
│   │   └── memory_agent.py
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
'''

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
* input snapshot
* output summary
* reasoning steps (“why this hypothesis was created”)
* retries & failures
* execution time
* final outputs

Stored at:

```
logs/system.json
```

---

## Developer-Focused Features

- **Fully config-driven architecture** — No hardcoded thresholds, file paths, or agent parameters.  
- **Schema validation layer** — Ensures safe, predictable data ingestion before processing.  
- **Column normalization** — Harmonizes input dataset column names for maximum compatibility.  
- **Per-agent structured logging** — Every agent logs actions in standardized JSON format.  
- **Retry system with failure logging** — Automatic retries on recoverable errors with detailed logs.  
- **Segmented performance analysis** — Breaks down performance by dimensions (campaign, ad group, creative, etc.).  
- **Clear fallback behaviors** — Example: generate `"Unknown"` hypotheses when data is insufficient.  
- **Automatic reports & logs** — Every run produces a summarized report plus detailed logs for debugging.  

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

## Agent Responsibilities

| **Agent**             | **Responsibility** |
|----------------------|--------------------|
| **PlannerAgent**     | Converts natural-language queries into a structured execution plan. |
| **DataAgent**        | Validates dataset columns/types, computes drift metrics, and retries on failure. |
| **InsightAgent**     | Generates CTR/ROAS hypotheses using quantified performance deltas. |
| **EvaluatorAgent**   | Assigns impact levels + confidence scores after validating hypotheses. |
| **CreativeScoreAgent** | Scores message/creative quality on a 0–100 scale. |
| **CreativeAgent**    | Rewrites creatives and ties improvements directly to identified issues. |
| **MemoryAgent**      | Writes full run history, failures, retries, and timestamps for observability. |

---

## Developer Notes

* Codebase is modular and agent-isolated.
* Extending the pipeline requires editing a single agent without breaking others.
* Dataset switching is fully config-based.
* Failures are surfaced cleanly with contextual logs—no silent errors.

## Release

```
v2.0.0
```

---

