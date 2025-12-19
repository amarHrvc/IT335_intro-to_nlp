"""
Simple test script to verify parser evaluator works

Run this BEFORE running the full evaluation to check if everything is set up correctly.

Usage:
    python test_simple.py
"""

import sys
import os

print("="*70)
print(" "*20 + "SIMPLE TEST - Parser Evaluator")
print("="*70)

# Test 1: Check Python version
print("\n[Test 1] Checking Python version...")
print(f"  Python version: {sys.version.split()[0]}")
if sys.version_info >= (3, 6):
    print("  ✓ Python version OK")
else:
    print("  ✗ Python version too old (need 3.6+)")

# Test 2: Check if we can import pandas
print("\n[Test 2] Checking pandas...")
try:
    import pandas as pd
    print(f"  Pandas version: {pd.__version__}")
    print("  ✓ Pandas installed")
except ImportError:
    print("  ✗ Pandas NOT installed")
    print("  Run: pip install pandas")

# Test 3: Check if we can find validation.csv
print("\n[Test 3] Checking for validation dataset...")
# Prefer cleaned version first, then fall back to original
possible_paths = [
    "../../TravelPlanner_cleaned/validation_cleaned.csv",  # BEST
    "../../TravelPlanner/validation.csv",                  # Fallback
    "../TravelPlanner_cleaned/validation_cleaned.csv",     # Alternative
]

found = False
for path in possible_paths:
    full_path = os.path.join(os.path.dirname(__file__), path)
    if os.path.exists(full_path):
        print(f"  ✓ Found at: {full_path}")
        
        # Try to read it
        try:
            df = pd.read_csv(full_path)
            print(f"    Contains {len(df)} queries")
            print(f"    Columns: {list(df.columns[:5])}...")
            found = True
            break
        except Exception as e:
            print(f"  ✗ Found but can't read: {e}")
else:
    if not found:
        print("  ✗ Validation dataset NOT found")
        print("  Make sure TravelPlanner_cleaned or TravelPlanner folder exists")

# Test 4: Check if we can import parser
print("\n[Test 4] Checking QueryParser...")
try:
    # Add parent to path
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    
    from agents.query_parser import QueryParser
    print("  ✓ QueryParser imported successfully")
    
    # Try to create parser
    try:
        parser = QueryParser(use_llm=False)
        print("  ✓ QueryParser initialized")
        
        # Try to parse a simple query
        try:
            result = parser.parse("Plan a 3-day trip to Rome for 2 people with $1000 budget")
            print(f"  ✓ Parser works! Sample result:")
            print(f"    Destination: {result.get('destination', 'N/A')}")
            print(f"    Duration: {result.get('duration', 'N/A')}")
            print(f"    Budget: {result.get('budget', 'N/A')}")
        except Exception as e:
            print(f"  ⚠ Parser initialized but failed to parse: {e}")
    except Exception as e:
        print(f"  ⚠ QueryParser imported but can't initialize: {e}")
        
except ImportError as e:
    print(f"  ✗ Cannot import QueryParser: {e}")

# Test 5: Check results folder
print("\n[Test 5] Checking results folder...")
results_dir = os.path.join(os.path.dirname(__file__), 'results')
if os.path.exists(results_dir):
    print(f"  ✓ Results folder exists: {results_dir}")
else:
    print(f"  Creating results folder: {results_dir}")
    try:
        os.makedirs(results_dir)
        print("  ✓ Results folder created")
    except Exception as e:
        print(f"  ✗ Cannot create folder: {e}")

# Summary
print("\n" + "="*70)
print(" "*25 + "TEST SUMMARY")
print("="*70)
print("\nIf all tests passed (✓), you can run:")
print("  python evaluate_parser.py")
print("\nIf any tests failed (✗), fix those issues first.")
print("="*70 + "\n")
