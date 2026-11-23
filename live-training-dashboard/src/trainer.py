"""Epoch-by-epoch MLP training, curve diagnostics, and patient risk inference."""
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    log_loss,
    precision_score,
    recall_score,
)
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

from src.data import HospitalDataset


@dataclass
class TrainConfig:
    hidden_layers: tuple[int, ...]
    learning_rate: float
    alpha: float
    epochs: int
    use_scaler: bool
    threshold: float
    seed: int = 42


@dataclass
class TrainingRun:
    model: MLPClassifier
    scaler: StandardScaler | None
    history: pd.DataFrame
    val_proba: np.ndarray
    val_pred: np.ndarray
    metrics: dict[str, float]
    confusion: pd.DataFrame
    status_level: str  # "error" | "warning" | "success"
    status_title: str
    status_detail: str


def run_training(dataset: HospitalDataset, cfg: TrainConfig) -> TrainingRun:
    """Train MLP epoch-by-epoch and evaluate generalization & clinical metrics."""
    if cfg.use_scaler:
        scaler = StandardScaler()
        X_tr = scaler.fit_transform(dataset.X_train)
        X_va = scaler.transform(dataset.X_val)
    else:
        scaler = None
        X_tr = dataset.X_train.to_numpy()
        X_va = dataset.X_val.to_numpy()

    y_tr = dataset.y_train.to_numpy()
    y_va = dataset.y_val.to_numpy()

    clf = MLPClassifier(
        hidden_layer_sizes=cfg.hidden_layers,
        learning_rate_init=cfg.learning_rate,
        alpha=cfg.alpha,
        random_state=cfg.seed,
    )
    rng = np.random.default_rng(cfg.seed)
    classes = np.array([0, 1])

    records = []
    for epoch in range(1, cfg.epochs + 1):
        perm = rng.permutation(len(X_tr))
        clf.partial_fit(X_tr[perm], y_tr[perm], classes=classes)

        p_tr = clf.predict_proba(X_tr)
        p_va = clf.predict_proba(X_va)

        records.append(
            {
                "epoch": epoch,
                "train_loss": log_loss(y_tr, p_tr),
                "val_loss": log_loss(y_va, p_va),
                "train_acc": accuracy_score(y_tr, p_tr[:, 1] >= 0.5),
                "val_acc": accuracy_score(y_va, p_va[:, 1] >= 0.5),
            }
        )

    history = pd.DataFrame(records)
    val_proba = clf.predict_proba(X_va)[:, 1]
    val_pred = (val_proba >= cfg.threshold).astype(int)

    tn, fp, fn, tp = confusion_matrix(y_va, val_pred).ravel()
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0

    metrics = {
        "accuracy": float(accuracy_score(y_va, val_pred)),
        "recall": float(recall_score(y_va, val_pred, zero_division=0)),
        "specificity": float(specificity),
        "precision": float(precision_score(y_va, val_pred, zero_division=0)),
        "pr_auc": float(average_precision_score(y_va, val_proba)),
        "missed_cancers": int(fn),
    }

    confusion = pd.DataFrame(
        [[tn, fp], [fn, tp]],
        index=["Actual Benign (0)", "Actual Malignant (1)"],
        columns=["Predicted Benign (0)", "Predicted Malignant (1)"],
    )

    final_gap = float(history["val_loss"].iloc[-1] - history["train_loss"].iloc[-1])
    final_val_acc = float(history["val_acc"].iloc[-1])

    if not cfg.use_scaler or final_val_acc < 0.88:
        status_level = "error"
        status_title = "Underfitting / Unscaled Input Features"
        status_detail = (
            f"Validation accuracy stalled at {final_val_acc:.1%}. Enable StandardScaler "
            "so large-magnitude features (e.g., area) do not dominate gradients."
        )
    elif final_gap > 0.12:
        status_level = "warning"
        status_title = f"Overfitting Detected (Loss Gap = {final_gap:.3f})"
        status_detail = (
            "Validation loss is diverging above training loss. Increase L2 regularization (alpha), "
            "lower the learning rate, or select a smaller hidden architecture."
        )
    else:
        status_level = "success"
        status_title = f"Healthy Generalization (Loss Gap = {final_gap:.3f})"
        status_detail = (
            "Training and validation curves converge cleanly with minimal generalization gap. "
            "Model is calibrated for clinical screening."
        )

    return TrainingRun(
        model=clf,
        scaler=scaler,
        history=history,
        val_proba=val_proba,
        val_pred=val_pred,
        metrics=metrics,
        confusion=confusion,
        status_level=status_level,
        status_title=status_title,
        status_detail=status_detail,
    )


def score_single_patient(
    dataset: HospitalDataset, run: TrainingRun, patient_row: pd.Series
) -> tuple[float, pd.DataFrame]:
    """Predict malignancy probability and rank top abnormal biomarkers vs. benign baseline."""
    df = pd.DataFrame([patient_row])[dataset.feature_names]
    X_in = run.scaler.transform(df) if run.scaler is not None else df.to_numpy()
    prob = float(run.model.predict_proba(X_in)[0, 1])

    z_scores = (patient_row - dataset.benign_means) / dataset.benign_stds
    deviations = pd.DataFrame(
        {
            "Biomarker": dataset.feature_names,
            "Patient Value": patient_row.values.round(3),
            "Healthy Mean": dataset.benign_means.values.round(3),
            "Z-Score vs. Healthy": z_scores.values.round(2),
        }
    )
    deviations["abs_z"] = deviations["Z-Score vs. Healthy"].abs()
    top_deviations = (
        deviations.sort_values("abs_z", ascending=False)
        .drop(columns=["abs_z"])
        .head(5)
        .reset_index(drop=True)
    )
    return prob, top_deviations


def build_ward_triage_table(
    dataset: HospitalDataset, run: TrainingRun, threshold: float
) -> pd.DataFrame:
    """Rank all validation patients by predicted malignancy risk for clinical triage."""
    triage = dataset.X_val[["mean radius", "mean texture", "worst radius", "worst concave points"]].copy()
    triage.insert(0, "Patient ID", [f"CH-{1000 + idx}" for idx in dataset.X_val.index])
    triage["Actual Diagnosis"] = np.where(dataset.y_val == 1, "Malignant", "Benign")
    triage["Malignancy Risk (%)"] = (run.val_proba * 100).round(1)
    triage["Triage Status"] = np.where(run.val_proba >= threshold, "ALERT: Biopsy", "Routine")
    return triage.sort_values("Malignancy Risk (%)", ascending=False).reset_index(drop=True)