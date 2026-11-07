import pandas as pd


def load(filepath="students_messy.csv"):
    """Load the original student dataset."""
    df = pd.read_csv(filepath)
    return df

def clean(df):
    """Clean the student dataset."""

    # Standardize city names
    df["city"] = df["city"].str.strip().str.title()

    # Replace invalid age values
    df["age"] = df["age"].replace("twenty", "20")

    # Convert age and score to numeric values
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["score"] = pd.to_numeric(df["score"], errors="coerce")

    # Remove rows where student name is missing
    df = df.dropna(subset=["name"])

    # Fill missing scores with median
    df["score"] = df["score"].fillna(df["score"].median())

    # Remove duplicate records
    df = df.drop_duplicates()

    # Reset row numbering
    df = df.reset_index(drop=True)

    return df

def add_features(df):
    """Add useful features to the dataset."""

    # Categorize student performance
    df["performance"] = pd.cut(
        df["score"],
        bins=[-1, 49, 69, 100],
        labels=["Needs Improvement", "Average", "Good"]
    )

    # Identify students who passed
    df["passed"] = df["score"] >= 50

    return df



if __name__ == "__main__": 

    # Step 1: Load data
    data = load()

    # Step 2: Clean data
    cleaned_data = clean(data)

    # Step 3: Add new features
    final_data = add_features(cleaned_data)

    # Step 4: Save processed data
    final_data.to_csv("students_clean.csv", index=False)

    print("Pipeline executed successfully!")
    print(final_data)

