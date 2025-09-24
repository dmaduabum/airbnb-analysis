# Platform Competition with Heterogeneous Hosts

## Overview
This repo contains background descriptive statistics and plots for the paper “Platform Competition with Heterogeneous Hosts.” The project focuses on Airbnb hosts in Boston, tracked by quarter. It’s distinctive because it uses individual-level supply data paired with aggregate demand data. Work is in progress.

## Project structure
```
airbnb-analysis/
├── data/
│   ├── raw/                 # Downloaded CSV files (immutable source)
│   └── processed/           # Cleaned data files
├── src/
│   ├── pipeline/
│   │   ├── get_raw_data.py          # Downloads raw Airbnb data
│   │   ├── clean_raw_data.py        # Cleans and validates data
│   │   └── create_aggregate_data.py # Builds joint/aggregate dataset
│   └── analysis/
│       ├── create_figures.py         # Exploratory visualizations
│       └── generate_summary_stats.py # Summary stats + statistical tests
├── results/
│   ├── figures/             # Generated plots
│   └── tables/              # Summary statistics & test results
├── tests/                   # Pytest-based tests (validation + analysis)
├── requirements.txt         # Python dependencies (pinned)
├── run_analysis.py          # One-command pipeline + test runner
└── README.md
```

## Installation & Setup
### 1. Clone the Repository

```bash
git clone https://github.com/dmaduabum/airbnb-analysis.git
cd airbnb-analysis
```
### 2. Create & Activate a Virtual Environment

```bash
python3 -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```
### 3. Install Dependencies

```bash
# Upgrade pip first
python3 -m pip install --upgrade pip

# Install all required packages from requirements.txt
pip install -r requirements.txt
```
## Usage
### One-Command Pipeline (includes tests)
```bash
python run_analysis.py
```
This will:

1. Download raw Airbnb data
2. Clean and validate the data
3. Create the aggregate / joint dataset
4. Generate figures
5. Produce summary statistics & statistical tests
6. Run the test suite (see “Testing” below)

## Next Steps
This is still a work in progress.
- Create and implement the model (based on BLP(1995) combined with nested logit)
- Expand to all US states listed in Inside Airbnb
- Further automate the data retrival process

