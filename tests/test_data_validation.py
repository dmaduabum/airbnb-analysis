import pandas as pd
import pytest

from src.pipeline.clean_raw_data import clean_airbnb_data


@pytest.fixture
def sample_data():
    """Minimal sample dataset with one invalid row."""
    return pd.DataFrame({
        "id": [1, 2, 3],
        "price": [100, 150, -1],            # negative price -> invalid
        "minimum_nights": [1, 2, 0],        # 0 nights -> invalid
        "availability_365": [100, 200, 400], # >365 -> invalid
        "neighbourhood": ["A", "B", "C"],
        "room_type": ["Entire home", "Private room", "Shared room"],
        "license": [None, None, None],
        "neighbourhood_group": [None, None, None],
    })


def test_cleaned_data_has_correct_columns_and_removes_invalid_rows(sample_data):
    """Cleaned data should have correct schema and valid rows only."""
    cleaned = clean_airbnb_data(sample_data)

    # Essential columns exist
    expected_cols = ["id", "price", "minimum_nights", "availability_365", "neighbourhood", "room_type"]
    assert all(col in cleaned.columns for col in expected_cols)

    # Unwanted columns removed
    assert "license" not in cleaned.columns
    assert "neighbourhood_group" not in cleaned.columns

    # All rows satisfy validation rules
    assert (cleaned["price"] > 0).all()
    assert (cleaned["minimum_nights"].between(1, 365)).all()
    assert (cleaned["availability_365"].between(0, 365)).all()
