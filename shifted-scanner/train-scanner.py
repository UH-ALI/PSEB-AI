"""
Project 3: The Shifted Scanner (Post Office)
Demonstrates how spatial shift & noise augmentation fixes performance collapse
on misaligned post-office scanner inputs and saves learning curves to curves.png.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score


def shift_image(img_flat: np.ndarray, dx: int, dy: int, noise_std: float = 0.0, rng=None) -> np.ndarray:
    """Shift an 8x8 flattened digit image by (dx, dy) pixels without wrap-around."""
    rng = rng or np.random.default_rng(42)
    img = img_flat.reshape(8, 8)
    shifted = np.zeros_like(img)

    src_x0, src_x1 = max(0, -dx), min(8, 8 - dx)
    dst_x0, dst_x1 = max(0, dx), min(8, 8 + dx)
    src_y0, src_y1 = max(0, -dy), min(8, 8 - dy)
    dst_y0, dst_y1 = max(0, dy), min(8, 8 + dy)

    if src_x1 > src_x0 and src_y1 > src_y0:
        shifted[dst_y0:dst_y1, dst_x0:dst_x1] = img[src_y0:src_y1, src_x0:src_x1]

    if noise_std > 0:
        shifted = np.clip(shifted + rng.normal(0, noise_std, size=shifted.shape), 0, 16)

    return shifted.ravel()


def create_shifted_test_set(X: np.ndarray, seed: int = 42) -> np.ndarray:
    """Simulate real post-office scanner drift (1-2 px random shifts + light noise)."""
    rng = np.random.default_rng(seed)
    offsets = [-2, -1, 1, 2]
    X_shifted = np.zeros_like(X)
    for i, row in enumerate(X):
        dx = int(rng.choice(offsets))
        dy = int(rng.choice(offsets))
        X_shifted[i] = shift_image(row, dx, dy, noise_std=0.6, rng=rng)
    return X_shifted


def augment_training_data(X: np.ndarray, y: np.ndarray, seed: int = 42):
    """Expand training set with shifted & lightly noisy scanner variations."""
    rng = np.random.default_rng(seed)
    X_list, y_list = [X], [y]
    shift_pairs = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-2, 0), (2, 0), (0, -2), (0, 2)]

    for dx, dy in shift_pairs:
        aug = np.array([shift_image(row, dx, dy, noise_std=0.4, rng=rng) for row in X])
        X_list.append(aug)
        y_list.append(y)

    return np.vstack(X_list), np.concatenate(y_list)


def train_epoch_curves(X_tr, y_tr, X_val_c, y_val_c, X_test_s, y_test_s, epochs: int = 35, seed: int = 42):
    """Train an MLP epoch-by-epoch and record centered vs. shifted accuracy curves."""
    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_tr)
    X_val_s = scaler.transform(X_val_c)
    X_tst_s = scaler.transform(X_test_s)

    clf = MLPClassifier(hidden_layer_sizes=(128, 64), alpha=0.01, learning_rate_init=0.002, random_state=seed)
    classes = np.arange(10)
    rng = np.random.default_rng(seed)

    history = {"train": [], "val_centered": [], "test_shifted": []}
    for _ in range(epochs):
        idx = rng.permutation(len(X_tr_s))
        clf.partial_fit(X_tr_s[idx], y_tr[idx], classes=classes)
        history["train"].append(accuracy_score(y_tr, clf.predict(X_tr_s)))
        history["val_centered"].append(accuracy_score(y_val_c, clf.predict(X_val_s)))
        history["test_shifted"].append(accuracy_score(y_test_s, clf.predict(X_tst_s)))

    return history


def main():
    digits = load_digits()
    X, y = digits.data, digits.target

    # Split: 60% train, 20% centered validation, 20% shifted scanner test
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.40, stratify=y, random_state=42)
    X_val, X_test_raw, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, stratify=y_temp, random_state=42)
    X_test_shifted = create_shifted_test_set(X_test_raw, seed=42)

    print("1/2 Training Baseline Scanner Model (centered digits only)...")
    base_hist = train_epoch_curves(X_train, y_train, X_val, y_val, X_test_shifted, y_test, epochs=35)

    print("2/2 Training Augmented Scanner Model (shift + noise augmentation)...")
    X_train_aug, y_train_aug = augment_training_data(X_train, y_train, seed=42)
    aug_hist = train_epoch_curves(X_train_aug, y_train_aug, X_val, y_val, X_test_shifted, y_test, epochs=35)

    print("\n--- Final Evaluation (Epoch 35) ---")
    print(f"Baseline  -> Centered Val Acc: {base_hist['val_centered'][-1]:.3f} | Shifted Test Acc: {base_hist['test_shifted'][-1]:.3f}")
    print(f"Augmented -> Centered Val Acc: {aug_hist['val_centered'][-1]:.3f} | Shifted Test Acc: {aug_hist['test_shifted'][-1]:.3f}")
    gain = (aug_hist["test_shifted"][-1] - base_hist["test_shifted"][-1]) * 100
    print(f"Shifted Scanner Accuracy Gain: +{gain:.1f} percentage points")

    # Plot and save curves.png
    epochs = np.arange(1, 36)
    fig = plt.figure(figsize=(13, 5.5), dpi=150)
    gs = fig.add_gridspec(2, 3, width_ratios=[1.4, 1.4, 1.0], wspace=0.32, hspace=0.38)

    # Panel A: Baseline curves
    ax1 = fig.add_subplot(gs[:, 0])
    ax1.plot(epochs, base_hist["train"], label="Train (Centered)", color="#1f77b4", lw=2)
    ax1.plot(epochs, base_hist["val_centered"], label="Val (Centered)", color="#2ca02c", lw=2, ls="--")
    ax1.plot(epochs, base_hist["test_shifted"], label="Test (Shifted Scanner)", color="#d62728", lw=2.5)
    ax1.set_title("Baseline Model (No Augmentation)", fontweight="bold")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Accuracy")
    ax1.set_ylim(0.2, 1.03)
    ax1.grid(alpha=0.25)
    ax1.legend(loc="lower right", fontsize=8.5)

    # Panel B: Augmented curves
    ax2 = fig.add_subplot(gs[:, 1])
    ax2.plot(epochs, aug_hist["train"], label="Train (Augmented)", color="#1f77b4", lw=2)
    ax2.plot(epochs, aug_hist["val_centered"], label="Val (Centered)", color="#2ca02c", lw=2, ls="--")
    ax2.plot(epochs, aug_hist["test_shifted"], label="Test (Shifted Scanner)", color="#ff7f0e", lw=2.5)
    ax2.set_title("Augmented Model (Shift + Noise)", fontweight="bold")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Accuracy")
    ax2.set_ylim(0.2, 1.03)
    ax2.grid(alpha=0.25)
    ax2.legend(loc="lower right", fontsize=8.5)

    # Panel C: Visual example of centered vs shifted input
    ax_top = fig.add_subplot(gs[0, 2])
    ax_top.imshow(X_test_raw[0].reshape(8, 8), cmap="gray_r")
    ax_top.set_title(f"Original Centered (Label: {y_test[0]})", fontsize=9.5, fontweight="bold")
    ax_top.axis("off")

    ax_bot = fig.add_subplot(gs[1, 2])
    ax_bot.imshow(X_test_shifted[0].reshape(8, 8), cmap="gray_r")
    ax_bot.set_title(f"Shifted Scanner Input (Label: {y_test[0]})", fontsize=9.5, fontweight="bold", color="#d62728")
    ax_bot.axis("off")

    fig.suptitle("Project 3: Post Office Shifted Scanner — Learning Curves & Domain Shift Fix", fontsize=12.5, fontweight="bold", y=0.99)
    out_path = Path(__file__).resolve().parent / "curves.png"
    plt.savefig(out_path, bbox_inches="tight")
    print(f"Saved curves to: {out_path}")


if __name__ == "__main__":
    main()