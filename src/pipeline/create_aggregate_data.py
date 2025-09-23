
"""
Script to merge quarterly data into a joint dataset and apply additional cleaning.
"""

import pandas as pd
import numpy as np
import os


def load_quarterly_data(processed_data_path):
    """Load all quarterly processed data files"""
    data_files = [f for f in os.listdir(processed_data_path) if f.startswith("listings_quarter")]
    data_files.sort()
    
    if not data_files:
        raise ValueError("No processed data files found. Run clean_data.py first.")
    
    quarterly_data = {}
    for i, fname in enumerate(data_files):
        input_file = os.path.join(processed_data_path, fname)
        print(f"Loading quarter {i+1} from {input_file}")
        
        df = pd.read_csv(input_file)
        df['quarter'] = f"Q{i+1}"
        
        quarterly_data[i+1] = df
    
    return quarterly_data

def merge_quarterly_data(quarterly_data):
    """Merge all quarterly data into a single DataFrame"""
    all_data = pd.concat(quarterly_data.values(), ignore_index=True)
    print(f"Merged {len(quarterly_data)} quarters, total {len(all_data)} listings")
    return all_data

def engineer_features(df):
    """
    Create meaningful features for analysis (of the merged data)
    """
    print("Engineering features...")
    
    #  Price-based features
    df['log_price'] = np.log(df['price'])  # For normalized distribution
    
    # Price categories
    df['price_category'] = pd.cut(df['price'], 
                                 bins=[50, 100, 150, 200, 500, 1000, np.inf],
                                 labels=['Budget', 'Moderate', 'Comfort', 
                                        'Expensive', 'Premium', 'Luxury'])
    
    # Availability features
    df['availability_rate'] = df['availability_365'] / 365
    df['is_highly_available'] = df['availability_365'] > 180  # Available > 6 months
    
    
    # Review activity features
    df['is_active_host'] = df['days_since_last_review'] < 180  # Reviewed in last 6 months
    df['review_frequency'] = df['number_of_reviews'] / (df['days_since_last_review'] + 1)
    
    # Seasonal/quarter features
    df['quarter_num'] = df['quarter'].str.replace('Q', '').astype(int)
    df['is_peak_season'] = df['quarter_num'].isin([2, 3])  # Q2, Q3 = summer/fall
    
    # Geographic features 
    # Calculate neighborhood statistics
    neighborhood_stats = df.groupby('neighbourhood').agg({
        'price': ['mean', 'median', 'count']
    }).round(2)
    neighborhood_stats.columns = ['neighborhood_avg_price', 'neighborhood_median_price', 'neighborhood_count']
    df = df.merge(neighborhood_stats, on='neighbourhood', how='left')
    
    # Price premium relative to neighborhood
    df['price_premium_pct'] = ((df['price'] - df['neighborhood_avg_price']) / df['neighborhood_avg_price']) * 100
    
    # 7. Room type features
    room_type_dummies = pd.get_dummies(df['room_type'], prefix='room_type')
    df = pd.concat([df, room_type_dummies], axis=1)
    
    return df


def clean_joint_dataset(df):
    """
    Apply additional cleaning specific to the joint dataset
    Drop listings that don't appear in every quarter/date

    Takes in the merged data
    """
    print("Cleaning joint dataset...")
    
    # Get the unique quarters/dates in the dataset
    unique_quarters = df['quarter'].unique()
    
    # Count how many quarters each listing appears in
    listing_quarter_count = df.groupby('id')['quarter'].nunique()
    
    # Find listings that appear in ALL quarters
    listings_in_all_quarters = listing_quarter_count[listing_quarter_count == len(unique_quarters)].index
    
    # Filter the dataframe to only include listings that appear in every quarter
    df = df[df['id'].isin(listings_in_all_quarters)]

    #transform it!
    df = engineer_features(df)
    return df

def main():
    # Paths
    current_path = os.getcwd()
    project_path = current_path.replace("/src/pipeline", "")
    processed_data_path = os.path.join(project_path, "data", "processed")
    output_file = os.path.join(processed_data_path, "boston_listings_joint.csv")
    
    print("Creating joint Boston listings dataset...")
    
    # Load quarterly data (returns a dictionary)
    quarterly_data_dict = load_quarterly_data(processed_data_path)
    
    # Merge into single DataFrame
    merged_df = merge_quarterly_data(quarterly_data_dict)
    
    # Clean and engineer features
    cleaned_df = clean_joint_dataset(merged_df)
    
    # Save the final dataset
    cleaned_df.to_csv(output_file, index=False)
    
    print(f"Saved joint dataset to: {output_file}")
    print(f"Final dataset shape: {cleaned_df.shape}")
    print("Done!")

if __name__ == "__main__":
    main()

    
