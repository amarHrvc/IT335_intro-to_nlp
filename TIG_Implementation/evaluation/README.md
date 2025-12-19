# Parser Evaluator - Milestone 4

## Overview

This script evaluates how well our query parser extracts information from natural language travel queries.

## What It Does

1. **Loads** 50 sample queries from validation dataset
2. **Parses** each query using our QueryParser
3. **Compares** parsed results with ground truth (correct answers)
4. **Calculates** accuracy for each field (destination, duration, budget, people)
5. **Saves** detailed results to 3 files in `results/` folder

## Files

- `evaluate_parser.py` - Main evaluation script
- `results/` - Folder where results are saved (created automatically)

## How to Run

### Option 1: Using WSL (Linux Virtual Environment)

```bash
# Navigate to evaluation folder
cd TIG_Implementation/evaluation

# Activate Linux virtual environment
source ../../linux-venv/bin/activate

# Run evaluation
python evaluate_parser.py
```

### Option 2: Using Windows Python (if you have dependencies installed)

```cmd
# Navigate to evaluation folder
cd TIG_Implementation\evaluation

# Run evaluation
python evaluate_parser.py
```

## Requirements

**Python packages:**
- pandas (to read CSV files)
- spacy (NLP library used by parser)

**Dataset:**
- `TravelPlanner_cleaned/validation_cleaned.csv` (preferred - already preprocessed!)
- OR `TravelPlanner/validation.csv` (script will fallback to this)

If you get import errors, install with:
```bash
pip install pandas spacy
python -m spacy download en_core_web_sm
```

## Output Files

After running, check the `results/` folder for 3 files:

1. **`parser_results_TIMESTAMP.json`**
   - Complete results in JSON format
   - Contains all parsed data and correctness checks
   - Use for further processing

2. **`parser_summary_TIMESTAMP.txt`**
   - Human-readable summary
   - Shows accuracy percentages
   - Quick overview of performance

3. **`parser_comparison_TIMESTAMP.txt`**
   - Detailed side-by-side comparison
   - First 20 queries shown
   - Ground truth vs parsed results
   - Which fields are correct/incorrect

## Understanding the Code

The script is heavily commented. Key sections:

### Main Function
```python
def main():
    evaluator = ParserEvaluator(sample_size=50)
    evaluator.run_evaluation()
```

### Evaluation Steps
1. **Load data** - `load_validation_data()`
2. **Evaluate each query** - `evaluate_single_query()`
3. **Check fields** - `check_destination()`, `check_duration()`, etc.
4. **Display results** - `display_results()`
5. **Save to files** - `save_results()`

## Modifying for Planner Evaluation

To create `evaluate_planner.py` (next task), copy this file and:

1. Import `ItineraryPlanner` instead of `QueryParser`
2. Change evaluation logic:
   - Instead of checking fields, check if itinerary is valid
   - Check if it has correct number of days
   - Check if budget is respected
   - Check if dates are valid
3. Update result fields
4. Keep the same file saving structure

## Troubleshooting

**Problem:** `FileNotFoundError: Could not find validation_cleaned.csv`
- **Solution:** Make sure you run from `evaluation/` folder
- **Solution:** Check that `TravelPlanner_cleaned/` folder exists 2 levels up
- **Note:** Script will automatically fallback to `TravelPlanner/validation.csv` if cleaned version not found

**Problem:** `ModuleNotFoundError: No module named 'pandas'`
- **Solution:** Install pandas: `pip install pandas`

**Problem:** `ModuleNotFoundError: No module named 'spacy'`
- **Solution:** Install spacy: `pip install spacy`
- **Solution:** Download model: `python -m spacy download en_core_web_sm`

**Problem:** Script crashes or hangs
- **Solution:** Try reducing sample_size: `ParserEvaluator(sample_size=10)`
- **Solution:** Check if parser code works: `python ../agents/query_parser.py`

## Sample Output

```
============================================================
               PARSER EVALUATION - MILESTONE 4
============================================================

[STEP 1/5] Loading validation data...
Found dataset at: ../../TravelPlanner/validation.csv
Total queries in dataset: 180
Sampled 50 random queries for evaluation
✓ Loaded 50 validation queries

[STEP 2/5] Evaluating queries...
----------------------------------------------------------------
Processing query 1/50...
Processing query 10/50...
...
✓ Evaluated all 50 queries

[STEP 3/5] Calculating accuracy metrics...
✓ Metrics calculated

[STEP 4/5] Displaying results...

======================================================================
                         EVALUATION RESULTS
======================================================================

Total Queries Evaluated: 50

----------------------------------------------------------------------
ACCURACY BY FIELD:
----------------------------------------------------------------------
  Destination:  78.0%  (39/50 correct)
  Duration:     92.0%  (46/50 correct)
  Budget:       64.0%  (32/50 correct)
  People Count: 88.0%  (44/50 correct)
----------------------------------------------------------------------
  OVERALL:      80.5%
----------------------------------------------------------------------
```

## Questions?

If you have questions about the code:
1. Read the comments - each function is explained
2. Try modifying `sample_size` to test with fewer queries
3. Check output files to understand the results
4. Ask for help if stuck!

Good luck with your evaluation! 🚀
