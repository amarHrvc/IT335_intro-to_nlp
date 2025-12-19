"""
Generate Tables and Charts from Table Models

This script uses pre-generated table models (JSON files) to create
visualizations including:
- Markdown tables (for research paper)
- CSV files (for data analysis)
- Charts (bar and pie charts for presentations)

Usage:
    cd TIG_Implementation/evaluation
    python generate_tables.py

Output:
    - results/visualizations/*.md (Markdown tables)
    - results/visualizations/*.csv (CSV files)
    - results/visualizations/*.png (Chart images)

Author: TIG Project - IT_335
Date: December 8, 2025
"""

import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, '..')

from helpers.table_visualizer import TableVisualizer


def load_table_models():
    """
    Load pre-generated table models from JSON files
    
    Returns:
        tuple: (parser_table, planner_table, system_table) as dictionaries
        
    Raises:
        FileNotFoundError: If table model files are not found
    """
    # Define table model file paths
    parser_model = Path('parser_performance_table_model.json')
    planner_model = Path('planner_success_table_model.json')
    system_model = Path('system_overview_table_model.json')
    
    # Check if files exist
    missing = []
    if not parser_model.exists():
        missing.append(str(parser_model))
    if not planner_model.exists():
        missing.append(str(planner_model))
    if not system_model.exists():
        missing.append(str(system_model))
    
    if missing:
        raise FileNotFoundError(
            f"Table model files not found:\n" +
            "\n".join(f"  - {f}" for f in missing) +
            "\n\nPlease ensure all table model JSON files are present."
        )
    
    print("Loading table models:")
    print(f"  Parser:  {parser_model.name}")
    print(f"  Planner: {planner_model.name}")
    print(f"  System:  {system_model.name}")
    print()
    
    # Load JSON data
    with open(parser_model, 'r', encoding='utf-8') as f:
        parser_table = json.load(f)
    
    with open(planner_model, 'r', encoding='utf-8') as f:
        planner_table = json.load(f)
    
    with open(system_model, 'r', encoding='utf-8') as f:
        system_table = json.load(f)
    
    return parser_table, planner_table, system_table


def main():
    """
    Main function to generate all tables and charts from table models
    """
    print("=" * 70)
    print("GENERATING TABLES AND CHARTS FROM TABLE MODELS")
    print("=" * 70)
    print()
    
    try:
        # Step 1: Load table models from JSON files
        print("Step 1: Loading table models...")
        parser_table, planner_table, system_table = load_table_models()
        print("✓ Table models loaded successfully")
        print()
        
        # Step 2: Generate visualizations
        output_dir = 'results/visualizations'
        print(f"Step 2: Generating visualizations...")
        print(f"  Output directory: {output_dir}/")
        print()
        
        # Parser visualizations
        print("  [1/3] Generating parser performance visualizations...")
        viz1 = TableVisualizer(parser_table)
        viz1.generate_all(output_dir, 'parser_performance')
        print()
        
        # Planner visualizations
        print("  [2/3] Generating planner success visualizations...")
        viz2 = TableVisualizer(planner_table)
        viz2.generate_all(output_dir, 'planner_success')
        print()
        
        # System overview
        print("  [3/3] Generating system overview visualizations...")
        viz3 = TableVisualizer(system_table)
        viz3.generate_all(output_dir, 'system_overview')
        print()
        
        # Success summary
        print("=" * 70)
        print("✓ ALL TABLES AND CHARTS GENERATED SUCCESSFULLY!")
        print("=" * 70)
        print()
        print(f"Output location: {output_dir}/")
        print()
        print("Files created:")
        print("  Parser Performance:")
        print("    - parser_performance.md")
        print("    - parser_performance.csv")
        print("    - parser_performance_bar.png")
        print()
        print("  Planner Success:")
        print("    - planner_success.md")
        print("    - planner_success.csv")
        print("    - planner_success_bar.png")
        print("    - planner_success_pie.png")
        print()
        print("  System Overview:")
        print("    - system_overview.md")
        print("    - system_overview.csv")
        print("    - system_overview_bar.png")
        print()
        print("=" * 70)
        print()
        print("Next steps:")
        print("  1. Check the markdown files (*.md) - ready for your paper")
        print("  2. Check the charts (*.png) - ready for presentations")
        print("  3. CSV files (*.csv) available for further analysis")
        print()
        print("You can now copy these files into your research paper!")
        print()
        
    except FileNotFoundError as e:
        print()
        print("=" * 70)
        print("ERROR: Missing Files")
        print("=" * 70)
        print()
        print(str(e))
        print()
        return 1
        
    except Exception as e:
        print()
        print("=" * 70)
        print("ERROR: Unexpected Error")
        print("=" * 70)
        print()
        print(f"Error: {e}")
        print()
        print("If you see 'matplotlib not installed', run:")
        print("  pip install matplotlib")
        print()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
