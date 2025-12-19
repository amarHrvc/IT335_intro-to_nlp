# Parser Evaluator - Complete Instructions

## 📋 What You Have

I've created a **simplified, well-commented** parser evaluator for Milestone 4.

### Files Created:
1. **`evaluate_parser.py`** - Main evaluation script (heavily commented)
2. **`test_simple.py`** - Test script to verify setup
3. **`README.md`** - Detailed documentation
4. **`INSTRUCTIONS.md`** - This file (step-by-step guide)

## 🎯 Goal

Evaluate how accurately your query parser extracts:
- Destination city
- Trip duration (days)
- Budget amount
- Number of people

## 📝 Step-by-Step Instructions

### Step 1: Test Your Setup

Run the test script first to check if everything is ready:

```bash
# Navigate to evaluation folder
cd TIG_Implementation/evaluation

# Run test
python test_simple.py
```

**What it checks:**
- ✓ Python version (need 3.6+)
- ✓ Pandas library installed
- ✓ validation.csv file exists
- ✓ QueryParser can be imported
- ✓ Results folder exists

**If any test fails:** Follow the instructions printed by the test script.

### Step 2: Run the Evaluation

Once all tests pass, run the main evaluation:

```bash
python evaluate_parser.py
```

**What it does:**
1. Loads 50 random queries from validation dataset
2. Parses each query using your QueryParser
3. Compares with ground truth
4. Calculates accuracy for each field
5. Saves 3 result files

**Expected runtime:** 1-2 minutes

### Step 3: Check the Results

Look in the `results/` folder for 3 files:

1. **`parser_results_TIMESTAMP.json`**
   - Complete data in JSON format
   - Use this for further analysis

2. **`parser_summary_TIMESTAMP.txt`**
   - Quick summary with accuracy percentages
   - Example:
     ```
     Destination:  78.0% (39/50 correct)
     Duration:     92.0% (46/50 correct)
     Budget:       64.0% (32/50 correct)
     People Count: 88.0% (44/50 correct)
     OVERALL:      80.5%
     ```

3. **`parser_comparison_TIMESTAMP.txt`**
   - Detailed comparison of first 20 queries
   - Shows ground truth vs parsed result
   - Indicates which fields are correct/incorrect

## 🔍 Understanding the Code

The code is written to be **simple and educational**. Here's the structure:

### Main Class: `ParserEvaluator`

```python
class ParserEvaluator:
    def __init__(self, sample_size=50):
        # Initialize parser and create results folder
    
    def load_validation_data(self):
        # Load CSV file with validation queries
    
    def evaluate_single_query(self, query, ground_truth):
        # Parse one query and check if correct
    
    def check_destination(self, parsed, ground_truth):
        # Compare destination field
    
    def check_duration(self, parsed, ground_truth):
        # Compare duration field
    
    def check_budget(self, parsed, ground_truth):
        # Compare budget (allows 20% tolerance)
    
    def check_people(self, parsed, ground_truth):
        # Compare people count
    
    def run_evaluation(self):
        # Main function - runs all steps
    
    def display_results(self):
        # Print results to console
    
    def save_results(self):
        # Save 3 result files
```

### Key Concepts

**1. Loading Data:**
```python
df = pd.read_csv("validation.csv")  # Load CSV into DataFrame
df = df.sample(n=50)                # Pick 50 random rows
```

**2. Evaluating One Query:**
```python
parsed = self.parser.parse(query)        # Parse query
is_correct = parsed_dest == gt_dest      # Compare
self.destination_correct += 1            # Count if correct
```

**3. Calculating Accuracy:**
```python
accuracy = (correct_count / total_count) * 100
```

## 🛠️ Troubleshooting

### Problem: "FileNotFoundError: validation.csv"

**Solution:**
- Make sure you're in the `evaluation/` folder
- Check that `../../TravelPlanner/validation.csv` exists
- Try running `test_simple.py` to see which path works

### Problem: "ModuleNotFoundError: pandas"

**Solution:**
```bash
pip install pandas
```

### Problem: "Can't import QueryParser"

**Solution:**
- Check that `../agents/query_parser.py` exists
- Make sure you're in the right folder
- Try: `cd TIG_Implementation/evaluation`

### Problem: Script takes too long

**Solution:**
Reduce sample size in the code:
```python
evaluator = ParserEvaluator(sample_size=10)  # Instead of 50
```

## 📊 Using Results for Milestone 4

### For Tables (Phase 2, Task 2.1):

You can use the JSON file to create tables:

```python
import json
with open('results/parser_results_TIMESTAMP.json', 'r') as f:
    data = json.load(f)

# Table 1: Parser Performance
print("Field       | Accuracy | Correct | Total")
print("Destination |", data['metrics']['destination_accuracy'])
print("Duration    |", data['metrics']['duration_accuracy'])
# ... etc
```

### For Charts (Phase 2, Task 2.2):

Create bar charts from the accuracy data:
- X-axis: Field names (Destination, Duration, Budget, People)
- Y-axis: Accuracy percentage

### For Results Section (Phase 3, Task 3.1):

Use the summary file to write about:
1. **Setup:** "We evaluated parser on 50 validation queries..."
2. **Findings:** "Destination extraction achieved 78% accuracy..."
3. **Analysis:** "Duration was most accurate (92%) because..."
4. **Limitations:** "Budget was challenging (64%) due to..."

## 🎓 Learning from This Code

This script demonstrates several important concepts:

1. **File I/O:** Reading CSV, writing JSON and TXT
2. **Data Processing:** Using pandas DataFrames
3. **Evaluation Metrics:** Calculating accuracy
4. **Code Organization:** Classes and methods
5. **Error Handling:** Try/except blocks
6. **Documentation:** Comments explaining each part

**To create `evaluate_planner.py` next:**
1. Copy this file
2. Replace `QueryParser` with `ItineraryPlanner`
3. Change evaluation logic (check itinerary validity)
4. Keep the same structure for loading data and saving results

## ✅ Next Steps

1. ✅ Run `test_simple.py` to verify setup
2. ✅ Run `evaluate_parser.py` to generate results
3. ✅ Check the 3 result files in `results/` folder
4. ✅ Use results to create tables and charts (Task 2)
5. ✅ Copy/modify this script to create `evaluate_planner.py` (Task 1.2)

## 📞 Getting Help

If you encounter issues:

1. **Check the comments** in the code - they explain each step
2. **Run `test_simple.py`** - it will tell you what's wrong
3. **Read error messages** - they usually say what's missing
4. **Try with fewer samples** - Change `sample_size=50` to `sample_size=5`
5. **Check README.md** - Has more troubleshooting tips

## 🎉 Success Criteria

You'll know it worked when:
- ✅ Script runs without errors
- ✅ Console shows accuracy percentages
- ✅ 3 files appear in `results/` folder
- ✅ Summary file shows reasonable accuracies (>50%)
- ✅ Comparison file shows parsed vs ground truth

Good luck! The code is simple and well-commented - you can do this! 💪
