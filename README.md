# VisaOps Risk Intelligence Console

A production-style **operational risk monitoring and early-warning system** for visa processing centers, combining signal engineering, regime detection, and automated decision memo generation.

This project demonstrates how **service delivery operations** (e.g. visa centers, public services, back-office ops) can be monitored using **composite stress indices** rather than isolated KPIs — enabling earlier intervention and clearer decision support.

> ⚠️ All data used in this project is **synthetic, non-sensitive**, and generated solely for demonstration and research purposes.

---

## 🔗 Live Demo & Outputs

- **Live Dashboard (Streamlit):**  
  👉 *<YOUR STREAMLIT APP URL HERE>*

- **Automated PDF Risk Memo:**  
  Generated directly from the dashboard, including:
  - Current regime classification  
  - Last 7-day operational drivers  
  - Embedded stress & regime timeline  

---

## 🧠 Problem Motivation

Operational teams often monitor dozens of metrics:
- Turnaround time (TAT)
- Queue size
- Utilization
- Throughput

In practice, this creates **signal overload**:
- No single indicator explains *how stressed* the system is  
- Early warning is reactive rather than proactive  
- Decision updates remain descriptive, not diagnostic  

**This system answers three operational questions clearly:**

1. *Is the system currently stressed?*  
2. *Why did stress increase or decrease?*  
3. *Was there an early warning before stress emerged?*  

---

## 🧩 System Overview

The pipeline is intentionally modular and explainable:

```text
Synthetic Ops Data
        ↓
Signal Engineering (rolling stats, z-scores)
        ↓
Composite Stress Index
        ↓
Regime Labeling (stable / elevated / stressed)
        ↓
Early-Warning Episode Detection
        ↓
Interactive Dashboard + PDF Risk Memo
```

---

## 📊 Core Concepts

### 1. Composite Stress Index
A rule-based index combining standardized operational signals such as:
- Turnaround Time (TAT) volatility
- Queue velocity
- Utilization pressure  

This compresses multiple KPIs into **one interpretable measure of operational strain**.

---

### 2. Regime Labeling
Each day is classified into one of three regimes:
- **Stable**
- **Elevated**
- **Stressed**

This enables **regime-aware monitoring** rather than static threshold alerts.

---

### 3. Early-Warning Episodes
The system detects **warning signals prior to stress regimes** and evaluates:
- Detection rate
- Lead time (days before stress onset)

This allows **retrospective validation** of whether warning signals were actually useful, not just noisy indicators.

---

### 4. Decision-Grade PDF Memos
The dashboard exports a **one-page operational risk memo** containing:
- Current regime & KPIs
- **Last 7-day operational drivers** (vs previous 7 days)
- Plain-English interpretation
- Embedded stress/regime timeline

This mirrors how operational and risk updates are consumed in real organizations.

---

## 🖥️ Dashboard Features

- Center-level selection (e.g. Delhi, Mumbai, Bengaluru)
- KPI cards:
  - Regime
  - Stress Index
  - Avg TAT
  - Queue Size
  - Utilization
- Stress & regime monitoring charts
- Early-warning episode tables
- Raw signal inspection
- One-click memo & PDF export

---

## 📁 Project Structure

```text
visaops-risk-intel/
├── app/
│   └── explorer.py          # Streamlit dashboard
├── src/
│   ├── signals.py           # Signal engineering
│   ├── stress_index.py      # Stress computation & regimes
│   ├── early_warning.py     # Lead-time detection
│   ├── episode_analysis.py  # Episode summaries
│   ├── plot_stress.py       # Visualization utilities
│   └── report_generator.py  # PDF memo generation
├── data/
│   └── processed/           # Synthetic outputs
├── reports/
│   ├── memo_*.md
│   └── visaops_report_*.pdf
├── requirements.txt
└── README.md
```
---

## 🚀 Run Locally

```bash
pip install -r requirements.txt
streamlit run app/explorer.py
```

---

## 🔬 Research & Extension Potential

This system is intentionally designed to be **research-extendable**.

Potential extensions include:
- Application to **clinical operations**, labs, or hospitals
- Statistical validation of stress thresholds
- Causal modeling of driver signals
- Cross-center contagion effects
- Forecasting stress regimes

---

## 👤 Intended Audience

- Operations Analytics
- Risk & Strategy teams
- Public sector service delivery
- Research & methods groups
- Hiring managers evaluating **end-to-end analytical thinking**

---

## 📌 Key Takeaway

This project is **not a dashboard of metrics**.

It is a **decision-support system** that:
- Compresses operational complexity into interpretable signals
- Explains *why* conditions change
- Evaluates whether warnings arrive early enough to matter

