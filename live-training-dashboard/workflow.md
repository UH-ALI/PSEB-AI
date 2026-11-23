# Workflow Design — Project 5: Live Training Dashboard (City Hospital)

## 1. Clinical Objective
Build an interactive ML workstation for City Hospital that solves two problems:
1. **Model Reliability:** Diagnose underfitting (unscaled features) and overfitting (high capacity + weak L2 regularization) on live training/validation curves before clinical use.
2. **Patient Screening:** Use the tuned model and a sensitivity-first decision threshold to screen individual biopsy patients and prioritize high-risk ward cases.

## 2. Two-Stage System Architecture

```text
[Stage 1: Live Training & Curve Diagnostics]
  Hyperparameters (Architecture, LR, Alpha, Epochs, Scaler)
        │
        ▼
  StandardScaler (optional) ──► MLPClassifier (epoch-by-epoch partial_fit)
        │
        ▼
  Track Train/Val Log-Loss & Accuracy ──► Automated Health Diagnosis
        │                                  (Underfitting / Overfitting / Healthy)
        ▼
[Stage 2: Clinical Triage & Patient Screening]
  Tuned Model + Clinical Alert Cutoff (default 0.35 for high recall)
        ├──► Single Patient Biomarker Sliders ──► Risk Probability + Top Deviations
        └──► Validation Ward Cohort ──► Ranked High-Risk Triage Queue