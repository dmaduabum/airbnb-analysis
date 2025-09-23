import pandas as pd
import os

def clean_airbnb_data(df):
    """
    Clean Airbnb dataset by removing invalid rows instead of capping values.

    Drops rows where:
      - price < 0
      - minimum_nights > 365
      - availability_365 > 365 or < 0

      --------
      Returns:
      df: cleaned data frame
    """
    df = df.copy()

    #drop uninformative columns
    df = df.drop(columns=['license', 'neighbourhood_group'])
    
    # Ensure correct dtypes
    df["id"] = pd.to_numeric(df["id"], errors="coerce").astype("Int64")
    df["host_id"] = pd.to_numeric(df["host_id"], errors="coerce").astype("Int64")
    df["last_review"] = pd.to_datetime(df["last_review"], errors="coerce")

    numeric_cols = [
        "latitude", "longitude", "price", "minimum_nights",
        "number_of_reviews", "reviews_per_month",
        "calculated_host_listings_count", "availability_365",
        "number_of_reviews_ltm"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # --- Drop weird data points ---
    df = df[df["price"] >= 0]                          # no negative prices
    df = df[df["minimum_nights"].between(1, 365)]      # reasonable stays only
    df = df[df["availability_365"].between(0, 365)]    # within a year
    return df

    
def main(dates = ["2024-09-18", "2024-12-20", "2025-03-15", "2025-06-19"]):
    # Paths
    current_path = os.getcwd()
    project_path = current_path.replace("/src/pipeline", "")
    raw_data_path = os.path.join(project_path, "data", "raw")
    processed_data_path = os.path.join(project_path, "data", "processed")

    # gets all files in the data/raw 
    raw_files = [f for f in os.listdir(raw_data_path) if f.startswith("listings")]
    raw_files.sort()
    
    
    for i, fname in enumerate(raw_files):
        input_file = os.path.join(raw_data_path, fname)
        output_file = os.path.join(processed_data_path, f"listings_quarter{i+1}")
    
        print(f"Loading {input_file} ...")
        df = pd.read_csv(input_file)
    
        print(f"Cleaning data from {fname} ...")
        df_clean = clean_airbnb_data(df)
        df_clean["date"] = dates[i]
        
        df_clean.to_csv(output_file, index=False)
        print(f"Saved cleaned file: {output_file}")

    print("Done!")


if __name__ == "__main__":
    main()