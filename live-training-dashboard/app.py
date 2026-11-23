"""
Project 5: Live Training Dashboard (City Hospital)
Run: streamlit run app.py
"""
import matplotlib.pyplot as plt
import streamlit as st

from src.data import KEY_BIOMARKERS, get_sample_patients, load_hospital_dataset
from src.trainer import (
    TrainConfig,
    build_ward_triage_table,
    run_training,
    score_single_patient,
)

st.set_page_config(page_title="City Hospital — Live ML Dashboard", layout="wide")


@st.cache_resource
def cached_dataset():
    return load_hospital_dataset()


def plot_learning_curves(history):
    fig, (ax_loss, ax_acc) = plt.subplots(1, 2, figsize=(12, 4.2), dpi=130)

    ax_loss.plot(history["epoch"], history["train_loss"], label="Train Loss", color="#1f77b4", lw=2)
    ax_loss.plot(history["epoch"], history["val_loss"], label="Validation Loss", color="#d62728", lw=2.2)
    ax_loss.fill_between(
        history["epoch"],
        history["train_loss"],
        history["val_loss"],
        color="#d62728",
        alpha=0.08,
        label="Generalization Gap",
    )
    ax_loss.set_title("Cross-Entropy Loss Curve", fontweight="bold")
    ax_loss.set_xlabel("Epoch")
    ax_loss.set_ylabel("Log Loss (Lower is better)")
    ax_loss.grid(alpha=0.25)
    ax_loss.legend()

    ax_acc.plot(history["epoch"], history["train_acc"], label="Train Accuracy", color="#1f77b4", lw=2)
    ax_acc.plot(history["epoch"], history["val_acc"], label="Validation Accuracy", color="#2ca02c", lw=2.2)
    ax_acc.set_title("Classification Accuracy Curve", fontweight="bold")
    ax_acc.set_xlabel("Epoch")
    ax_acc.set_ylabel("Accuracy")
    ax_acc.set_ylim(0.55, 1.02)
    ax_acc.grid(alpha=0.25)
    ax_acc.legend(loc="lower right")

    fig.tight_layout()
    return fig


def main():
    dataset = cached_dataset()

    st.title("City Hospital — Live Training & Patient Screening Dashboard")
    st.caption(
        "Project 5: Diagnose and fix training curves in real time, then screen patients with the tuned clinical model."
    )

    # ---------------- SIDEBAR CONTROLS ----------------
    st.sidebar.header("1. Live Training Controls")
    preset = st.sidebar.radio(
        "Diagnostic Scenario",
        [
            "Broken: Overfitting (High LR & Weak L2)",
            "Broken: Unscaled Features (No Scaler)",
            "Fixed: Regularized & Scaled",
            "Custom Live Tuning",
        ],
        index=0,
    )

    presets = {
        "Broken: Overfitting (High LR & Weak L2)": ("(128, 64)", 0.02, 0.0001, 60, True),
        "Broken: Unscaled Features (No Scaler)": ("(32, 16)", 0.005, 0.1, 45, False),
        "Fixed: Regularized & Scaled": ("(32, 16)", 0.002, 1.5, 45, True),
        "Custom Live Tuning": ("(32, 16)", 0.003, 0.5, 45, True),
    }
    def_arch, def_lr, def_alpha, def_epochs, def_scaler = presets[preset]

    arch_options = {"(16,)": (16,), "(32, 16)": (32, 16), "(64, 32)": (64, 32), "(128, 64)": (128, 64)}
    arch_key = st.sidebar.selectbox(
        "Hidden Layer Architecture",
        list(arch_options.keys()),
        index=list(arch_options.keys()).index(def_arch),
    )
    lr = st.sidebar.select_slider(
        "Learning Rate",
        options=[0.0005, 0.001, 0.002, 0.003, 0.005, 0.01, 0.02, 0.05],
        value=def_lr,
    )
    alpha = st.sidebar.select_slider(
        "L2 Regularization (alpha)",
        options=[0.0001, 0.001, 0.01, 0.1, 0.5, 1.0, 1.5, 3.0, 5.0],
        value=def_alpha,
    )
    epochs = st.sidebar.slider("Training Epochs", min_value=15, max_value=80, value=def_epochs, step=5)
    use_scaler = st.sidebar.checkbox("Apply StandardScaler", value=def_scaler)

    st.sidebar.header("2. Clinical Decision Cutoff")
    threshold = st.sidebar.slider(
        "Malignancy Alert Threshold",
        min_value=0.10,
        max_value=0.80,
        value=0.35,
        step=0.05,
        help="Lower thresholds increase cancer sensitivity (recall) to avoid missed diagnoses.",
    )

    cfg = TrainConfig(
        hidden_layers=arch_options[arch_key],
        learning_rate=lr,
        alpha=alpha,
        epochs=epochs,
        use_scaler=use_scaler,
        threshold=threshold,
    )
    run = run_training(dataset, cfg)

    tab_curves, tab_screen = st.tabs(
        ["1. Live Training Curves & Diagnostics", "2. Patient Screening & Ward Triage"]
    )

    # ---------------- TAB 1: LIVE TRAINING CURVES ----------------
    with tab_curves:
        banner_fn = getattr(st, run.status_level)
        banner_fn(f"**{run.status_title}** — {run.status_detail}")

        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Validation Accuracy", f"{run.metrics['accuracy']:.1%}")
        m2.metric("Cancer Recall (Sensitivity)", f"{run.metrics['recall']:.1%}")
        m3.metric("Specificity", f"{run.metrics['specificity']:.1%}")
        m4.metric("PR-AUC", f"{run.metrics['pr_auc']:.3f}")
        m5.metric("Missed Malignancies (FN)", f"{run.metrics['missed_cancers']}")

        st.pyplot(plot_learning_curves(run.history))

        col_cm, col_notes = st.columns([1.2, 1.0])
        with col_cm:
            st.subheader(f"Validation Confusion Matrix (Cutoff = {threshold:.2f})")
            st.dataframe(run.confusion, use_container_width=True)
        with col_notes:
            st.subheader("Clinical Trade-off Summary")
            st.markdown(
                f"- **Alert Precision (PPV):** `{run.metrics['precision']:.1%}` of flagged patients are truly malignant.\n"
                f"- **Sensitivity vs. Cutoff:** At `{threshold:.2f}`, the model catches "
                f"`{run.metrics['recall']:.1%}` of malignancies with `{run.metrics['missed_cancers']}` false negatives."
            )

    # ---------------- TAB 2: SCREEN REAL PATIENTS ----------------
    with tab_screen:
        if run.status_level != "success":
            st.warning(
                "Current model curves are not healthy. Switch to **'Fixed: Regularized & Scaled'** "
                "in the sidebar before relying on patient predictions."
            )

        st.subheader("Individual Patient Biopsy Screening")
        samples = get_sample_patients(dataset)
        selected_label = st.selectbox("Load Validation Patient Profile", list(samples.keys()))
        patient = samples[selected_label].copy()

        st.caption("Adjust key fine-needle aspirate (FNA) cell nucleus measurements to simulate live lab inputs:")
        slider_cols = st.columns(4)
        for idx, feat in enumerate(KEY_BIOMARKERS):
            col = slider_cols[idx % 4]
            patient[feat] = col.slider(
                feat,
                min_value=float(dataset.X_train[feat].min()),
                max_value=float(dataset.X_train[feat].max()),
                value=float(patient[feat]),
            )

        prob, top_deviations = score_single_patient(dataset, run, patient)

        st.divider()
        res_left, res_right = st.columns([1, 1.8])
        with res_left:
            st.metric(
                "Predicted Malignancy Risk",
                f"{prob:.1%}",
                delta=f"Cutoff: {threshold:.0%}",
                delta_color="inverse",
            )
            if prob >= threshold:
                st.error(
                    "**HIGH RISK — TRIAGE ALERT**\n\n"
                    "Exceeds clinical alert cutoff. Refer immediately for oncology review and confirmatory biopsy."
                )
            else:
                st.success(
                    "**LOW RISK — ROUTINE**\n\n"
                    "Below clinical alert cutoff. Recommend standard follow-up schedule."
                )

        with res_right:
            st.markdown("**Top Biomarker Deviations vs. Healthy Baseline**")
            st.dataframe(top_deviations, use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("Ward Triage Queue (Top-10 Highest-Risk Validation Patients)")
        triage_df = build_ward_triage_table(dataset, run, threshold)
        st.dataframe(triage_df.head(10), use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()