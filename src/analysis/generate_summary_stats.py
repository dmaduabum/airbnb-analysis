import pandas as pd
import numpy as np
from scipy import stats
import os
from pathlib import Path

def perform_statistical_analysis(df, results_path):
    """Perform statistical tests and generate summary statistics"""
    # Summary statistics by quarter
    summary_stats = df.groupby('quarter').agg({
        'price': ['mean', 'median', 'std', 'count'],
        'availability_365': ['mean', 'median', 'std'],
        'number_of_reviews': ['mean', 'median', 'std']
    }).round(2)
    
    summary_stats.to_csv(results_path + '/summary_statistics.csv')
    
    # Price comparison between quarters (ANOVA)
    price_by_quarter = [df[df['quarter'] == q]['price'].dropna() for q in df['quarter'].unique()]
    f_stat, p_value = stats.f_oneway(*price_by_quarter)
    
    # Save statistical test results
    stats_results = pd.DataFrame({
        'test': ['ANOVA - Price across quarters'],
        'f_statistic': [f_stat],
        'p_value': [p_value],
        'significance': ['Significant' if p_value < 0.05 else 'Not Significant']
    })
    
    stats_results.to_csv(results_path + '/statistical_tests.csv', index=False)
    
    return summary_stats, stats_results

def main():
    current_path = os.getcwd()
    project_path = current_path.replace("/src/analysis", "")
    processed_data_path = os.path.join(project_path, "data", "processed")
    tables_results_path = os.path.join(project_path, "results", "tables")
    
    df = pd.read_csv(processed_data_path + "/boston_listings_joint.csv")
    
    print("Performing statistical analysis...")
    summary_stats, stats_results = perform_statistical_analysis(df, tables_results_path)
    
    print("Statistical analysis complete!")
    #print(f"ANOVA p-value for price differences: {stats_results['p_value'].iloc[0]:.4f}")

if __name__ == "__main__":
    main()