"""Clinical dataset loading, stratified splitting, and sample patient profiles."""
from dataclasses import dataclass
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split


KEY_BIOMARKERS = [
    "mean radius",
    "mean texture",
    "mean perimeter",
    "mean area",
    "mean smoothness",
    "mean concavity",
    "worst radius",
    "worst concave points",
]


@dataclass
class HospitalDataset:
    X_train: pd.DataFrame
    X_val: pd.DataFrame
    y_train: pd.Series
    y_val: pd.Series
    feature_names: list[str]
    benign_means: pd.Series
    benign_stds: pd.Series


def load_hospital_dataset(test_size: float = 0.25, seed: int = 42) -> HospitalDataset:
    """Load Wisconsin Diagnostic Breast Cancer dataset with 1 = Malignant, 0 = Benign."""
    raw = load_breast_cancer()
    X = pd.DataFrame(raw.data, columns=raw.feature_names)
    y = pd.Series(1 - raw.target, name="malignant")

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=seed
    )

    benign_train = X_train[y_train == 0]
    return HospitalDataset(
        X_train=X_train,
        X_val=X_val,
        y_train=y_train,
        y_val=y_val,
        feature_names=list(raw.feature_names),
        benign_means=benign_train.mean(),
        benign_stds=benign_train.std().replace(0, 1.0),
    )


def get_sample_patients(dataset: HospitalDataset) -> dict[str, pd.Series]:
    """Return representative validation patients for interactive screening."""
    malignant_df = dataset.X_val[dataset.y_val == 1]
    benign_df = dataset.X_val[dataset.y_val == 0]

    high_risk = malignant_df.sort_values("worst radius", ascending=False).iloc[1].copy()
    borderline = malignant_df.sort_values("mean radius", ascending=True).iloc[0].copy()
    routine = benign_df.sort_values("mean radius", ascending=True).iloc[5].copy()

    return {
        "Patient A — High-Risk Referral (Actual Malignant)": high_risk,
        "Patient B — Borderline Case (Actual Malignant)": borderline,
        "Patient C — Routine Checkup (Actual Benign)": routine,
    }

