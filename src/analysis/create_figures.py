import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def generate_exploratory_figures(df, results_path):
    """Generate exploratory analysis figures"""
    
    # Price distribution by quarter
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=df, x='quarter', y='price')
    plt.title('Price Distribution by Quarter')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(results_path + 'price_distribution_by_quarter.png')
    plt.close()
    
    # Availability trends
    plt.figure(figsize=(12, 8))
    availability_by_quarter = df.groupby('quarter')['availability_365'].mean()
    availability_by_quarter.plot(kind='bar')
    plt.title('Average Availability by Quarter')
    plt.ylabel('Average Availability (days)')
    plt.tight_layout()
    plt.savefig(results_path + 'availability_by_quarter.png')
    plt.close()
    
    # Correlation heatmap (for numerical columns)
    numerical_cols = df.select_dtypes(include=['number']).columns
    corr_matrix = df[numerical_cols].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Matrix')
    plt.tight_layout()
    plt.savefig(results_path + 'correlation_matrix.png')
    plt.close()

def main():
    current_path = os.getcwd()
    project_path = current_path.replace("/src/analysis", "")
    processed_data_path = os.path.join(project_path, "data", "processed")
    figures_results_path = os.path.join(project_path, "results", "figures")
    
    df = pd.read_csv(processed_data_path + "boston_listings_joint.csv")
    
    print("Generating exploratory figures...")
    generate_exploratory_figures(df, figures_results_path)
    
    print("Exploratory analysis complete!")

if __name__ == "__main__":
    main()