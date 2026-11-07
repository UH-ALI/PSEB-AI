import pandas as pd
from pipeline import clean


def test_clean():

    # Create a small messy dataset
    data = pd.DataFrame({
        "name": ["Ali", "Sara", "Omar", "Omar"],
        "city": ["karachi", "LAHORE", "KARACHI", "KARACHI"],
        "age": ["21", "22", "twenty", "twenty"],
        "score": [80, None, 92, 92]
    })

    # Run cleaning function
    result = clean(data)

    # Check that missing values are removed
    assert result["name"].isna().sum() == 0

    # Check that duplicate records are removed
    assert result.duplicated().sum() == 0

    # Check that age is numeric
    assert pd.api.types.is_numeric_dtype(result["age"])

    # Check city capitalization
    assert all(city == city.title() for city in result["city"])

    # Check that scores have no missing values
    assert result["score"].isna().sum() == 0

