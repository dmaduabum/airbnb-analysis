# Platform Competition with Heterogeneous Hosts

## Description
Background descriptive statistics and plots for the paper "Platform Competition with Heterogeneous Hosts" that aims to estimate equilibrium in a platform economy: housing. This is still a work in progress. The data set looks at the boston host per quarter. It making it unique in that it has indidiual level level supply side data but aggregate level demand data per quate.  

## project structure
```
airbnb-analysis/
├── data/
│   ├── raw/                 # Downloaded CSV files (immutable source)
│   └── processed/           # Cleaned data files
├── src/
│   ├── pipeline/
│   │   ├── get_raw_data.py          # Downloads raw Airbnb data
│   │   ├── clean_raw_data.py        # Cleans and processes data
│   │   └── create_aggregate_data.py # Creates joint dataset
│   └── analysis/
│       ├── create_figures.py         # Generates exploratory visualizations
│       └── generate_summary_stats.py # Produces statistical summaries
├── results/
│   ├── figures/             # Generated plots and charts
│   └── tables/              # Summary statistics and test results
├── tests/                   # Test files for data validation
├── docs/                    # Documentation files
├── requirements.txt         # Python dependencies
├── run_analysis.py          # Main pipeline execution script
└── README.md               # This file
```

## Installation & Setup
### 1. Clone the Repository

```bash
git clone https://github.com/dmaduabum/airbnb-analysis.git
cd airbnb-analysis
```
### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
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
### Run Complete Analysis Pipeline
```bash
python run_analysis.py
```
This single command executes the entire pipeline:

- Downloads raw Airbnb data from Inside Airbnb
- Cleans and processes the data
- Creates aggregated joint dataset
- Generates exploratory figures and visualizations
- Produces summary statistics and statistical tests

## Next Steps
This is still a work in progress.
- Create and implement the model (based on BLP(1995) combined with nested logit)
- Expand to all US states listed in Inside Airbnb
- Further automate the data retrival process

