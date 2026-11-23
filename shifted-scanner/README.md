# Project 3: The Shifted Scanner (Post Office)

## Objectives
Post office parcel scanners frequently capture digits off-center (1–2 pixels) with sensor noise. This project demonstrates how spatial shift causes a standard classifier to collapse and fixes the failure mode using data augmentation.

## Files
- `workflow.md` — Paper-first pipeline design and hypothesis
- `train-scanner.py` — Baseline vs. augmented MLP training and evaluation script
- `curves.png` — Training/validation learning curves and shifted input comparison

## Setup & Run
```bash
pip install numpy matplotlib scikit-learn
python train-scanner.py