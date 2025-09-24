import os
import pandas as pd
import pytest

from src.analysis.generate_summary_stats import (
    calculate_summary_stats,
    run_anova,
    perform_statistical_analysis,
)


@pytest.fixture #to use the dataset later
def sample_df():
    """Fixture: Small sample dataset with two quarters of data."""
    return pd.DataFrame({
        "quarter": ["2020Q1"] * 5 + ["2020Q2"] * 5,
        "price": [100, 120, 130, 110, 150, 200, 210, 190, 220, 205],
        "availability_365": [100, 150, 120, 130, 140, 200, 210, 190, 180, 205],
        "number_of_reviews": [5, 10, 7, 8, 6, 20, 22, 18, 25, 19],
    })


def test_calculate_summary_stats_structure(sample_df):
    """Check that summary stats contain expected metrics."""
    summary = calculate_summary_stats(sample_df)

    # Verify multi-index columns exist
    assert ("price", "mean") in summary.columns
    assert ("availability_365", "median") in summary.columns
    assert ("number_of_reviews", "std") in summary.columns

    # Should have 2 rows (one per quarter)
    assert summary.shape[0] == 2


def test_run_anova_outputs_valid_results(sample_df):
    """Ensure ANOVA test returns correct structure and valid p-value."""
    results = run_anova(sample_df)

    assert "p_value" in results.columns
    assert "f_statistic" in results.columns
    assert results.shape[0] == 1

    # p-value must be between 0 and 1
    p_val = results["p_value"].iloc[0]
    assert 0 <= p_val <= 1


def test_perform_analysis_creates_files(tmp_path, sample_df): #fake path from pytest
    """Full integration test: check CSV outputs are written."""
    results_dir = tmp_path

    summary_stats, stats_results = perform_statistical_analysis(sample_df, str(results_dir))

    # Files must exist
    summary_file = os.path.join(results_dir, "summary_statistics.csv")
    stats_file = os.path.join(results_dir, "statistical_tests.csv")

    assert os.path.exists(summary_file)
    assert os.path.exists(stats_file)

    # Validate summary file contents
    df_summary = pd.read_csv(summary_file, header=[0, 1])
    assert "price" in df_summary.columns.get_level_values(0)

    # Validate stats results contents
    df_stats = pd.read_csv(stats_file)
    assert "p_value" in df_stats.columns
