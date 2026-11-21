# CityNet Customer Churn Lab

This lab trains and evaluates models that estimate whether a customer will churn. The business target is a weekly list of the 100 customers with the highest predicted risk so the retention team can contact them first.

## Repository and branch

This CityNet project is maintained on the `lab/citynet-churn` branch. It can be opened independently from this folder.

```text
citynet-churn/
├── data/
│   ├── citynet_churn.csv       # 5,000 customer records
│   └── new_customers.csv       # 8 customers for batch prediction
├── src/
│   ├── common.py               # shared columns and train/validation/test split
│   ├── lab1_inspect.py         # dataset inspection
│   ├── lab2_split.py           # verify stratified splitting
│   ├── lab3_pipeline.py        # preprocessing pipeline
│   ├── lab4_models.py          # baseline and classifier comparison
│   ├── lab4b_svm.py            # linear SVM experiment
│   ├── lab5_evaluate.py        # validation PR-AUC and top-100 evaluation
│   ├── lab6_errors.py          # permutation importance and error analysis
│   ├── lab7_save.py            # save the fitted pipeline
│   ├── predict.py              # score and rank new customers
│   └── svm_toy.py              # small standalone SVM example
├── models/                     # generated joblib model; ignored by Git
├── reports/                    # generated prediction reports; ignored by Git
├── DATA.md
├── requirements.txt
└── README.md
```

## Dataset summary

- Training data: 5,000 rows and 14 columns.
- Prediction data: 8 rows and 12 columns.
- Target: `churned`, where 1 means the customer cancelled.
- Observed class split: 4,104 retained customers (82.08%) and 896 churned customers (17.92%).
- Missing values:
  - `payment_method`: 149
  - `age`: 411
- `cancel_request_logged` is a target-adjacent leakage column and must not be used as a normal feature.

See [DATA.md](DATA.md) for the data card.

## Environment setup

From the repository root:

```powershell
conda activate psebenv
cd E:\PSEB-AI\citynet-churn
python -m pip install -r requirements.txt
```

Run scripts from `citynet-churn/`, not from `src/`, because imports and data paths are written relative to this folder.

## Lab sequence

| Lab | Purpose | Current status |
|---|---|---|
| `svm_toy.py` | Demonstrates support vectors and linear SVM predictions on six small examples | Ready to run |
| `lab1_inspect.py` | Describes shape, types, missing values, churn rate, and suspicious relationships | Ready to run |
| `lab2_split.py` | Checks the 60/20/20 stratified train, validation, and test split | Needs `stratify=y` in `common.py` |
| `lab3_pipeline.py` | Builds numeric and categorical preprocessing | Needs imputation and encoding choices |
| `lab4_models.py` | Compares dummy, logistic-regression, and random-forest candidates | Needs dummy strategy and completed preprocessing |
| `lab4b_svm.py` | Compares scaled and unscaled linear SVM pipelines | Needs kernel, fit, top-100, and completed preprocessing |
| `lab5_evaluate.py` | Calculates validation PR-AUC, confusion matrix, classification report, and top-100 hits | Needs `fit` and target/probability arguments |
| `lab6_errors.py` | Measures permutation importance and analyses errors by region and behaviour | Requires completed `lab5_evaluate.py` behavior |
| `lab7_save.py` | Fills and saves the fitted pipeline | Needs `joblib.dump()` |
| `predict.py` | Loads a model and creates ranked predictions for new customers | Needs model loading and `predict_proba()` |

The intentional `____` placeholders are exercise points and must be resolved before the related script can complete.

## Useful commands

The currently runnable standalone SVM example:

```powershell
python src/svm_toy.py
```

The inspection exercise:

```powershell
python src/lab1_inspect.py
```

After completing the fill-in exercises:

```powershell
python src/lab2_split.py
python src/lab3_pipeline.py
python src/lab4_models.py
python src/lab4b_svm.py
python src/lab5_evaluate.py
python src/lab6_errors.py
python src/lab7_save.py
python src/predict.py data/new_customers.csv
```

The prediction command writes `reports/predictions.csv`.

## Completed and remaining work

### Current

- Dataset and package scaffold are organized.
- Shared feature lists and split structure are present.
- Runnable SVM toy and data-inspection exercises are available.
- Laboratory modules are divided by purpose.
- Generated model/report paths are excluded by `.gitignore`.

### Remaining

- Complete the intended split, preprocessing, model, evaluation, save, and prediction placeholders.
- Document validation PR-AUC, recall, precision, and top-100 churners.
- Check whether class weighting and threshold choices meet the retention objective.
- Run each script and record outputs.
- Compare validation and test results only after model selection is complete.
- Add automated tests for the shared split and preprocessing pipeline.

## Validation and test policy

The test set should remain untouched until the model and threshold are selected using the training and validation data. It should be used once for a final, recorded estimate of performance.

## Intended use

The model is for prioritizing retention outreach, such as a weekly call list of 100 customers.

## Not for

- Automatically cancelling or suspending a customer.
- Making decisions without human review.
- Treating a probability as proof that a customer will leave.
- Using `cancel_request_logged` as a normal predictor.

## Assumptions and limitations

- The CSV is course-made sample data and may not represent real CityNet operations.
- The data is imbalanced: only about 18% of records are churned.
- Missing numeric and categorical values require preprocessing.
- Historical data may contain bias from prior retention actions.
- Aggregated performance may hide differences between regions or plans.
- A production system needs monitoring, retraining, schema checks, and privacy controls.
