2026 April - NTU PACE - Data Science &amp; AI - Capstone Project

# 🚚 Ninja Van AI Control Tower

> A Multi-Agent System for Predictive, Explainable, and Coordinated Logistics Decision-Making

---

## 🧠 Overview

This project presents a proof-of-concept **AI Control Tower** designed to address key logistics challenges using a multi-agent architecture.

It integrates machine learning models, decision logic, explainability, and a lightweight knowledge system to simulate how modern logistics operations can be coordinated through AI.

---

## 🎯 Problem Scope

This project addresses selected Ninja Van problem statements:

- 📦 Demand Forecasting
- 🚚 Delivery Failure Prediction
- 🔧 Predictive Maintenance
- 📚 Customer Support (RAG-lite)
- 🧠 Multi-Agent Control Tower

---

## 🏗️ System Architecture

> 📐 *Text-based mockup — to be replaced with a draw.io diagram.*

```text
┌──────────────────────────────────────────────┐
│      🏷️ Ninja Van AI Control Tower           │
└──────────────────────────────────────────────┘


🔵 INPUT LAYER
┌──────────────────────────────┐
│ 👤 User / Operations Staff   │
│ Driver | Planner | Ops Mgr   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│ 🖥️ Gradio Web UI                             │
│ - Real-time sliders                          │
│ - Batch CSV upload                           │
└──────────────┬───────────────────────────────┘
               │
               ▼


🟣 ORCHESTRATION LAYER
┌──────────────────────────────────────────────┐
│ 🧠 Master Orchestrator                       │
│ run_ninjai_system()                          │
│ - build_input_df()                           │
│ - shared_state + decision_logs               │
│ - routes tasks to agents                     │
└──────────────┬───────────────────────────────┘
               │
               ▼


🟢 PREDICTIVE AGENT LAYER
        ┌──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 📦 Demand    │ │ 🚚 Delivery  │ │ 🔧 Mainten-  │
│ Agent        │ │ Risk Agent   │ │ ance Agent   │
│ Regression   │ │ Classific.   │ │ Classific.   │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       └─────────────────┼────────────────┘
                         ▼


🟠 DECISION LAYER
┌──────────────────────────────────────────────┐
│ 🧠 Control Tower Agent                       │
│ - final_risk_score                           │
│ - recommendation engine                      │
│ - cross-agent coordination                   │
└───────┬───────────────┬──────────────────────┘
        │               │
        ▼               ▼


🟡 INTELLIGENCE AUGMENTATION
┌──────────────────────┐ ┌──────────────────────┐
│ 📚 Support Agent     │ │ 🔍 Explainability    │
│ (RAG-lite)           │ │ Agent                │
│ - SOP guidance       │ │ - key drivers        │
│ - action suggestions │ │ - transparency       │
└──────────┬───────────┘ └──────────┬───────────┘
           └──────────────┬─────────┘
                          ▼


⚪ OUTPUT LAYER
┌──────────────────────────────────────────────┐
│ 📊 Control Tower Report                      │
│ - predicted volume                           │
│ - failure probability                        │
│ - maintenance risk                           │
│ - recommendations                            │
│ - explanations                               │
└──────────────┬───────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│ 📜 Decision Logs                             │
│ - historical records                         │
│ - shared_state snapshots                     │
└──────────────┬───────────────────────────────┘
               │
               ▼


⚫ TRUST LAYER (dApp)
┌──────────────────────────────────────────────┐
│ 🔐 Simulated Proof-of-Delivery               │
│ - delivery record                            │
│ - SHA256 hash                                │
│ - timestamp                                  │
│                                              │
│ Future:                                      │
│ → Smart contract (Ethereum)                  │
│ → Immutable proof                            │
└──────────────────────────────────────────────┘
```

---

## 🧩 Core Components

### 1. 📦 Demand Forecasting Agent
- Predicts daily parcel volume using regression models
- Helps anticipate operational load

### 2. 🚚 Delivery Failure Risk Agent
- Predicts probability of delivery failure
- Supports proactive intervention before dispatch

### 3. 🔧 Predictive Maintenance Agent
- Estimates vehicle breakdown risk
- Enables preventive maintenance decisions

### 4. 📚 RAG-lite Support Agent
- Provides operational recommendations using a structured knowledge base
- Bridges predictions with actionable decisions

> **Note:** Current version uses rule-based retrieval. Future upgrade: vector-based RAG with semantic search.

### 5. 🔍 Explainability Agent
- Identifies key contributing factors behind predictions
- Improves transparency and decision trust

### 6. 🧠 Control Tower Agent
- Combines outputs from all agents
- Produces coordinated recommendations based on system-wide risk

---

## ⚙️ Technology Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Scikit-learn | ML models |
| Pandas | Data processing |
| Gradio (Hugging Face Spaces) | UI & deployment |
| Joblib | Model serialization |

---

## 📊 Dataset (Simulated)

Due to the absence of real operational data, a synthetic logistics dataset was generated.

**Features:**
- `distance_km`
- `num_stops`
- `hub_congestion`
- `traffic_level`
- `weather_rain`
- `vehicle_mileage_km`
- `days_since_service`
- `driver_experience`
- `current_load`

**Targets:**
- `parcel_volume` *(regression)*
- `delivery_failed` *(classification)*
- `breakdown_risk` *(classification)*

> **Key Design Choice:** Controlled noise is introduced to avoid overfitting to rule-based logic and simulate real-world uncertainty.

---

## 🗂️ Sample CSV Input (Batch Prediction)

The file `sample_operations_input.csv` represents a pre-dispatch daily planning dataset. Each row corresponds to one planned delivery trip or route.

### Required ML Input Columns

| Column | Description |
|--------|-------------|
| `distance_km` | Planned delivery distance |
| `num_stops` | Number of delivery stops |
| `hub_congestion` | Hub congestion score (0–1) |
| `traffic_level` | Traffic severity score (0–1) |
| `weather_rain` | 1 = raining, 0 = not raining |
| `vehicle_mileage_km` | Vehicle mileage |
| `days_since_service` | Days since last servicing |
| `driver_experience` | Driver experience in years |
| `current_load` | Vehicle load percentage |

### Optional Operational Metadata Columns

| Column | Purpose |
|--------|---------|
| `trip_id` | Identifies each planned route |
| `driver_id` | Assigned driver |
| `vehicle_id` | Assigned vehicle |
| `route_zone` | Delivery region |
| `planned_dispatch_hour` | Planned departure time |

### Example CSV

```csv
trip_id,driver_id,vehicle_id,route_zone,planned_dispatch_hour,distance_km,num_stops,hub_congestion,traffic_level,weather_rain,vehicle_mileage_km,days_since_service,driver_experience,current_load
TRIP_A,D001,V001,Zone_A,9,12.5,8,0.7,0.8,1,190000,130,2,85
TRIP_B,D002,V002,Zone_B,10,6.0,3,0.2,0.3,0,65000,45,5,40
```

### How It Is Used

```text
Daily planning CSV
→ Each row = one planned trip
→ System extracts required ML features
→ AI Control Tower evaluates each trip
→ Outputs risk score, recommendations, and explanations
```

> This enables pre-dispatch decision-making before vehicles leave the hub.

---

## 📈 Model Evaluation

> ⚠️ These metrics validate pipeline integration, not production performance. Production systems would require real data, train/test splits, and cross-validation.

| Model | Metric | Value |
|-------|--------|-------|
| Demand Forecasting | MAE | ~6–7 |
| Demand Forecasting | RMSE | ~7–8 |
| Delivery Failure Prediction | Accuracy | ~0.80 |
| Predictive Maintenance | Accuracy | ~0.85–0.90 |

---

## 🤖 Multi-Agent Design

| Agent | Role |
|-------|------|
| Demand Agent | Predicts parcel volume |
| Delivery Risk Agent | Predicts failure probability |
| Maintenance Agent | Predicts breakdown risk |
| Support Agent | Provides operational guidance |
| Explainability Agent | Explains predictions |
| Control Tower Agent | Coordinates decisions |

---

## 🔐 Simulated dApp Layer

A placeholder proof-of-delivery system that:
- Generates a delivery record
- Computes a SHA256 hash
- Returns a verifiable proof object

**Purpose:** Demonstrates trust layer integration and simulates tamper-resistant record systems.

**Future Upgrade:**
- Ethereum smart contract deployment
- Immutable on-chain proof-of-delivery

---

## 🌐 Deployment

Deployed using **Gradio on Hugging Face Spaces**.

- ✅ Real-time scenario simulation (UI inputs)
- ✅ Batch CSV prediction (daily planning)
- ✅ Recommendation engine
- ✅ Explainability output
- ✅ Decision logging
- ✅ Proof-of-delivery simulation

---

## 🔄 System Evolution

This project was developed iteratively, reflecting the evolution from standalone models to an integrated AI system:

```text
ML Prototype → Realistic Data → Noise Injection → Multi-Agent System
→ Explainability → Decision Layer → Deployment → Trust Layer
```

---

## 🔌 Real Data Ingestion Path

In a production setting, data ingestion replaces manual UI input while the agent pipeline remains unchanged:

```text
Operational CSV / Database / API
→ Data validation
→ Feature extraction
→ Model inference
→ Agent orchestration
→ Control Tower output
```

The system extracts required ML columns while preserving metadata for logging and traceability. Future data sources may include:

- 🗄️ Shipment management database
- 🔧 Fleet maintenance system
- 👤 Driver assignment system
- 🌦️ Weather API
- 🚦 Traffic API
- 🎫 Customer support ticket system

---

## 📚 RAG Upgrade Path

Current version uses a RAG-lite structured knowledge base:

```python
SUPPORT_KB = {
    "high_delivery_failure": "...",
    "high_maintenance_risk": "...",
    "high_demand": "..."
}
```

Future full RAG version would use a document library:

```text
docs/
  delivery_sop.md
  customer_support_faq.md
  maintenance_policy.md
  escalation_guide.md
```

Production RAG flow:

```text
Query / operational event
→ embed query
→ retrieve relevant SOP/FAQ chunks
→ generate grounded response
→ escalate if confidence is low
```

Possible RAG tools: [FAISS](https://github.com/facebookresearch/faiss), [ChromaDB](https://www.trychroma.com/), [sentence-transformers](https://www.sbert.net/), [LangChain](https://www.langchain.com/) / [LlamaIndex](https://www.llamaindex.ai/), FastAPI RAG endpoint.

---

## 🧱 Modular Production Upgrade Plan

This prototype is intentionally modular — each component can be replaced or upgraded independently without rewriting the full system.

| Prototype Component | Production Upgrade |
|---|---|
| Synthetic dataset | Real shipment, delivery, fleet, and support data |
| Manual Gradio inputs | CSV upload, database query, or API ingestion |
| Joblib ML models | Model registry + scheduled retraining |
| RAG-lite dictionary | Vector database + SOP document retrieval |
| In-memory logs | PostgreSQL, BigQuery, or cloud logging |
| Simulated dApp hash | Smart contract proof-of-delivery |
| Gradio demo | FastAPI backend + web/mobile frontend |
| Rule-based orchestration | LangGraph / tool-calling agent workflow |

---

## 🚀 Future Improvements

- [ ] CSV upload validation
- [ ] Batch prediction output table in UI
- [ ] Persistent decision logging
- [ ] Model retraining pipeline
- [ ] Modular code structure (`agents.py`, `models.py`, `rag_lite.py`, `app.py`)
- [ ] Replace RAG-lite with full vector-based RAG
- [ ] Deploy scalable backend (FastAPI + cloud infrastructure)

---

## 🧠 Key Takeaway

This project demonstrates how **multiple AI components can be integrated into a unified control system** to support predictive, explainable, and coordinated logistics decision-making.

---

> 📌 **Note:** This is a proof-of-concept system focused on architecture and integration — not production optimization.
