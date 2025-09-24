import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np


def generate_exploratory_figures(df, results_path):
    """Generate exploratory analysis figures using engineered features"""
    
    # Set style for better visuals
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # 1. Price distribution by quarter (with log scale option)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Regular price
    sns.boxplot(data=df, x='quarter', y='price', ax=ax1)
    ax1.set_title('Price Distribution by Quarter')
    ax1.set_ylabel('Price ($)')
    
    # Log price for better visualization of distribution
    sns.boxplot(data=df, x='quarter', y='log_price', ax=ax2)
    ax2.set_title('Log Price Distribution by Quarter')
    ax2.set_ylabel('Log(Price)')
    
    plt.tight_layout()
    plt.savefig(os.path.join(results_path, 'price_distribution_by_quarter.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Price categories across quarters
    plt.figure(figsize=(12, 8))
    price_cat_counts = pd.crosstab(df['quarter'], df['price_category'], normalize='index') * 100
    price_cat_counts.plot(kind='bar', stacked=True, ax=plt.gca())
    plt.title('Price Category Distribution by Quarter')
    plt.ylabel('Percentage (%)')
    plt.xlabel('Quarter')
    plt.legend(title='Price Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(results_path, 'price_category_distribution.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Availability analysis
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Average availability by quarter
    availability_by_quarter = df.groupby('quarter')['availability_365'].mean()
    availability_by_quarter.plot(kind='bar', ax=ax1, color='skyblue')
    ax1.set_title('Average Availability by Quarter')
    ax1.set_ylabel('Average Availability (days)')
    ax1.set_xlabel('Quarter')
    
    # Highly available listings percentage
    highly_available_pct = df.groupby('quarter')['is_highly_available'].mean() * 100
    highly_available_pct.plot(kind='bar', ax=ax2, color='lightcoral')
    ax2.set_title('Percentage of Highly Available Listings (>180 days)')
    ax2.set_ylabel('Percentage (%)')
    ax2.set_xlabel('Quarter')
    
    plt.tight_layout()
    plt.savefig(os.path.join(results_path, 'availability_analysis.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Neighborhood analysis - Top 10 neighborhoods by listing count
    plt.figure(figsize=(12, 8))
    top_neighborhoods = df['neighbourhood'].value_counts().head(10)
    top_neighborhoods.plot(kind='barh', color='teal')
    plt.title('Top 10 Neighborhoods by Number of Listings')
    plt.xlabel('Number of Listings')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(os.path.join(results_path, 'top_neighborhoods.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Room type distribution across quarters
    plt.figure(figsize=(12, 8))
    room_type_pct = pd.crosstab(df['quarter'], df['room_type'], normalize='index') * 100
    room_type_pct.plot(kind='bar', stacked=True, ax=plt.gca())
    plt.title('Room Type Distribution by Quarter')
    plt.ylabel('Percentage (%)')
    plt.xlabel('Quarter')
    plt.legend(title='Room Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(results_path, 'room_type_distribution.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 6. Price premium analysis
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Price premium distribution
    df['price_premium_pct'].hist(bins=50, ax=ax1, alpha=0.7, color='orange')
    ax1.set_title('Distribution of Price Premium Relative to Neighborhood')
    ax1.set_xlabel('Price Premium (%)')
    ax1.set_ylabel('Frequency')
    ax1.axvline(0, color='red', linestyle='--', alpha=0.8)
    
    # Average price premium by quarter
    premium_by_quarter = df.groupby('quarter')['price_premium_pct'].mean()
    premium_by_quarter.plot(kind='bar', ax=ax2, color='gold')
    ax2.set_title('Average Price Premium by Quarter')
    ax2.set_ylabel('Average Price Premium (%)')
    ax2.set_xlabel('Quarter')
    ax2.axhline(0, color='red', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(os.path.join(results_path, 'price_premium_analysis.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 7. Peak season vs off-season comparison
    plt.figure(figsize=(10, 6))
    season_comparison = df.groupby('is_peak_season')['price'].agg(['mean', 'median', 'count'])
    season_comparison[['mean', 'median']].plot(kind='bar', ax=plt.gca())
    plt.title('Price Comparison: Peak Season vs Off-Season')
    plt.ylabel('Price ($)')
    plt.xlabel('Season')
    plt.xticks([0, 1], ['Off-Season', 'Peak Season'], rotation=0)
    plt.legend(['Mean Price', 'Median Price'])
    plt.tight_layout()
    plt.savefig(os.path.join(results_path, 'seasonal_pricing.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 8. Review activity analysis (using existing review columns)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Average reviews per month by quarter
    reviews_by_quarter = df.groupby('quarter')['reviews_per_month'].mean()
    reviews_by_quarter.plot(kind='bar', ax=ax1, color='green')
    ax1.set_title('Average Reviews per Month by Quarter')
    ax1.set_ylabel('Reviews per Month')
    ax1.set_xlabel('Quarter')
    
    # Number of reviews by quarter
    total_reviews_by_quarter = df.groupby('quarter')['number_of_reviews'].median()
    total_reviews_by_quarter.plot(kind='bar', ax=ax2, color='purple')
    ax2.set_title('Median Number of Reviews by Quarter')
    ax2.set_ylabel('Number of Reviews')
    ax2.set_xlabel('Quarter')
    
    plt.tight_layout()
    plt.savefig(os.path.join(results_path, 'review_activity_analysis.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 9. Enhanced correlation heatmap (focus on key engineered features)
    engineered_features = [
        'price', 'log_price', 'minimum_nights', 'availability_365', 'availability_rate',
        'number_of_reviews', 'reviews_per_month', 'calculated_host_listings_count',
        'neighborhood_avg_price', 'price_premium_pct', 'neighborhood_count'
    ]
    
    # Select only columns that exist in the dataframe
    existing_features = [col for col in engineered_features if col in df.columns]
    corr_matrix = df[existing_features].corr()
    
    plt.figure(figsize=(12, 10))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))  # Mask upper triangle
    sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm', center=0, 
                square=True, fmt='.2f', cbar_kws={"shrink": .8})
    plt.title('Correlation Matrix of Engineered Features')
    plt.tight_layout()
    plt.savefig(os.path.join(results_path, 'correlation_matrix_enhanced.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 10. Time trend of key metrics
    quarterly_metrics = df.groupby('quarter').agg({
        'price': 'median',
        'availability_365': 'mean',
        'number_of_reviews': 'median',
        'neighborhood_avg_price': 'mean'
    }).reset_index()
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()
    
    metrics = ['price', 'availability_365', 'number_of_reviews', 'neighborhood_avg_price']
    titles = ['Median Price', 'Average Availability', 'Median Reviews', 'Neighborhood Avg Price']
    colors = ['blue', 'green', 'red', 'purple']
    
    for i, (metric, title, color) in enumerate(zip(metrics, titles, colors)):
        axes[i].plot(range(len(quarterly_metrics)), quarterly_metrics[metric], 
                    marker='o', linewidth=2, markersize=8, color=color)
        axes[i].set_title(f'{title} Trend')
        axes[i].set_xlabel('Quarter')
        axes[i].set_ylabel(title)
        axes[i].set_xticks(range(len(quarterly_metrics)))
        axes[i].set_xticklabels(quarterly_metrics['quarter'])
        axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(results_path, 'time_trends.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 11. Room type pricing comparison
    plt.figure(figsize=(12, 8))
    room_type_pricing = df.groupby(['quarter', 'room_type'])['price'].median().unstack()
    room_type_pricing.plot(kind='bar', ax=plt.gca())
    plt.title('Median Price by Room Type and Quarter')
    plt.ylabel('Median Price ($)')
    plt.xlabel('Quarter')
    plt.legend(title='Room Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(results_path, 'room_type_pricing.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 12. Neighborhood price distribution (top 5 neighborhoods)
    plt.figure(figsize=(12, 8))
    top_5_neighborhoods = df['neighbourhood'].value_counts().head(5).index
    top_neighborhood_data = df[df['neighbourhood'].isin(top_5_neighborhoods)]
    
    sns.boxplot(data=top_neighborhood_data, x='neighbourhood', y='price')
    plt.title('Price Distribution in Top 5 Neighborhoods')
    plt.ylabel('Price ($)')
    plt.xlabel('Neighborhood')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(results_path, 'neighborhood_pricing.png'), dpi=300, bbox_inches='tight')
    plt.close()

def main():
    current_path = os.getcwd()
    project_path = current_path.replace("/src/analysis", "")
    processed_data_path = os.path.join(project_path, "data", "processed")
    figures_results_path = os.path.join(project_path, "results", "figures")
    
    # Create results directory if it doesn't exist
    os.makedirs(figures_results_path, exist_ok=True)
    
    print("Loading joint dataset...")
    df = pd.read_csv(os.path.join(processed_data_path, "boston_listings_joint.csv"))
    
    print("Generating exploratory figures...")
    generate_exploratory_figures(df, figures_results_path)
    
    print(f"Exploratory analysis complete! Figures saved to {figures_results_path}")

if __name__ == "__main__":
    main()