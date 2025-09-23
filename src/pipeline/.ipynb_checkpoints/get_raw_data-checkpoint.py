import requests
import os
from datetime import datetime
from typing import Optional

BASE_URL = "https://data.insideairbnb.com/united-states/ma/boston/"

def download_file(url: str, save_path: str):
    """
    Downloads a file from a URL to a specified path.

    Args:
        url (str): The URL of the file to download.
        save_path (str): The local path to save the downloaded file.
    """
 
    try:
        print(f"Attempting to download {url}...")
        resp = requests.get(url)
        resp.raise_for_status()

        with open(save_path, "wb") as f:
            f.write(resp.content)
        print(f"Successfully downloaded to {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}. Error: {e}")
        

#dates could change depending...
def main(dates = ["2024-09-18", "2024-12-20", "2025-03-15", "2025-06-19"]):
    """
    Downloads historical and current employment data files from the BLS website.
    """
    # Define the directory for saving files
    current_path = os.getcwd()# Get the current working directory
    project_path = current_path.replace('/src/pipeline', '')
    raw_data_dir = project_path + '/data/raw'
    
    # Download data
    print("--- Downloading Airbnb data ---")
    for date in dates:
        url = f"{BASE_URL}{date}/visualisations/listings.csv"
        filename = f"listings_{date}.csv"
        save_path = os.path.join(raw_data_dir, filename)

        try:
            download_file(url, save_path)
        except requests.exceptions.RequestException as e:
            # Handle cases where the file for a specific year is not available
            print(f"Warning: File for date {date} was not found or could not be downloaded. Continuing to next date.")

if __name__ == "__main__":
    main()