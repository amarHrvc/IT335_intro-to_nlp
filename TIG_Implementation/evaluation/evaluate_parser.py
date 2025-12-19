"""
Parser Evaluation Script - Milestone 4
Evaluates query parser accuracy on validation dataset

SIMPLIFIED VERSION FOR LEARNING

This script:
1. Loads validation data (50 sample queries)
2. Runs parser on each query
3. Compares parsed results with ground truth
4. Calculates accuracy for each field
5. Saves detailed results to files
"""

import sys
import os
import pandas as pd
import json
from datetime import datetime

# Add parent directory to Python path so we can import our parser
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import our query parser
from agents.query_parser import QueryParser

class ParserEvaluator:
    """
    Simple class to evaluate parser performance
    
    What it does:
    - Loads validation queries from CSV
    - Parses each query
    - Compares with ground truth
    - Counts correct/incorrect for each field
    - Saves results to files
    """
    
    def __init__(self, sample_size=50):
        """
        Initialize the evaluator
        
        Args:
            sample_size: How many queries to test (default: 50)
        """
        self.sample_size = sample_size
        
        # Create the parser (use_llm=False means rule-based, no API needed)
        print("Initializing parser...")
        self.parser = QueryParser(use_llm=False)
        
        # Dictionary to store results
        self.results = {
            'total': 0,                    # Total queries evaluated
            'destination_correct': 0,      # Count of correct destinations
            'duration_correct': 0,         # Count of correct durations
            'budget_correct': 0,           # Count of correct budgets
            'people_correct': 0,           # Count of correct people counts
            'details': []                  # List of detailed results per query
        }
        
        # Create results folder if it doesn't exist
        self.results_folder = os.path.join(current_dir, 'results')
        if not os.path.exists(self.results_folder):
            os.makedirs(self.results_folder)
            print(f"Created results folder: {self.results_folder}")
    
    def load_validation_data(self):
        """
        Load validation dataset from CSV file
        
        WHY USE CLEANED VERSION:
        - Data already preprocessed (normalized text, removed duplicates)
        - Consistent with training data processing
        - Better quality, no noise
        - No need to clean data in this script
        
        Returns:
            pandas DataFrame with validation queries
        """
        print("\n--- Loading Validation Data ---")
        
        # Try to find validation_cleaned.csv in different locations
        # Preference: cleaned > original (cleaned = already preprocessed!)
        possible_paths = [
            "../../TravelPlanner_cleaned/validation_cleaned.csv",  # BEST - preprocessed
            "../../TravelPlanner/validation.csv",                  # Fallback to original
            "../TravelPlanner_cleaned/validation_cleaned.csv",     # Alternative path
        ]
        
        df = None
        for path in possible_paths:
            full_path = os.path.join(current_dir, path)
            if os.path.exists(full_path):
                print(f"Found dataset at: {full_path}")
                df = pd.read_csv(full_path)
                break
        
        # If we couldn't find the file, stop
        if df is None:
            raise FileNotFoundError(
                "Could not find validation_cleaned.csv or validation.csv. "
                "Please make sure TravelPlanner_cleaned folder exists."
            )
        
        print(f"Total queries in dataset: {len(df)}")
        
        # If dataset is larger than sample_size, pick random sample
        if len(df) > self.sample_size:
            df = df.sample(n=self.sample_size, random_state=42)
            print(f"Sampled {self.sample_size} random queries for evaluation")
        
        return df
    
    def normalize_city(self, city):
        """
        Normalize city name for comparison
        
        Example: "New York" -> "new york", "San-Francisco" -> "san francisco"
        
        Args:
            city: City name string
            
        Returns:
            Normalized city name (lowercase, no hyphens)
        """
        if not city:
            return ""
        return str(city).strip().lower().replace("-", " ")
    
    def check_destination(self, parsed, ground_truth):
        """
        Check if destination city was extracted correctly
        
        Args:
            parsed: Dictionary from parser (our result)
            ground_truth: Dictionary from dataset (correct answer)
            
        Returns:
            True if correct, False if incorrect
        """
        # Get destination from parsed result
        parsed_dest = self.normalize_city(parsed.get('destination', ''))
        
        # Get destination from ground truth ('dest' column in CSV)
        gt_dest = self.normalize_city(ground_truth.get('dest', ''))
        
        # Check if they match (exact match or contains)
        is_correct = parsed_dest == gt_dest or gt_dest in parsed_dest
        
        return is_correct
    
    def check_duration(self, parsed, ground_truth):
        """
        Check if trip duration (days) was extracted correctly
        
        Args:
            parsed: Dictionary from parser
            ground_truth: Dictionary from dataset
            
        Returns:
            True if correct, False if incorrect
        """
        try:
            # Convert to integers for comparison
            parsed_days = int(parsed.get('duration', 0))
            gt_days = int(ground_truth.get('days', 0))
            
            # Must be exact match
            return parsed_days == gt_days
        except:
            # If conversion fails, it's incorrect
            return False
    
    def check_budget(self, parsed, ground_truth):
        """
        Check if budget was extracted correctly
        
        Note: We allow 20% tolerance because budget might be extracted
        differently (e.g., "$1,500" vs "1500")
        
        Args:
            parsed: Dictionary from parser
            ground_truth: Dictionary from dataset
            
        Returns:
            True if within 20% tolerance, False otherwise
        """
        try:
            # Convert to numbers
            parsed_budget = float(parsed.get('budget', 0))
            gt_budget = float(ground_truth.get('budget', 0))
            
            # If ground truth budget is 0, parsed must also be 0
            if gt_budget == 0:
                return parsed_budget == 0
            
            # Allow 20% tolerance (±20%)
            # Example: if GT is 1000, accept 800-1200
            tolerance = 0.20
            lower_bound = gt_budget * (1 - tolerance)
            upper_bound = gt_budget * (1 + tolerance)
            
            is_correct = lower_bound <= parsed_budget <= upper_bound
            
            return is_correct
        except:
            return False
    
    def check_people(self, parsed, ground_truth):
        """
        Check if people count was extracted correctly
        
        Args:
            parsed: Dictionary from parser
            ground_truth: Dictionary from dataset
            
        Returns:
            True if correct, False if incorrect
        """
        try:
            # Convert to integers
            parsed_people = int(parsed.get('people_number', 0))
            gt_people = int(ground_truth.get('people_number', 0))
            
            # Must be exact match
            return parsed_people == gt_people
        except:
            return False
    
    def evaluate_single_query(self, query, ground_truth):
        """
        Evaluate ONE query
        
        Steps:
        1. Parse the query using our parser
        2. Check each field (destination, duration, budget, people)
        3. Return which fields are correct/incorrect
        
        Args:
            query: Natural language query string (e.g., "Plan a 3-day trip to Rome...")
            ground_truth: Dictionary with correct answers from dataset
            
        Returns:
            Dictionary with parsed results and correctness for each field
        """
        # Step 1: Parse the query using our parser
        try:
            parsed_result = self.parser.parse(query)
        except Exception as e:
            # If parsing fails, log the error
            print(f"  ERROR parsing query: {e}")
            parsed_result = {}
        
        # Step 2: Check each field against ground truth
        results = {
            'parsed': parsed_result,  # What our parser extracted
            'correct': {
                'destination': self.check_destination(parsed_result, ground_truth),
                'duration': self.check_duration(parsed_result, ground_truth),
                'budget': self.check_budget(parsed_result, ground_truth),
                'people': self.check_people(parsed_result, ground_truth)
            }
        }
        
        return results
    
    def run_evaluation(self):
        """
        Main function to run the complete evaluation
        
        Steps:
        1. Load validation data
        2. Evaluate each query
        3. Calculate accuracy metrics
        4. Display results
        5. Save results to files
        """
        print("\n" + "="*70)
        print(" "*15 + "PARSER EVALUATION - MILESTONE 4")
        print("="*70)
        
        # STEP 1: Load validation data
        print("\n[STEP 1/5] Loading validation data...")
        df = self.load_validation_data()
        self.results['total'] = len(df)
        print(f"✓ Loaded {len(df)} validation queries\n")
        
        # STEP 2: Evaluate each query
        print("[STEP 2/5] Evaluating queries...")
        print("-" * 70)
        
        for idx, row in df.iterrows():
            # Get query and ground truth from CSV row
            query = row['query']
            ground_truth = row.to_dict()  # Convert row to dictionary
            
            # Show progress every 10 queries
            current = idx + 1
            if current % 10 == 0 or current == 1:
                print(f"Processing query {current}/{len(df)}...")
            
            # Evaluate this single query
            eval_result = self.evaluate_single_query(query, ground_truth)
            
            # Update correctness counters
            if eval_result['correct']['destination']:
                self.results['destination_correct'] += 1
            if eval_result['correct']['duration']:
                self.results['duration_correct'] += 1
            if eval_result['correct']['budget']:
                self.results['budget_correct'] += 1
            if eval_result['correct']['people']:
                self.results['people_correct'] += 1
            
            # Store detailed information for this query
            self.results['details'].append({
                'query_id': current,
                'query_text': query[:100] + '...' if len(query) > 100 else query,
                'ground_truth': {
                    'destination': ground_truth.get('dest'),
                    'duration': ground_truth.get('days'),
                    'budget': ground_truth.get('budget'),
                    'people': ground_truth.get('people_number')
                },
                'parsed': eval_result['parsed'],
                'correct': eval_result['correct']
            })
        
        print(f"✓ Evaluated all {len(df)} queries\n")
        
        # STEP 3: Calculate accuracy metrics
        print("[STEP 3/5] Calculating accuracy metrics...")
        total = self.results['total']
        
        # Calculate percentage for each field
        self.results['metrics'] = {
            'destination_accuracy': (self.results['destination_correct'] / total * 100) if total > 0 else 0,
            'duration_accuracy': (self.results['duration_correct'] / total * 100) if total > 0 else 0,
            'budget_accuracy': (self.results['budget_correct'] / total * 100) if total > 0 else 0,
            'people_accuracy': (self.results['people_correct'] / total * 100) if total > 0 else 0,
        }
        
        # Calculate overall accuracy (average of all fields)
        total_checks = total * 4  # 4 fields per query
        total_correct = (
            self.results['destination_correct'] + 
            self.results['duration_correct'] + 
            self.results['budget_correct'] + 
            self.results['people_correct']
        )
        self.results['metrics']['overall_accuracy'] = (total_correct / total_checks * 100) if total_checks > 0 else 0
        
        print("✓ Metrics calculated\n")
        
        # STEP 4: Display results to console
        print("[STEP 4/5] Displaying results...")
        self.display_results()
        
        # STEP 5: Save results to files
        print("\n[STEP 5/5] Saving results to files...")
        self.save_results()
        print("✓ Evaluation complete!\n")
    
    def display_results(self):
        """
        Display evaluation results to console
        
        Shows:
        - Total queries evaluated
        - Accuracy for each field
        - Overall accuracy
        - Sample results
        """
        print("\n" + "="*70)
        print(" "*25 + "EVALUATION RESULTS")
        print("="*70)
        
        metrics = self.results['metrics']
        total = self.results['total']
        
        # Display summary
        print(f"\nTotal Queries Evaluated: {total}")
        print("\n" + "-"*70)
        print("ACCURACY BY FIELD:")
        print("-"*70)
        print(f"  Destination:  {metrics['destination_accuracy']:.1f}%  ({self.results['destination_correct']}/{total} correct)")
        print(f"  Duration:     {metrics['duration_accuracy']:.1f}%  ({self.results['duration_correct']}/{total} correct)")
        print(f"  Budget:       {metrics['budget_accuracy']:.1f}%  ({self.results['budget_correct']}/{total} correct)")
        print(f"  People Count: {metrics['people_accuracy']:.1f}%  ({self.results['people_correct']}/{total} correct)")
        print("-"*70)
        print(f"  OVERALL:      {metrics['overall_accuracy']:.1f}%")
        print("-"*70)
        
        # Show sample results (first 3 queries)
        print("\nSAMPLE RESULTS (first 3 queries):")
        print("-"*70)
        for i, detail in enumerate(self.results['details'][:3], 1):
            print(f"\nQuery {i}:")
            print(f"  Text: {detail['query_text']}")
            print(f"  Ground Truth: dest={detail['ground_truth']['destination']}, "
                  f"days={detail['ground_truth']['duration']}, "
                  f"budget={detail['ground_truth']['budget']}, "
                  f"people={detail['ground_truth']['people']}")
            print(f"  Parsed: {detail['parsed']}")
            print(f"  Correct: {detail['correct']}")
        print("="*70)
    
    def save_results(self):
        """
        Save results to multiple files in results folder
        
        Creates 3 files:
        1. parser_results_full.json - Complete results with all details
        2. parser_results_summary.txt - Human-readable summary
        3. parser_results_comparison.txt - Side-by-side comparison
        """
        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # FILE 1: Full results as JSON
        json_file = os.path.join(self.results_folder, f"parser_results_{timestamp}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Saved full results: {json_file}")
        
        # FILE 2: Summary as readable text
        summary_file = os.path.join(self.results_folder, f"parser_summary_{timestamp}.txt")
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("PARSER EVALUATION SUMMARY - MILESTONE 4\n")
            f.write("="*70 + "\n\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Queries: {self.results['total']}\n\n")
            
            f.write("ACCURACY METRICS:\n")
            f.write("-"*70 + "\n")
            metrics = self.results['metrics']
            f.write(f"Destination:  {metrics['destination_accuracy']:.1f}% ({self.results['destination_correct']}/{self.results['total']})\n")
            f.write(f"Duration:     {metrics['duration_accuracy']:.1f}% ({self.results['duration_correct']}/{self.results['total']})\n")
            f.write(f"Budget:       {metrics['budget_accuracy']:.1f}% ({self.results['budget_correct']}/{self.results['total']})\n")
            f.write(f"People Count: {metrics['people_accuracy']:.1f}% ({self.results['people_correct']}/{self.results['total']})\n")
            f.write("-"*70 + "\n")
            f.write(f"OVERALL:      {metrics['overall_accuracy']:.1f}%\n")
            f.write("="*70 + "\n")
        print(f"  ✓ Saved summary: {summary_file}")
        
        # FILE 3: Detailed comparison (first 20 queries)
        comparison_file = os.path.join(self.results_folder, f"parser_comparison_{timestamp}.txt")
        with open(comparison_file, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("PARSER RESULTS - DETAILED COMPARISON\n")
            f.write("="*70 + "\n\n")
            
            # Show first 20 queries
            for detail in self.results['details'][:20]:
                f.write(f"\nQuery {detail['query_id']}:\n")
                f.write(f"  Text: {detail['query_text']}\n\n")
                
                f.write(f"  GROUND TRUTH:\n")
                f.write(f"    Destination: {detail['ground_truth']['destination']}\n")
                f.write(f"    Duration:    {detail['ground_truth']['duration']} days\n")
                f.write(f"    Budget:      ${detail['ground_truth']['budget']}\n")
                f.write(f"    People:      {detail['ground_truth']['people']}\n\n")
                
                f.write(f"  PARSED RESULT:\n")
                parsed = detail['parsed']
                f.write(f"    Destination: {parsed.get('destination', 'NOT FOUND')}\n")
                f.write(f"    Duration:    {parsed.get('duration', 'NOT FOUND')} days\n")
                f.write(f"    Budget:      ${parsed.get('budget', 'NOT FOUND')}\n")
                f.write(f"    People:      {parsed.get('people_number', 'NOT FOUND')}\n\n")
                
                f.write(f"  CORRECTNESS:\n")
                correct = detail['correct']
                f.write(f"    Destination: {'✓ CORRECT' if correct['destination'] else '✗ INCORRECT'}\n")
                f.write(f"    Duration:    {'✓ CORRECT' if correct['duration'] else '✗ INCORRECT'}\n")
                f.write(f"    Budget:      {'✓ CORRECT' if correct['budget'] else '✗ INCORRECT'}\n")
                f.write(f"    People:      {'✓ CORRECT' if correct['people'] else '✗ INCORRECT'}\n")
                f.write("-"*70 + "\n")
        print(f"  ✓ Saved comparison: {comparison_file}")


# ==============================================================================
# MAIN PROGRAM
# ==============================================================================

def main():
    """
    Main function - this runs when you execute the script
    
    Usage:
        python evaluate_parser.py
    """
    print("\n" + "="*70)
    print(" "*20 + "STARTING PARSER EVALUATION")
    print("="*70)
    
    # Create evaluator (sample_size=50 means evaluate 50 queries)
    evaluator = ParserEvaluator(sample_size=50)
    
    # Run the evaluation
    evaluator.run_evaluation()
    
    print("\n" + "="*70)
    print(" "*25 + "EVALUATION COMPLETE!")
    print("="*70)
    print("\nCheck the 'results' folder for detailed output files.")
    print("="*70 + "\n")


# This runs the main() function when script is executed
if __name__ == "__main__":
    main()
