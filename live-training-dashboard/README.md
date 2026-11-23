# Project 5: Live Training Dashboard (City Hospital)

## Objectives
Build an interactive Streamlit dashboard for City Hospital that enables clinicians and ML engineers to:
1. Diagnose and fix training issues (unscaled inputs and overfitting) on live learning curves.
2. Tune the clinical decision threshold for high cancer sensitivity (recall) and screen real patients.

## Repository Structure

```text
live-dashboard/
├── README.md               # Objectives, setup, implementation, results, and limitations
├── workflow.md             # Paper-first two-stage system design
├── requirements.txt        # Python dependencies
├── app.py                  # Streamlit dashboard entry point
├── src/
│   ├── __init__.py
│   ├── data.py             # Clinical dataset loading, splitting & patient profiles
│   └── trainer.py          # Epoch-by-epoch MLP training, curve diagnostics & risk scoring
└── screenshots/            # Dashboard implementation & result screenshots