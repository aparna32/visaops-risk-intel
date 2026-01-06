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
