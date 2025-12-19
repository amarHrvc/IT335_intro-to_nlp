# Table Visualizer - Complete Usage Guide

**Created:** December 8, 2025  
**Version:** 1.0  
**File:** `helpers/table_visualizer.py`

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Core Concept](#core-concept)
4. [Table Model Structure](#table-model-structure)
5. [Quick Start](#quick-start)
6. [Complete API Reference](#complete-api-reference)
7. [Usage Examples](#usage-examples)
8. [Chart Type Guide](#chart-type-guide)
9. [Advanced Features](#advanced-features)
10. [Troubleshooting](#troubleshooting)
11. [Best Practices](#best-practices)

---

## 🎯 Overview

The Table Visualizer is a **simple, table-first visualization system** that converts structured table data into multiple output formats:

- **Markdown tables** (for documentation, LLM analysis)
- **CSV files** (for Excel, data analysis)
- **Charts** (bar, pie, line - for presentations)

### Key Features

✅ **Simple table model** - Easy to understand and create  
✅ **Multiple outputs** - One table → many visualizations  
✅ **LLM-friendly** - Simple structure for AI assistance  
✅ **Flexible** - Works with any tabular data  
✅ **Configurable** - Specify which charts to generate  

---

## 📦 Installation

### Prerequisites

```bash
# Required for charts
pip install matplotlib

# Optional (for better-looking charts)
pip install seaborn
```

### File Location

```
TIG_Implementation/
└── helpers/
    └── table_visualizer.py
```

### Import

```python
from helpers.table_visualizer import TableVisualizer
```

---

## 💡 Core Concept

**Everything flows through a simple table structure:**

```
Raw Data → Simple Table Model → Multiple Outputs
              ↓
    (Can be created by LLM!)
              ↓
         ┌────────────┐
         │   Table    │
         └────┬───────┘
              │
    ┌─────────┼─────────┬─────────┐
    ↓         ↓         ↓         ↓
  .md       .csv      .png      .png
(Markdown)  (CSV)   (Bar)     (Pie)
```

**Why this approach?**

1. **Universal format** - Tables are understood everywhere
2. **Simple** - No complex data structures
3. **Flexible** - Works with any data
4. **LLM-friendly** - AI can easily create table structures

---

## 📊 Table Model Structure

### Basic Structure

```python
table = {
    'title': 'Table Title',           # Required: Table name
    'headers': ['Col1', 'Col2'],      # Required: Column names
    'rows': [                         # Required: Data rows
        ['val1', 'val2'],
        ['val3', 'val4']
    ],
    'footer': ['Total', '100'],       # Optional: Summary row
    'charts': ['bar', 'pie']          # Optional: Which charts to generate
}
```

### Field Descriptions

| Field | Type | Required | Description | Default |
|-------|------|----------|-------------|---------|
| `title` | string | Yes | Table title (used in charts) | - |
| `headers` | list[string] | Yes | Column headers | - |
| `rows` | list[list] | Yes | Data rows (2D array) | - |
| `footer` | list | No | Summary/total row | None |
| `charts` | list[string] | No | Chart types to generate | `['bar']` |

### Chart Types

- `'bar'` - Bar chart (comparing categories)
- `'pie'` - Pie chart (showing proportions)
- `'line'` - Line chart (showing trends)

---

## 🚀 Quick Start

### Step 1: Define Your Table

```python
from helpers.table_visualizer import TableVisualizer

# Simple table
table = {
    'title': 'Parser Performance',
    'headers': ['Field', 'Accuracy'],
    'rows': [
        ['Destination', '98%'],
        ['Duration', '88%'],
        ['Budget', '100%']
    ],
    'charts': ['bar']
}
```

### Step 2: Create Visualizer

```python
viz = TableVisualizer(table)
```

### Step 3: Generate Outputs

```python
# Option A: Generate all at once
viz.generate_all('output_folder', 'my_table')

# Option B: Generate individually
viz.to_markdown('output/table.md')
viz.to_csv('output/table.csv')
viz.to_bar_chart('output/chart.png')
```

**That's it!** 🎉

---

## 📖 Complete API Reference

### Class: `TableVisualizer`

```python
class TableVisualizer:
    def __init__(self, table_data)
    def to_markdown(self, output_path=None)
    def to_csv(self, output_path)
    def to_bar_chart(self, output_path, x_column=0, y_column=1)
    def to_pie_chart(self, output_path, label_column=0, value_column=1)
    def to_line_chart(self, output_path, x_column=0, y_columns=[1])
    def generate_all(self, output_dir, basename, chart_types=None)
```

---

### Method: `__init__(table_data)`

Initialize visualizer with table data.

**Parameters:**
- `table_data` (dict): Table structure with title, headers, rows, etc.

**Example:**
```python
table = {'title': 'My Data', 'headers': [...], 'rows': [...]}
viz = TableVisualizer(table)
```

---

### Method: `to_markdown(output_path=None)`

Generate Markdown table.

**Parameters:**
- `output_path` (str, optional): File path to save. If None, returns string only.

**Returns:**
- `str`: Markdown formatted table

**Output Format:**
```markdown
## Table Title

| Header1 | Header2 |
| --- | --- |
| val1 | val2 |
| val3 | val4 |
```

**Example:**
```python
# Get markdown string
md_text = viz.to_markdown()
print(md_text)

# Save to file
viz.to_markdown('output/table.md')
```

**Best for:**
- Documentation
- Research papers
- LLM analysis (easy to read/parse)
- GitHub README files

---

### Method: `to_csv(output_path)`

Generate CSV file.

**Parameters:**
- `output_path` (str): File path to save CSV

**Output Format:**
```csv
Header1,Header2
val1,val2
val3,val4
Total,100
```

**Example:**
```python
viz.to_csv('output/data.csv')
```

**Best for:**
- Excel import
- Data analysis
- Spreadsheet tools
- Archival/backup

---

### Method: `to_bar_chart(output_path, x_column=0, y_column=1)`

Generate bar chart (PNG).

**Parameters:**
- `output_path` (str): File path to save PNG
- `x_column` (int): Column index for X-axis (default: 0)
- `y_column` (int): Column index for Y-axis (default: 1)

**Example:**
```python
# Use columns 0 and 1
viz.to_bar_chart('charts/accuracy.png')

# Use different columns
viz.to_bar_chart('charts/count.png', x_column=0, y_column=2)
```

**Best for:**
- Comparing categories
- Showing performance metrics
- Side-by-side comparisons

**Handles:**
- Percentages: `"95.5%"` → `95.5`
- Numbers with commas: `"1,234"` → `1234`
- Plain numbers: `"42"` → `42`

---

### Method: `to_pie_chart(output_path, label_column=0, value_column=1)`

Generate pie chart (PNG).

**Parameters:**
- `output_path` (str): File path to save PNG
- `label_column` (int): Column index for labels (default: 0)
- `value_column` (int): Column index for values (default: 1)

**Example:**
```python
viz.to_pie_chart('charts/distribution.png')
```

**Best for:**
- Showing proportions/percentages
- Part-to-whole relationships
- Distribution visualization

---

### Method: `to_line_chart(output_path, x_column=0, y_columns=[1])`

Generate line chart (PNG).

**Parameters:**
- `output_path` (str): File path to save PNG
- `x_column` (int): Column index for X-axis (default: 0)
- `y_columns` (list[int]): Column indices for Y-axis (default: [1])

**Example:**
```python
# Single line
viz.to_line_chart('charts/trend.png')

# Multiple lines (columns 1, 2, 3)
viz.to_line_chart('charts/comparison.png', x_column=0, y_columns=[1, 2, 3])
```

**Best for:**
- Time series data
- Showing trends over time
- Comparing multiple metrics

---

### Method: `generate_all(output_dir, basename, chart_types=None)`

Generate all visualization types at once.

**Parameters:**
- `output_dir` (str): Directory to save all files
- `basename` (str): Base name for files (e.g., 'parser_results')
- `chart_types` (list[str], optional): Override table's charts setting

**Creates:**
- `{basename}.md` - Markdown (always)
- `{basename}.csv` - CSV (always)
- `{basename}_bar.png` - Bar chart (if 'bar' in charts)
- `{basename}_pie.png` - Pie chart (if 'pie' in charts)
- `{basename}_line.png` - Line chart (if 'line' in charts)

**Example:**
```python
# Use table's charts specification
viz.generate_all('output', 'results')

# Override with specific chart types
viz.generate_all('output', 'results', chart_types=['bar', 'pie'])

# Generate all types
viz.generate_all('output', 'results', chart_types=['bar', 'pie', 'line'])
```

---

## 💼 Usage Examples

### Example 1: Parser Evaluation Results

```python
from helpers.table_visualizer import TableVisualizer

# Create table from evaluation results
parser_table = {
    'title': 'Parser Accuracy by Field',
    'headers': ['Field', 'Accuracy %', 'Correct', 'Total'],
    'rows': [
        ['Destination', '98.0', '49', '50'],
        ['Duration', '88.0', '44', '50'],
        ['Budget', '100.0', '50', '50'],
        ['People', '76.0', '38', '50']
    ],
    'footer': ['Overall', '90.5', '181', '200'],
    'charts': ['bar']  # Bar chart for comparison
}

# Generate everything
viz = TableVisualizer(parser_table)
viz.generate_all('evaluation/results', 'parser_performance')

# Creates:
# - evaluation/results/parser_performance.md
# - evaluation/results/parser_performance.csv
# - evaluation/results/parser_performance_bar.png
```

---

### Example 2: Planner Success Distribution

```python
# Planner results with bar + pie charts
planner_table = {
    'title': 'Planner Success Distribution',
    'headers': ['Success Level', 'Count', 'Percentage'],
    'rows': [
        ['Complete (5/5)', '21', '70%'],
        ['Partial (3-4/5)', '9', '30%'],
        ['Failed (0-2/5)', '0', '0%']
    ],
    'footer': ['Total', '30', '100%'],
    'charts': ['bar', 'pie']  # Both charts!
}

viz = TableVisualizer(planner_table)
viz.generate_all('evaluation/results', 'planner_success')

# Creates:
# - planner_success.md
# - planner_success.csv
# - planner_success_bar.png (comparison)
# - planner_success_pie.png (proportions)
```

---

### Example 3: System Overview Table

```python
# Overall system performance
system_table = {
    'title': 'TIG System Performance Summary',
    'headers': ['Component', 'Metric', 'Score'],
    'rows': [
        ['Parser', 'Accuracy', '90.5%'],
        ['Planner', 'Success Rate', '100%'],
        ['System', 'Complete Rate', '70%']
    ],
    'charts': ['bar']
}

viz = TableVisualizer(system_table)
viz.generate_all('evaluation/results', 'system_overview')
```

---

### Example 4: Converting JSON to Table

```python
import json

# Read evaluation results
with open('parser_results.json') as f:
    data = json.load(f)

# Convert to table structure
table = {
    'title': 'Parser Performance',
    'headers': ['Field', 'Accuracy'],
    'rows': [
        ['Destination', f"{data['metrics']['destination_accuracy']}%"],
        ['Duration', f"{data['metrics']['duration_accuracy']}%"],
        ['Budget', f"{data['metrics']['budget_accuracy']}%"],
        ['People', f"{data['metrics']['people_accuracy']}%"]
    ],
    'footer': ['Overall', f"{data['metrics']['overall_accuracy']}%"],
    'charts': ['bar']
}

# Generate visualizations
viz = TableVisualizer(table)
viz.generate_all('output', 'parser_results')
```

---

### Example 5: LLM-Assisted Table Creation

```python
# Step 1: Get your raw JSON data
raw_data = load_evaluation_results('results.json')

# Step 2: Ask LLM to create table structure
# Prompt: "Convert this JSON to simple table format with 
#          title, headers, and rows"
# 
# LLM returns Python dict:

table = {
    'title': 'Evaluation Results',
    'headers': ['Metric', 'Value', 'Status'],
    'rows': [
        ['Accuracy', '90.5%', 'Good'],
        ['Precision', '88.0%', 'Good'],
        ['Recall', '92.0%', 'Excellent']
    ],
    'charts': ['bar', 'pie']
}

# Step 3: Generate visualizations
viz = TableVisualizer(table)
viz.generate_all('output', 'evaluation_results')
```

---

### Example 6: Individual Output Generation

```python
# Sometimes you want fine-grained control
table = {
    'title': 'My Data',
    'headers': ['Category', 'Value'],
    'rows': [['A', '10'], ['B', '20'], ['C', '30']]
}

viz = TableVisualizer(table)

# Generate only what you need
viz.to_markdown('docs/table.md')           # For documentation
viz.to_csv('data/export.csv')              # For analysis
viz.to_bar_chart('presentation/chart.png') # For slides

# Don't use generate_all() - pick what you need!
```

---

### Example 7: Multiple Chart Types

```python
# Comprehensive visualization
comprehensive_table = {
    'title': 'Monthly Performance',
    'headers': ['Month', 'Accuracy', 'Success Rate', 'Throughput'],
    'rows': [
        ['January', '85%', '90%', '1200'],
        ['February', '88%', '92%', '1400'],
        ['March', '90%', '95%', '1600']
    ],
    'charts': ['bar', 'line']  # Bar for comparison, line for trends
}

viz = TableVisualizer(comprehensive_table)
viz.generate_all('reports', 'monthly_performance')

# Creates both bar and line charts
```

---

### Example 8: Custom Column Selection

```python
# Table with multiple columns
multi_column_table = {
    'title': 'Performance Metrics',
    'headers': ['Field', 'Accuracy', 'Precision', 'Recall'],
    'rows': [
        ['Test 1', '95%', '93%', '97%'],
        ['Test 2', '88%', '85%', '90%']
    ]
}

viz = TableVisualizer(multi_column_table)

# Generate different charts using different columns
viz.to_bar_chart('accuracy.png', x_column=0, y_column=1)   # Accuracy
viz.to_bar_chart('precision.png', x_column=0, y_column=2)  # Precision
viz.to_bar_chart('recall.png', x_column=0, y_column=3)     # Recall

# Or compare multiple metrics in line chart
viz.to_line_chart('comparison.png', x_column=0, y_columns=[1, 2, 3])
```

---

## 📊 Chart Type Guide

### When to Use Bar Charts

**Best for:**
- Comparing values across categories
- Showing performance by field
- Side-by-side comparisons

**Examples:**
- Parser accuracy by field
- Success count by level
- Scores by category

**Code:**
```python
table = {
    'title': 'Comparison',
    'headers': ['Category', 'Score'],
    'rows': [['A', '85'], ['B', '90'], ['C', '78']],
    'charts': ['bar']
}
```

---

### When to Use Pie Charts

**Best for:**
- Showing proportions/percentages
- Part-to-whole relationships
- Distribution visualization

**Examples:**
- Success level distribution (Complete/Partial/Failed)
- Market share
- Budget allocation

**Code:**
```python
table = {
    'title': 'Distribution',
    'headers': ['Level', 'Percentage'],
    'rows': [['Complete', '70%'], ['Partial', '30%']],
    'charts': ['pie']
}
```

**Note:** Pie charts work best with 2-7 categories.

---

### When to Use Line Charts

**Best for:**
- Time series data
- Showing trends
- Comparing multiple metrics over time

**Examples:**
- Accuracy over months
- Performance trends
- Multiple metric comparison

**Code:**
```python
table = {
    'title': 'Trends',
    'headers': ['Month', 'Metric1', 'Metric2'],
    'rows': [['Jan', '80'], ['Feb', '85'], ['Mar', '90']],
    'charts': ['line']
}
```

---

### Chart Combinations

| Data Type | Recommended Charts |
|-----------|-------------------|
| Category comparison | `['bar']` |
| Distribution/proportions | `['bar', 'pie']` |
| Time series | `['line']` |
| Multi-metric comparison | `['bar', 'line']` |
| Comprehensive analysis | `['bar', 'pie', 'line']` |

---

## 🔧 Advanced Features

### Feature 1: Runtime Chart Override

Override table's chart specification when generating:

```python
table = {
    'title': 'Data',
    'headers': ['X', 'Y'],
    'rows': [['A', '10'], ['B', '20']],
    'charts': ['bar']  # Default
}

viz = TableVisualizer(table)

# Use default (bar only)
viz.generate_all('output', 'default')

# Override: generate all types
viz.generate_all('output', 'all', chart_types=['bar', 'pie', 'line'])

# Override: just pie
viz.generate_all('output', 'pie', chart_types=['pie'])
```

---

### Feature 2: Number Parsing

Automatic handling of different number formats:

```python
# Percentages
"95.5%" → 95.5

# Commas
"1,234" → 1234

# Plain numbers
"42" → 42

# Mixed
["95%", "1,234", "42"] → [95, 1234, 42]
```

**Used automatically in all chart generation!**

---

### Feature 3: Markdown Without Saving

Get markdown string without saving to file:

```python
viz = TableVisualizer(table)

# Returns string, doesn't save
md_text = viz.to_markdown()

# Use in your code
print(md_text)
send_to_api(md_text)
process_with_llm(md_text)

# Or save manually
with open('custom_path.md', 'w') as f:
    f.write(md_text)
```

---

### Feature 4: Custom File Organization

```python
viz = TableVisualizer(table)

# Save to different locations
viz.to_markdown('docs/tables/results.md')
viz.to_csv('data/exports/results.csv')
viz.to_bar_chart('presentation/charts/results_bar.png')
viz.to_pie_chart('presentation/charts/results_pie.png')

# Or use generate_all with organized structure
viz.generate_all('reports/2025/december', 'evaluation_results')
```

---

### Feature 5: Programmatic Table Creation

```python
def create_table_from_results(results_file):
    """Convert evaluation results to table"""
    with open(results_file) as f:
        data = json.load(f)
    
    # Build table dynamically
    rows = []
    for field, accuracy in data['metrics'].items():
        rows.append([field.title(), f"{accuracy}%"])
    
    return {
        'title': 'Evaluation Results',
        'headers': ['Field', 'Accuracy'],
        'rows': rows,
        'charts': ['bar']
    }

# Use it
table = create_table_from_results('parser_results.json')
viz = TableVisualizer(table)
viz.generate_all('output', 'auto_generated')
```

---

## 🔍 Troubleshooting

### Issue 1: matplotlib not installed

**Error:**
```
❌ matplotlib not installed. Run: pip install matplotlib
```

**Solution:**
```bash
pip install matplotlib
```

---

### Issue 2: Chart shows zeros

**Problem:** Values appear as zero in chart

**Cause:** Number parsing failed

**Solution:** Check value format
```python
# ❌ Bad (can't parse)
['Field', 'N/A']
['Field', 'None']
['Field', '---']

# ✅ Good
['Field', '0']
['Field', '95%']
['Field', '1,234']
```

---

### Issue 3: Pie chart looks weird

**Problem:** Too many slices, hard to read

**Cause:** Too many categories

**Solution:** Use bar chart instead, or limit categories
```python
# If more than 7 categories, use bar chart
'charts': ['bar']  # Instead of ['pie']
```

---

### Issue 4: File path errors on Windows

**Problem:** `FileNotFoundError` with paths

**Solution:** Use forward slashes or Path
```python
# ✅ Option 1: Forward slashes
viz.to_markdown('output/table.md')

# ✅ Option 2: Use Path
from pathlib import Path
viz.to_markdown(Path('output') / 'table.md')

# ❌ Avoid backslashes without raw strings
viz.to_markdown('output\table.md')  # Wrong!
```

---

### Issue 5: Charts not showing all labels

**Problem:** X-axis labels overlapping or cut off

**Cause:** Too many categories or long labels

**Built-in Solution:** Labels auto-rotate 45° and adjust layout

**Manual Solution:** Edit chart size in code if needed

---

## 📝 Best Practices

### 1. Table Structure

✅ **DO:**
- Keep titles concise and descriptive
- Use clear, short column headers
- Maintain consistent data types per column
- Include footer for totals/summaries

❌ **DON'T:**
- Mix data types in same column
- Use very long column names
- Include raw JSON/complex structures

---

### 2. Chart Selection

✅ **DO:**
- Use bar charts for comparisons (most cases)
- Use pie charts for distributions (2-7 categories)
- Use line charts for trends over time
- Generate multiple chart types for comprehensive view

❌ **DON'T:**
- Use pie charts with 10+ categories
- Use line charts for unordered categories
- Generate charts you won't use

---

### 3. File Organization

✅ **DO:**
```python
# Good structure
viz.generate_all('evaluation/results/tables', 'parser_performance')
viz.generate_all('evaluation/results/charts', 'planner_distribution')
```

❌ **DON'T:**
```python
# Everything in one place
viz.generate_all('.', 'table1')
viz.generate_all('.', 'table2')  # Messy!
```

---

### 4. Naming Conventions

✅ **DO:**
```python
# Clear, descriptive names
viz.generate_all('output', 'parser_accuracy_by_field')
viz.generate_all('output', 'planner_success_distribution')
viz.generate_all('output', 'system_performance_summary')
```

❌ **DON'T:**
```python
# Vague names
viz.generate_all('output', 'table1')
viz.generate_all('output', 'results')
viz.generate_all('output', 'data')
```

---

### 5. LLM Integration

✅ **DO:**
- Use simple, clear table structure
- Ask LLM to generate Python dict directly
- Validate LLM output before using
- Keep table model in prompt

**Example Prompt:**
```
Convert this evaluation data to a table in this format:
{
    'title': 'Table Name',
    'headers': ['Col1', 'Col2'],
    'rows': [['val1', 'val2']],
    'charts': ['bar']
}

Data: [your JSON here]
```

---

### 6. Documentation

✅ **DO:**
```python
# Document your table creation
def create_parser_table(results):
    """
    Create parser performance table
    
    Args:
        results: JSON with parser evaluation results
    
    Returns:
        Table dict with accuracy by field
    """
    return {
        'title': 'Parser Accuracy',
        'headers': ['Field', 'Accuracy'],
        'rows': [...],
        'charts': ['bar']
    }
```

---

### 7. Reusability

✅ **DO:**
```python
# Create reusable transform functions
def evaluation_to_table(json_file, table_type):
    """Generic converter for evaluation results"""
    with open(json_file) as f:
        data = json.load(f)
    
    if table_type == 'parser':
        return create_parser_table(data)
    elif table_type == 'planner':
        return create_planner_table(data)

# Use it
table = evaluation_to_table('results.json', 'parser')
viz = TableVisualizer(table)
viz.generate_all('output', 'results')
```

---

## 📚 Complete Example: End-to-End Workflow

```python
"""
Complete workflow: From evaluation results to visualizations
"""

from helpers.table_visualizer import TableVisualizer
import json

# Step 1: Load evaluation results
with open('evaluation/results/parser_results.json') as f:
    parser_data = json.load(f)

with open('evaluation/results/planner_results.json') as f:
    planner_data = json.load(f)

# Step 2: Create parser table
parser_table = {
    'title': 'Parser Accuracy by Field',
    'headers': ['Field', 'Accuracy %', 'Correct', 'Total'],
    'rows': [
        ['Destination', '98.0', '49', '50'],
        ['Duration', '88.0', '44', '50'],
        ['Budget', '100.0', '50', '50'],
        ['People', '76.0', '38', '50']
    ],
    'footer': ['Overall', '90.5', '181', '200'],
    'charts': ['bar']
}

# Step 3: Create planner table
planner_table = {
    'title': 'Planner Success Distribution',
    'headers': ['Success Level', 'Count', 'Percentage'],
    'rows': [
        ['Complete (5/5)', '21', '70%'],
        ['Partial (3-4/5)', '9', '30%'],
        ['Failed (0-2/5)', '0', '0%']
    ],
    'footer': ['Total', '30', '100%'],
    'charts': ['bar', 'pie']
}

# Step 4: Create system overview table
system_table = {
    'title': 'TIG System Performance Summary',
    'headers': ['Component', 'Metric', 'Score'],
    'rows': [
        ['Parser', 'Overall Accuracy', '90.5%'],
        ['Planner', 'Success Rate', '100%'],
        ['System', 'Complete Rate', '70%']
    ],
    'charts': ['bar']
}

# Step 5: Generate all visualizations
output_dir = 'evaluation/visualizations'

# Parser
parser_viz = TableVisualizer(parser_table)
parser_viz.generate_all(output_dir, 'parser_performance')

# Planner
planner_viz = TableVisualizer(planner_table)
planner_viz.generate_all(output_dir, 'planner_success')

# System
system_viz = TableVisualizer(system_table)
system_viz.generate_all(output_dir, 'system_overview')

print("✓ All visualizations generated!")
print(f"  Location: {output_dir}/")
print("  Files:")
print("    - parser_performance.md/.csv/_bar.png")
print("    - planner_success.md/.csv/_bar.png/_pie.png")
print("    - system_overview.md/.csv/_bar.png")
```

---

## 🎓 Summary

### Key Takeaways

1. **Simple table model** - Easy dict structure
2. **Multiple outputs** - MD, CSV, charts from one table
3. **Flexible chart selection** - Specify in table or override
4. **LLM-friendly** - AI can create table structures
5. **Educational** - Clear, commented, maintainable code

### Quick Reference

```python
# Import
from helpers.table_visualizer import TableVisualizer

# Create table
table = {
    'title': 'My Data',
    'headers': ['Col1', 'Col2'],
    'rows': [['val1', 'val2']],
    'charts': ['bar', 'pie']  # Optional
}

# Generate
viz = TableVisualizer(table)
viz.generate_all('output', 'my_table')
```

### Output Files

```
output/
├── my_table.md          # Markdown table
├── my_table.csv         # CSV file
├── my_table_bar.png     # Bar chart
└── my_table_pie.png     # Pie chart
```

---

## 📞 Questions or Issues?

Check:
1. This guide (VISUALIZATION_HELPER_GUIDE.md)
2. Code comments in `table_visualizer.py`
3. Demo examples at bottom of `table_visualizer.py`

---

**Happy Visualizing! 📊✨**

*Created with ❤️ for the TIG Project - IT_335*
