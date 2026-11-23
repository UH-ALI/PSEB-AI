# Workflow Design — Project 3: The Shifted Scanner (Post Office)

## 1. Problem Statement
Optical parcel-sorting scanners at the post office suffer from mechanical belt drift. Incoming digit scans are frequently shifted by 1–2 pixels off-center and contain light sensor noise. A classifier trained exclusively on centered calibration digits fails when deployed on shifted production scans.

## 2. End-to-End Pipeline Design

```text
[Raw 8x8 Digit Scans]
        │
        ▼
[Stratified Split: 60% Train | 20% Centered Val | 20% Held-Out Test]
        │                                               │
        │                                               ▼
        │                                  [Simulate Scanner Drift]
        │                                  (±1 to ±2 px shift + noise)
        │                                               │
        ├───────────────────────────┐                   │
        ▼                           ▼                   │
[Baseline Train Set]     [Augmented Train Set]          │
 (Centered only)          (10x directional shifts       │
                           + mild Gaussian noise)       │
        │                           │                   │
        ▼                           ▼                   │
[StandardScaler + MLP]   [StandardScaler + MLP]         │
        │                           │                   │
        └─────────────┬─────────────┘                   │
                      ▼                                 │
        [Track Epoch-by-Epoch Learning Curves] ◄────────┘
                      │
                      ▼
            [Save curves.png]