# PSEB AI Coursework Repository

This repository contains Python practice work, coursework assignments, a student data pipeline, and the CityNet customer-churn laboratory exercises.

## Repository layout

```text
PSEB-AI/
├── citynet-churn/             # Customer-churn machine-learning lab
├── StudentDataPipeline/       # Assignment 03 data-cleaning pipeline
├── assignment_png/            # Assignment screenshots
├── assignment.ipynb           # Python assignment notebook
├── Student_manager.py         # Student class and top-scorer exercise
├── task01.py                  # GitHub API exercise
├── task03.py                  # Pytest exercise
├── p1.py / p2.py / p3.py      # Python and API practice scripts
├── hello.py                   # Introductory Python script
└── library.sql                # SQL practice
```

## Work completed so far

### Branch practice and tasks

- **StudentManager exercise:** defines a `Student` class, stores students in a list, prints students scoring above 50, and identifies the top scorer.
- **GitHub API exercises:** fetch public repository counts or profile information from the GitHub API and handle response status codes.
- **Pytest exercise:** implements `is_adult(age)` and tests ages below 18, equal to or above 18, and negative input.
- **General Python practice:** separate scripts cover basic data structures and API examples.

### Assignment 03 - Student Data Pipeline

The work in `StudentDataPipeline/` loads a messy CSV, standardizes text and numeric values, removes missing names and duplicate rows, creates performance and pass/fail features, and writes `students_clean.csv`.

Implemented in [pipeline.py](StudentDataPipeline/pipeline.py):

- `load(filepath)` - loads the source CSV.
- `clean(df)` - strips and title-cases city names, converts `"twenty"` to `"20"`, converts numeric columns, removes missing names and duplicates, fills missing scores with the median, and resets the index.
- `add_features(df)` - creates a three-level performance category and a passed boolean.

Run from `StudentDataPipeline/`:

```powershell
python pipeline.py
pytest test_pipe.py -v
```

The pipeline test checks missing-name removal, duplicate removal, numeric age, title-cased cities, and missing-score handling.

## Branch guide

| Branch | Contents | State |
|---|---|---|
| `main` | Root coursework, Assignment 03 student pipeline, notebooks, practice scripts, SQL, and screenshots | Stable shared coursework baseline |
| `lab/citynet-churn` | Everything in `main` plus the complete CityNet churn lab scaffold, datasets, scripts, and documentation | Active practice branch; lab exercises contain intentional fill-in placeholders |
| `origin/lab/citynet-churn` | Remote copy of the CityNet lab branch | Synchronised with the local `lab/citynet-churn` branch |

The CityNet work is intentionally kept on `lab/citynet-churn` so it does not mix with the general coursework on `main`.

## CityNet churn lab

See [citynet-churn/README.md](citynet-churn/README.md) for the full lab guide.

The current lab has:

- A 5,000-row training dataset and an 8-row prediction dataset.
- Separated inspection, splitting, preprocessing, model-comparison, evaluation, interpretation, and saving stages.
- Several intentional placeholders that are to be completed during the exercises.
- No final trained model or prediction report committed, as generated outputs are ignored.

## Python environment

A Conda environment or a `.venv` environment may be used. Conda is recommended for this course when both Python and scientific packages are needed.

Example:

```powershell
conda create -n psebenv python=3.12
conda activate psebenv
python -m pip install -r citynet-churn/requirements.txt
```

VS Code can attach to the environment through **Ctrl+Shift+P → Python: Select Interpreter**.

## Git workflow

Keep normal coursework on `main` and run the CityNet lab on its own branch:

```powershell
git switch main
git switch lab/citynet-churn
```

Merge or push only after the intended exercise files have been checked and the required test or run results are documented.
