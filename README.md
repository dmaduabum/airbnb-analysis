Installation & Setup
1. Clone the Repository

```bash
git clone https://github.com/dmaduabum/airbnb-analysis.git
cd airbnb-analysis
```
3. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```
3. Install Dependencies

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

Downloads raw Airbnb data from Inside Airbnb

Cleans and processes the data

Creates aggregated joint dataset

Generates exploratory figures and visualizations

Produces summary statistics and statistical tests

