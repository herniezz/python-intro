# MCDM Project: TOPSIS & SPOTIS Implementation

This project implements two Multi-Criteria Decision Making (MCDM) methods: TOPSIS (Technique for Order Preference by Similarity to an Ideal Solution) and SPOTIS (Stable Preference Ordering Towards Ideal Solution).

## Project Structure

```
.
├── data_loader.py      # Data loading and validation
├── normalization.py    # Data normalization methods
├── weights.py         # Weight calculation methods
├── topsis.py         # TOPSIS implementation
├── spotis.py         # SPOTIS implementation
├── pipeline.py       # Main execution script
├── docs/             # Documentation
│   └── README.md
└── tests/            # Test files
    └── test_methods.py
```

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Prepare your data in CSV format with alternatives as rows and criteria as columns.

2. Run the pipeline:
```bash
python pipeline.py
```

The script will:
- Load and validate your data
- Normalize the decision matrix
- Calculate criteria weights
- Apply both TOPSIS and SPOTIS methods
- Save results to `results.csv`

## Example Results

The output will be saved in `results.csv` with two columns:
- TOPSIS: Scores from the TOPSIS method
- SPOTIS: Scores from the SPOTIS method

Higher scores indicate better alternatives. The rankings can be interpreted as follows:
- Score close to 1: Alternative is close to the ideal solution
- Score close to 0: Alternative is far from the ideal solution

## Testing

Run the test suite:
```bash
pytest tests/
```

## Methods Overview

### TOPSIS
- Calculates distances to ideal and anti-ideal solutions
- Ranks alternatives based on relative closeness to ideal solution
- Considers both positive and negative ideal solutions

### SPOTIS
- Focuses on stability of preference ordering
- Uses weighted distances to ideal solution
- Provides more stable rankings in some cases

## Contributing

Feel free to submit issues and enhancement requests! 