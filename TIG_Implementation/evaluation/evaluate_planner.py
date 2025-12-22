"""
    Planner Evaluation Script - Milestone 4, Task 1.2
    Evaluates itinerary planner performance on validation dataset

    SIMPLIFIED VERSION FOR LEARNING

    This script:
    1. Loads validation data (30 sample queries, configurable)
    2. Runs planner on each query
    3. Checks 5 criteria (generated, days, budget, people, destination)
    4. Classifies as Complete/Partial/Failed
    5. Saves detailed results to 3 files

    SUCCESS LEVELS:
    - Complete: 5/5 criteria met ✅
    - Partial: 3-4/5 criteria met ⚠️
    - Failed: 0-2/5 criteria met ❌
    """

import sys
import os
import pandas as pd
import json
import re
from datetime import datetime

from numpy.matlib import empty

# Add parent directory to Python path so we can import planner
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import our planner and dataset
from agents.planner import ItineraryPlanner
from utils.data_loader import TravelDataSet


class PlannerEvaluator:
    """
    Simple class to evaluate planner performance

    What it does:
    - Loads validation queries from CSV
    - Generates itinerary for each query
    - Checks 5 success criteria
    - Classifies result (Complete/Partial/Failed)
    - Saves results to files
    """

    def __init__(self, sample_size=5):
        """
        Initialize the evaluator

        Args:
            sample_size: How many queries to test (default: 30, configurable)
        """
        self.sample_size = sample_size

        print("Initializing planner evaluator...")

        # Load dataset (needed by planner for few-shot examples)
        print("  Loading dataset...")
        self.dataset = TravelDataSet()

        # Create the planner (uses LLM to generate itineraries)
        print("  Initializing planner...")
        self.planner = ItineraryPlanner(self.dataset, debug=True)

        # Dictionary to store results
        self.results = {
            'total': 0,  # Total queries evaluated
            'complete': 0,  # Count with 5/5 criteria
            'partial': 0,  # Count with 3-4/5 criteria
            'failed': 0,  # Count with 0-2/5 criteria
            'details': []  # List of detailed results per query
        }



        # Create results folder if it doesn't exist
        self.results_folder = os.path.join(current_dir, 'results')
        if not os.path.exists(self.results_folder):
            os.makedirs(self.results_folder)
            print(f"  Created results folder: {self.results_folder}")

        print("✓ Planner evaluator ready\n")

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
            "../../TravelPlanner/validation.csv",  # Fallback to original
            "../TravelPlanner_cleaned/validation_cleaned.csv",  # Alternative path 1
            "../TravelPlanner/validation.csv"  # Alternative path 2
        ]

        df = None

        # Try each path until we find one that exists
        for path in possible_paths:
            # IMMPLEMENT: Check if path exists
            full_path = os.path.join(current_dir, path)
            if os.path.exists(full_path):
                print(f"Found dataset: {full_path}")
                # IMMPLEMENT: Read CSV into df
                df = pd.read_csv(full_path)
                break  # Found it, stop looking

        # If we couldn't find the file, stop
        if df is None:
            raise FileNotFoundError(
                "Could not find validation_cleaned.csv or validation.csv. "
                "Please make sure TravelPlanner_cleaned folder exists."
            )

        print(f"Total queries in dataset: {len(df)}")

        # If dataset is larger than sample_size, pick random sample
        # WHY SAMPLE: Testing 30 queries is enough, faster than all 180
        if len(df) > self.sample_size:
            # IMMPLEMENT: Sample random queries
            # HINT: df.sample(n=?, random_state=42) for reproducibility
            df = df.sample(n=self.sample_size, random_state=42)
            print(f"Sampled {self.sample_size} random queries for evaluation")

        print(f"✓ Loaded {len(df)} queries for evaluation\n")

        return df

    def itinerary_is_generated(self, result):
        """
        Criterion 1: Itinerary was generated (not empty or error)

        WHY THIS MATTERS:
        If planner couldn't generate anything, all other checks fail.
        This is the most basic requirement.

        Args:
            result: Dictionary returned from planner.generate_itinerary()
                    Format: {'itinerary': '...', 'parsed_query': {...}, ...}
                    Or: {'error': '...', 'itinerary': 'Failed to generate...'}

        Returns:
            True if valid itinerary exists, False otherwise
        """
        # Check 1: Does result have an 'error' key?
        # IMMPLEMENT: if 'error' in result → return False
        if 'error' in result:
            return False

        # Check 2: Get the itinerary text
        # IMMPLEMENT: itinerary = result.get('itinerary', '')
        itinerary = result.get('itinerary')

        # Check 3: Is it empty or failed message?
        # IMMPLEMENT: if empty or == "Failed to generate itinerary" → return False
        if itinerary == empty or itinerary is None or itinerary == 'Failed to generate itinerary':
            return False

        # If we got here, itinerary was generated
        return True

    def has_correct_number_of_days(self, result, ground_truth):
        """
        Criterion 2: Itinerary has correct number of days

        WHY THIS MATTERS:
        User asks for 3-day trip, planner must deliver 3 days, not 2 or 4.

        HOW WE CHECK:
        Itinerary is JSON string like: {"Day 1": {...}, "Day 2": {...}, "Day 3": {...}}
        Count how many "Day X" entries exist in the string.

        Args:
            result: Dictionary with 'itinerary' key (JSON string)
            ground_truth: DataFrame row with 'days' column

        Returns:
            True if day count matches, False otherwise
        """
        # Get itinerary text
        itinerary_text = result.get('itinerary', '')

        # Count "Day 1", "Day 2", etc. using regex
        # WHY REGEX: Itinerary format is: "Day 1": {...}, "Day 2": {...}
        # PATTERN: r'"Day \d+"' matches "Day 1", "Day 2", "Day 3", etc.
        pattern = r'"Day \d+"'
        days_found = 0


        # IMMPLEMENT: Use re.findall() to find all matches
        # HINT: matches = re.findall(pattern, itinerary_text)
        # HINT: days_found = len(matches)
        matches = re.findall(pattern, itinerary_text)

        days_found = len(matches)

        # Get expected days from ground truth
        expected_days = int(ground_truth['days'])

        print(f"    Days: Found {days_found}, Expected {expected_days}")

        # IMMPLEMENT: return True if days_found == expected_days
        return days_found == expected_days

    def check_budget(self, result, ground_truth):
        """
        Criterion 3: Total cost does not exceed budget

        WHY THIS MATTERS:
        User specifies budget = $2000. Planner must stay within it.
        Can be under (good!), but cannot exceed.

        HOW WE CHECK:
        Look for "Total Cost": "$1670" in itinerary JSON string.
        Extract number, compare to budget limit.

        Args:
            result: Dictionary with itinerary
            ground_truth: DataFrame row with 'budget' column

        Returns:
            True if within budget (or no cost found), False if exceeded
        """
        itinerary_text = result.get('itinerary', '')

        # Extract "Total Cost": "$1670" using regex
        # PATTERN: "Total Cost": "$NUMBER"
        pattern = r'"Total Cost":\s*"\$(\d+)"'

        # IMMPLEMENT: Use re.search() to find cost
        # HINT: match = re.search(pattern, itinerary_text)
        # HINT: if not match → return True (no cost, assume followed instructions)

        match = None

        match = re.search(pattern, itinerary_text)

        if not match:
            # No cost found, assume planner followed instructions
            print(f"    Budget: No cost found, assuming met")
            return True

        # Extract cost as integer
        # IMMPLEMENT: total_cost = int(match.group(1))
        total_cost = int(match.group(1))

        budget_limit = int(ground_truth['budget'])

        print(f"    Budget: ${total_cost} vs ${budget_limit} limit")

        # Must not exceed (can be under!)
        # IMMPLEMENT: return total_cost <= budget_limit
        return total_cost <= budget_limit

    def check_criterion_4_people(self, result, ground_truth):
        """
        Criterion 4: Accommodates correct number of people

        WHY THIS MATTERS:
        User says "trip for 2 people", planner must handle 2 people.

        HOW WE CHECK:
        Look at parsed_query['people_number'] in result.
        This shows the planner understood the requirement.

        ALTERNATIVE (more complex):
        Could parse itinerary for hotel room capacities, but that's harder.

        Args:
            result: Dictionary with 'parsed_query'
            ground_truth: DataFrame row with 'people_number'

        Returns:
            True if people count matches
        """
        # Get parsed query from result
        parsed = result.get('parsed_query', {})

        # IMMPLEMENT: Extract people numbers
        # HINT: expected = int(ground_truth['people_number'])
        # HINT: actual = int(parsed.get('people_number', 1))

        expected = int(ground_truth['people_number'])
        actual = int(parsed.get('people_number', 1))

        print(f"    People: {actual} vs {expected} expected")

        # IMMPLEMENT: return actual == expected
        return actual == expected

    def check_criterion_5_destination(self, result, ground_truth):
        """
        Criterion 5: Destination city appears in itinerary

        WHY THIS MATTERS:
        If user asks for Rome trip, "Rome" should appear in the itinerary.

        HOW WE CHECK:
        Simple text search (case-insensitive) for city name in itinerary.

        ⚠️ NOTE ON NORMALIZATION:
        We have normalize_city() functions in:
        1. TravelPlannerProcessor.normalize_cities() - Root level
        2. evaluate_parser.normalize_city() - Parser evaluator

        DECISION: Write simple inline (no import needed for this check)

        Args:
            result: Dictionary with itinerary text
            ground_truth: DataFrame row with 'dest' column

        Returns:
            True if destination mentioned in itinerary
        """
        # Get itinerary text and make lowercase for case-insensitive search
        itinerary_text = result.get('itinerary', '').lower()

        # Get destination and normalize (simple: lowercase + strip whitespace)
        # IMMPLEMENT: expected_dest = str(ground_truth['dest']).lower().strip()
        expected_dest = str(ground_truth['dest']).lower().strip()

        print(f"    Destination: Checking for '{expected_dest}' in itinerary")

        # Check if destination appears in text
        # IMMPLEMENT: return expected_dest in itinerary_text
        return expected_dest in itinerary_text

    def evaluate_single_query(self, row, index):
        """
        Evaluate planner on one query

        WORKFLOW:
        1. Build query dict from row
        2. Generate itinerary using planner
        3. Check all 5 criteria
        4. Count how many criteria met
        5. Classify as Complete/Partial/Failed
        6. Return results

        Args:
            row: DataFrame row with query parameters
            index: Query number (for progress display)

        Returns:
            Dictionary with evaluation results
        """
        print(f"\nEvaluating query #{index + 1}...")

        # Build query dictionary from DataFrame row
        query = {
            'destination': row['dest'],
            'duration': int(row['days']),
            'budget': int(row['budget']),
            'people_number': int(row['people_number'])
        }

        print(f"  Query: {query['duration']}-day trip to {query['destination']}, "
              f"${query['budget']} for {query['people_number']} people")

        try:
            # Generate itinerary using planner (k=3 means use 3 similar examples)
            # WHY k=3: Few-shot learning works best with 3-5 examples
            print("  Generating itinerary...")
            result = self.planner.generate_itinerary(query, k=3, debug=True)

            # Extract debug info if available
            debug_info = result.get('debug_info', None)


            print("  Checking criteria...")

            # Track failure reasons for debugging
            failure_reasons = []

            # Check all 5 criteria
            # IMMPLEMENT: Call each check function
            criteria = {
                'generated': self.itinerary_is_generated(result),
                'days': self.has_correct_number_of_days(result, row),
                'budget': self.check_budget(result, row),
                'people': self.check_criterion_4_people(result, row),
                'destination': self.check_criterion_5_destination(result, row)
            }

            # Add failure reasons for each failed criterion
            if not criteria['generated']:
                failure_reasons.append("Failed to generate itinerary (empty or error)")
            if not criteria['days']:
                failure_reasons.append(f"Wrong number of days (expected {row['days']})")
            if not criteria['budget']:
                failure_reasons.append(f"Exceeded budget (limit: ${row['budget']})")
            if not criteria['people']:
                failure_reasons.append(f"Wrong people count (expected {row['people_number']})")
            if not criteria['destination']:
                failure_reasons.append(f"Wrong destination (expected {row['dest']})")

            # Count how many criteria were met
            # IMMPLEMENT: sum(criteria.values()) counts True values
            count = sum(criteria.values())

            # Classify based on count
            # RULES:
            # - 5/5 = Complete (perfect!)
            # - 3-4/5 = Partial (usable but imperfect)
            # - 0-2/5 = Failed (not usable)
            if count == 5:
                level = 'complete'
            elif count >= 3:
                level = 'partial'
            else:
                level = 'failed'

            print(f"  Result: {level.upper()} ({count}/5 criteria met)")

            # Return evaluation result
            eval_result = {
                'query': query,
                'result': result,
                'criteria': criteria,
                'count': count,
                'level': level,
                'failure_reasons': failure_reasons
            }

            # Add debug info if available
            if debug_info:
                eval_result['debug_info'] = debug_info

            return eval_result

        except Exception as e:
            # If planner crashes, treat as failed
            print(f"  ❌ Error: {e}")
            return {
                'query': query,
                'error': str(e),
                'criteria': {
                    'generated': False,
                    'days': False,
                    'budget': False,
                    'people': False,
                    'destination': False
                },
                'count': 0,
                'level': 'failed'
            }

    def run_evaluation(self):
        """
        Main evaluation workflow

        STEPS:
        1. Load validation data
        2. Loop through queries
        3. Evaluate each query
        4. Track results
        5. Display summary
        6. Save to files
        """
        print("\n" + "=" * 70)
        print("PLANNER EVALUATION - MILESTONE 4")
        print("=" * 70)

        # Step 1: Load validation data
        print("\n[STEP 1/4] Loading validation data...")
        data = self.load_validation_data()

        # Step 2: Evaluate all queries
        print("\n[STEP 2/4] Evaluating queries...")
        print(f"Will evaluate {len(data)} queries...\n")

        # Loop through each query
        for index, row in data.iterrows():
            # Show progress every 5 queries
            if (index + 1) % 5 == 0:
                print(f"\n--- Progress: {index + 1}/{len(data)} queries ---")

            # Evaluate this query
            eval_result = self.evaluate_single_query(row, index)

            # Update results counters
            # IMMPLEMENT:
            self.results['total'] += 1
            self.results[eval_result['level']] += 1 # (complete/partial/failed)
            self.results['details'].append(eval_result)

        print("\n✓ Evaluation complete!")

        # Step 3: Display results
        print("\n[STEP 3/4] Displaying results...")
        self.display_results()

        # Step 4: Save results
        print("\n[STEP 4/4] Saving results...")
        self.save_results()

        print("\n" + "=" * 70)
        print("✓ EVALUATION COMPLETE")
        print("=" * 70)

    def display_results(self):
        """
        Print evaluation summary to console

        DISPLAYS:
        - Total queries
        - Success level breakdown
        - Percentages
        - Overall success rate
        """
        print("\n" + "=" * 70)
        print("EVALUATION RESULTS")
        print("=" * 70)

        total = self.results['total']
        complete = self.results['complete']
        partial = self.results['partial']
        failed = self.results['failed']

        print(f"\nTotal Queries Evaluated: {total}")
        print("\n" + "-" * 70)
        print("SUCCESS LEVELS:")
        print("-" * 70)

        # IMMPLEMENT: Calculate percentages
        # HINT: complete_pct = (complete / total) * 100
        complete_pct = (complete / total) * 100
        partial_pct = (partial / total) * 100
        failed_pct = (failed / total) * 100

        print(f"  Complete (5/5): {complete:2d} ({complete_pct:.1f}%)")
        print(f"  Partial (3-4):  {partial:2d} ({partial_pct:.1f}%)")
        print(f"  Failed (0-2):   {failed:2d} ({failed_pct:.1f}%)")
        print("-" * 70)

        # Overall success rate (complete + partial = usable itineraries)
        success = complete + partial
        success_pct = 0
        if total == 0 or success == 0:
            print("succes_pct is 0 !")
        else:
            success_pct = (success / total) * 100
        print(f"\nOverall Success Rate: {success_pct:.1f}% ({success}/{total})")
        print("(Success = Complete + Partial, i.e., usable itineraries)")

    def save_results(self):
        """
        Save 3 output files (same pattern as parser evaluator)

        FILES:
        1. planner_results_TIMESTAMP.json - Complete data for further analysis
        2. planner_summary_TIMESTAMP.txt - Human-readable summary stats
        3. planner_comparison_TIMESTAMP.txt - Detailed query-by-query results

        WHY 3 FILES:
        - JSON for programmatic analysis
        - Summary TXT for quick overview
        - Comparison TXT for detailed inspection
        """
        # Generate timestamp for unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # File 1: Save JSON (complete data)
        json_file = os.path.join(self.results_folder, f"planner_results_{timestamp}.json")

        # IMMPLEMENT: Save self.results to JSON
        # HINT: with open(json_file, 'w') as f:
        # HINT:     json.dump(self.results, f, indent=2, default=str)
        # NOTE: default=str handles any non-serializable objects
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Saved full results: {json_file}")

        print(f"✓ Saved JSON: {json_file}")

        # File 2: Save summary TXT
        summary_file = os.path.join(self.results_folder, f"planner_summary_{timestamp}.txt")

        total = self.results['total']
        complete = self.results['complete']
        partial = self.results['partial']
        failed = self.results['failed']

        complete_pct = (complete / total) * 100
        partial_pct = (partial / total) * 100
        failed_pct = (failed / total) * 100
        success = complete + partial
        success_pct = (success / total) * 100

        # Write summary file
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("PLANNER EVALUATION SUMMARY\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Total Queries Evaluated: {total}\n\n")
            f.write("SUCCESS LEVELS:\n")
            f.write("-" * 70 + "\n")
            f.write(f"  Complete (5/5): {complete:2d} ({complete_pct:.1f}%)\n")
            f.write(f"  Partial (3-4):  {partial:2d} ({partial_pct:.1f}%)\n")
            f.write(f"  Failed (0-2):   {failed:2d} ({failed_pct:.1f}%)\n")
            f.write("-" * 70 + "\n\n")
            f.write(f"Overall Success Rate: {success_pct:.1f}% ({success}/{total})\n")
            f.write("(Success = Complete + Partial, i.e., usable itineraries)\n")
            f.write("\n" + "=" * 70 + "\n")

        print(f"✓ Saved summary: {summary_file}")


        # File 3: Save comparison TXT (detailed)
        comparison_file = os.path.join(self.results_folder, f"planner_comparison_{timestamp}.txt")

        with open(comparison_file, 'w', encoding='utf-8') as f:
            f.write("PLANNER EVALUATION - DETAILED COMPARISON\n")
            f.write("=" * 70 + "\n\n")

            for idx, detail in enumerate(self.results['details'], 1):
                query = detail['query']
                criteria = detail.get('criteria', {})
                level = detail['level']
                count = detail['count']

                f.write(f"Query #{idx}\n")
                f.write("-" * 70 + "\n")
                f.write(f"Destination: {query['destination']}\n")
                f.write(f"Duration: {query['duration']} days\n")
                f.write(f"Budget: ${query['budget']}\n")
                f.write(f"People: {query['people_number']}\n\n")

                f.write("Criteria Met:\n")
                f.write(f"  Generated:    {'✓' if criteria.get('generated') else '✗'}\n")
                f.write(f"  Days:         {'✓' if criteria.get('days') else '✗'}\n")
                f.write(f"  Budget:       {'✓' if criteria.get('budget') else '✗'}\n")
                f.write(f"  People:       {'✓' if criteria.get('people') else '✗'}\n")
                f.write(f"  Destination:  {'✓' if criteria.get('destination') else '✗'}\n\n")

                f.write(f"Result: {level.upper()} ({count}/5)\n")
                f.write("=" * 70 + "\n\n")

        print(f"✓ Saved comparison: {comparison_file}")

        # Generate detailed formatted report
        try:
            from format_evaluation_results import format_evaluation_results
            detailed_file = json_file.replace('.json', '_detailed.txt')
            format_evaluation_results(json_file, detailed_file)
            print(f"   ✓ Detailed debug report: {detailed_file}")
        except Exception as e:
            print(f"   ⚠️  Could not generate detailed report: {e}")

        print("\nAll results saved to 'results/' folder")


def main():
    """
    Main entry point

    USAGE:
        python evaluate_planner.py

    WHAT IT DOES:
        1. Creates evaluator (default 30 samples)
        2. Runs evaluation
        3. Saves results
    """
    print("\n" + "=" * 70)
    print("PLANNER EVALUATOR - MILESTONE 4, TASK 1.2")
    print("=" * 70)

    # Create evaluator (change sample_size here if you want different amount)
    evaluator = PlannerEvaluator(sample_size=3)

    # Run evaluation
    evaluator.run_evaluation()

    print("\n✅ Done! Check 'results/' folder for output files.")


if __name__ == "__main__":
    main()
