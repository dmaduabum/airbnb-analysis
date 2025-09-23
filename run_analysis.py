#!/usr/bin/env python3
"""
Main script to run the complete analysis pipeline.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from analysis.exploratory_analysis import main as exploratory_main
from analysis.statistical_analysis import main as statistical_main

def main():
    print("=== Running Complete Analysis ===")
    
    print("1. Running exploratory analysis...")
    exploratory_main()
    
    print("2. Running statistical analysis...")
    statistical_main()
    
    print("3. Generating final report...")
    # You can add report generation here
    
    print("=== Analysis Complete ===")
    print("Results saved to results/ directory")

if __name__ == "__main__":
    main()