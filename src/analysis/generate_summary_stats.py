import pandas as pd
import os
from scipy import stats


def calculate_summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate summary statistics grouped by quarter (no file writing)."""
    return df.groupby("quarter").agg({
        "price": ["mean", "median", "std", "count"],
        "availability_365": ["mean", "median", "std"],
        "number_of_reviews": ["mean", "median", "std"]
    }).round(2)


def run_anova(df: pd.DataFrame) -> pd.DataFrame:
    """Run ANOVA on price across quarters (no file writing)."""
    price_by_quarter = [
        df[df["quarter"] == q]["price"].dropna() for q in df["quarter"].unique()
    ]
    f_stat, p_value = stats.f_oneway(*price_by_quarter)

    return pd.DataFrame({
        "test": ["ANOVA - Price across quarters"],
        "f_statistic": [f_stat],
        "p_value": [p_value],
        "significance": ["Significant" if p_value < 0.05 else "Not Significant"]
    })


def perform_statistical_analysis(df: pd.DataFrame, results_path: str):
    """Perform full statistical analysis and save outputs to disk."""
    os.makedirs(results_path, exist_ok=True)

    summary_stats = calculate_summary_stats(df)
    stats_results = run_anova(df)

    summary_stats.to_csv(os.path.join(results_path, "summary_statistics.csv"))
    stats_results.to_csv(os.path.join(results_path, "statistical_tests.csv"), index=False)

    return summary_stats, stats_results


def main():
    """Entry point for running statistical analysis as a script."""
    current_path = os.getcwd()
    project_path = current_path.replace(os.path.join("src", "analysis"), "")

    processed_data_path = os.path.join(project_path, "data", "processed")
    tables_results_path = os.path.join(project_path, "results", "tables")

    df = pd.read_csv(os.path.join(processed_data_path, "boston_listings_joint.csv"))

    print("Performing statistical analysis...")
    perform_statistical_analysis(df, tables_results_path)

    print("Statistical analysis complete!")
    print(f"Summary saved to: {os.path.join(tables_results_path, 'summary_statistics.csv')}")
    print(f"Stats test saved to: {os.path.join(tables_results_path, 'statistical_tests.csv')}")


if __name__ == "__main__":
    main()
