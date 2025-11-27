
# 🧠 Kasparro Agentic FB Analyst

A fully automated **multi-agent system** that analyzes Facebook Ads performance, diagnoses issues, and generates actionable creative recommendations using a clean, modular agentic architecture.

This project follows the structure and requirements of the **Kasparro Agentic Assignment**, ensuring:

- Clean directory structure  
- Agents with clear I/O schema  
- Configurable thresholds  
- Logs and test coverage  
- Reproducible orchestrator pipeline  
- Reports generated automatically  
- Release-ready repository  

---

## 🚀 System Architecture

```

+-----------------------+
|     Planner Agent     |
|  Interprets the task  |
+-----------+-----------+
|
v
+-----------------------+
|      Data Agent       |
| Loads & summarizes DF |
+-----------+-----------+
|
v
+-----------------------+
|     Insight Agent     |
|  Generates hypotheses |
+-----------+-----------+
|
v
+-----------------------+
|    Evaluator Agent    |
| Validates hypotheses  |
+-----------+-----------+
|
v
+-----------------------+
|    Creative Agent     |
| Suggests creatives    |
+-----------+-----------+
|
v
+-----------------------+
|      Orchestrator     |
| Runs full pipeline    |
+-----------------------+

```

---

## 📁 Folder Structure

```

project/
├── config/
│   └── config.yaml
├── data/
│   └── your_dataset.csv
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
│   └── utils/
├── tests/
│   └── test_evaluator.py
├── requirements.txt
├── .gitignore
└── README.md

````

---

## ⚙️ Configuration

`config/config.yaml` controls dataset path, thresholds, and system settings.

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
````

### Threshold Logic Examples

* CTR drop from **0.02 → 0.013** → below low_ctr → flag low performance
* ROAS drop from **2.1 → 0.9** → below low_roas → inefficiency
* CTR decline **>30% WoW** → fatigue risk

---

## 🧩 Agent Responsibilities

### 1. Planner Agent

* Interprets the query
* Breaks the task into subtasks
* Guides orchestrator execution

### 2. Data Agent

* Loads dataset from disk
* Generates summary metrics:

  * Average CTR
  * Average ROAS
  * Total spend
  * Date range
  * Top countries

### 3. Insight Agent

* Produces hypotheses such as:

  * Low CTR
  * Low ROAS
  * Audience mismatch
  * Fatigue signals

### 4. Evaluator Agent

* Validates hypotheses using thresholds from config
* Ensures JSON-safe output (Python-native bools)

### 5. Creative Agent

* Suggests improved creatives using rules
* Highlights benefits
* Adds urgency CTAs
* Improves emotional storytelling

---

## 🏁 How to Run the Full System

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the orchestrator pipeline

```bash
python3 -m src.orchestrator.run
```

### 📂 Outputs generated:

```
reports/insights.json
reports/creatives.json
reports/report.md
logs/system.log
```

---

## 🧪 Running Tests

Run all tests:

```bash
pytest
```

Expected:

```
1 passed
```

---

## 📊 Example Output (Real Run)

### Insights:

```json
[
  {
    "issue": "Low CTR",
    "value": 0.0131,
    "threshold": 0.015,
    "valid": true
  }
]
```

### Creatives:

```json
{
  "campaign": "Men ComfortMax Launch",
  "old_message": "Breathable bamboo that moves with you",
  "new_creatives": [
    "Add urgency CTA",
    "Highlight benefits",
    "Increase emotional storytelling"
  ]
}
```

---

## 📘 Logs & Reports

```
logs/system.log         → runtime logs  
reports/insights.json   → validated insights  
reports/creatives.json  → creative recommendations  
reports/report.md       → final combined report  
```

---

## 🔮 Future Enhancements

* Real-time dashboard
* Audience clustering
* LTV-weighted creative scoring
* Zero-shot creative scoring using LLMs
* Multi-language creative suggestions

---

## ⭐ Unique Enhancement (Required by Assignment)

👉 **Reserved for your final unique improvement.**
Examples you may add:

* Memory-enabled insight refinement
* Multi-query mode
* Creative clustering by themes
* Automatic root-cause analysis agent
* LLM-based insight scoring agent



---

## 🏷 Version

```
v1.0.0
```

---

# ✔️ End of README

```

---

```
