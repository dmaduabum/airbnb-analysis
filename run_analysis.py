"""
Main entry point for the Airbnb analysis pipeline.
Runs the complete analysis from raw data to final results.
"""

import os
import sys
from datetime import datetime
import pytest

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

from pipeline.get_raw_data import main as download_data
from pipeline.clean_raw_data import main as clean_data
from pipeline.create_aggregate_data import main as aggregate_data
from analysis.create_figures import main as create_figures
from analysis.generate_summary_stats import main as generate_stats


def main():
    """Run the complete analysis pipeline + tests"""
    print("Starting Airbnb analysis pipeline...")
    start_time = datetime.now()

    # Define key paths
    project_root = current_dir
    data_processed = os.path.join(project_root, "data", "processed")
    results_tables = os.path.join(project_root, "results", "tables")

    try:
        # Step 1: Download raw data
        print("Step 1/5: Downloading raw data...")
        download_data()

        # Step 2: Clean data
        print("Step 2/5: Cleaning data...")
        clean_data()

        # Step 3: Create aggregate dataset
        print("Step 3/5: Creating aggregate dataset...")
        aggregate_data()

        # Step 4: Generate figures
        print("Step 4/5: Creating figures...")
        create_figures()

        # Step 5: Generate summary statistics
        print("Step 5/5: Generating summary statistics...")
        generate_stats()


        end_time = datetime.now()
        duration = end_time - start_time

        print("Analysis completed successfully!")
        print(f"Total duration: {duration}")

        # Run tests after pipeline
        print("\nRunning test suite...")
        test_dir = os.path.join(project_root, "tests")
        # Run pytest programmatically
        pytest_args = [test_dir, "-v"]
        exit_code = pytest.main(pytest_args)
        if exit_code == 0:
            print("All tests passed!")
        else:
            print("Some tests failed. Check logs above.")

    except Exception as e:
        print(f"Pipeline failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
