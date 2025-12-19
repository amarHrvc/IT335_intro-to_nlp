"""
Table-First Visualization System

Core concept: Everything is a table!
1. Define simple table structure
2. Generate any visualization from it

Usage:
    # Define your table
    table = {
        'title': 'My Results',
        'headers': ['Name', 'Score'],
        'rows': [['Test 1', '95'], ['Test 2', '87']]
    }

    # Generate everything
    viz = TableVisualizer(table)
    viz.to_markdown('output.md')
    viz.to_csv('output.csv')
    viz.to_bar_chart('output.png')
"""

import csv
import json
from pathlib import Path


class TableVisualizer:
    """
    Simple table-based visualization generator

    Table format:
    {
        'title': 'Table Title',
        'headers': ['Col1', 'Col2', 'Col3'],
        'rows': [
            ['val1', 'val2', 'val3'],
            ['val4', 'val5', 'val6']
        ],
        'footer': ['Total', '100', '200'],  # Optional
        'charts': ['bar', 'pie']  # Optional: which charts to generate
    }
    
    Chart types:
    - 'bar': Bar chart (comparing categories)
    - 'pie': Pie chart (showing proportions)
    - 'line': Line chart (showing trends)
    """

    def __init__(self, table_data):
        """
        Initialize with table data

        Args:
            table_data: Dictionary with title, headers, rows, optional footer, optional charts
        """
        self.title = table_data.get('title', 'Untitled Table')
        self.headers = table_data.get('headers', [])
        self.rows = table_data.get('rows', [])
        self.footer = table_data.get('footer', None)
        self.charts = table_data.get('charts', ['bar'])  # Default to bar chart

    def to_markdown(self, output_path=None):
        """
        Generate Markdown table

        Perfect for:
        - Documentation
        - LLM analysis (easy to read)
        - Quick reports

        Returns markdown string, optionally saves to file
        """
        lines = []

        # Title
        lines.append(f"## {self.title}\n")

        # Headers
        header_line = "| " + " | ".join(self.headers) + " |"
        separator = "|" + "|".join([" --- " for _ in self.headers]) + "|"

        lines.append(header_line)
        lines.append(separator)

        # Rows
        for row in self.rows:
            row_line = "| " + " | ".join(str(cell) for cell in row) + " |"
            lines.append(row_line)

        # Footer (if present)
        if self.footer:
            lines.append(separator)
            footer_line = "| " + " | ".join(str(cell) for cell in self.footer) + " |"
            lines.append(footer_line)

        markdown = "\n".join(lines)

        # Save if path provided
        if output_path:
            Path(output_path).write_text(markdown, encoding='utf-8')
            print(f"✓ Markdown saved: {output_path}")

        return markdown

    def to_csv(self, output_path):
        """
        Generate CSV file

        Perfect for:
        - Excel import
        - Data analysis
        - Archival
        """
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Write headers
            writer.writerow(self.headers)

            # Write rows
            writer.writerows(self.rows)

            # Write footer if present
            if self.footer:
                writer.writerow(self.footer)

        print(f"✓ CSV saved: {output_path}")

    def to_bar_chart(self, output_path, x_column=0, y_column=1):
        """
        Generate bar chart from table

        Args:
            output_path: Where to save PNG
            x_column: Index of column for X-axis (default: 0)
            y_column: Index of column for Y-axis (default: 1)

        Example:
            Table with ['Field', 'Accuracy'] headers
            x_column=0 (Field names)
            y_column=1 (Accuracy values)
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("❌ matplotlib not installed. Run: pip install matplotlib")
            return

        # Extract data
        x_data = [row[x_column] for row in self.rows]
        y_data = [self._parse_number(row[y_column]) for row in self.rows]

        # Create chart
        plt.figure(figsize=(10, 6))
        plt.bar(x_data, y_data)
        plt.xlabel(self.headers[x_column])
        plt.ylabel(self.headers[y_column])
        plt.title(self.title)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Save
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ Bar chart saved: {output_path}")

    def to_pie_chart(self, output_path, label_column=0, value_column=1):
        """
        Generate pie chart from table

        Perfect for: Showing proportions/percentages
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("❌ matplotlib not installed. Run: pip install matplotlib")
            return

        # Extract data
        labels = [row[label_column] for row in self.rows]
        values = [self._parse_number(row[value_column]) for row in self.rows]

        # Create chart
        plt.figure(figsize=(8, 8))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title(self.title)
        plt.axis('equal')

        # Save
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ Pie chart saved: {output_path}")

    def to_line_chart(self, output_path, x_column=0, y_columns=[1]):
        """
        Generate line chart from table

        Args:
            y_columns: List of column indices to plot (can plot multiple lines)

        Perfect for: Trends over time or categories
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("❌ matplotlib not installed. Run: pip install matplotlib")
            return

        # Extract data
        x_data = [row[x_column] for row in self.rows]

        # Create chart
        plt.figure(figsize=(10, 6))

        for y_col in y_columns:
            y_data = [self._parse_number(row[y_col]) for row in self.rows]
            plt.plot(x_data, y_data, marker='o', label=self.headers[y_col])

        plt.xlabel(self.headers[x_column])
        plt.ylabel('Value')
        plt.title(self.title)
        plt.legend()
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Save
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ Line chart saved: {output_path}")

    def _parse_number(self, value):
        """
        Parse number from string

        Handles:
        - Percentages: "95.5%" → 95.5
        - Numbers with commas: "1,234" → 1234
        - Plain numbers: "42" → 42
        """
        if isinstance(value, (int, float)):
            return value

        # Remove %, commas, spaces
        cleaned = str(value).replace('%', '').replace(',', '').strip()

        try:
            return float(cleaned)
        except ValueError:
            return 0

    def generate_all(self, output_dir, basename, chart_types=None):
        """
        Generate all visualization types

        Args:
            output_dir: Directory to save files
            basename: Base name for files (e.g., 'parser_performance')
            chart_types: Optional list of chart types to override table's charts setting
                        Options: 'bar', 'pie', 'line'
                        If None, uses self.charts from table data

        Creates:
            - basename.md (Markdown - always)
            - basename.csv (CSV - always)
            - basename_bar.png (if 'bar' in charts)
            - basename_pie.png (if 'pie' in charts)
            - basename_line.png (if 'line' in charts)
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Use provided chart_types or fall back to table's charts setting
        charts_to_generate = chart_types if chart_types is not None else self.charts

        # Always generate markdown and CSV
        self.to_markdown(output_dir / f"{basename}.md")
        self.to_csv(output_dir / f"{basename}.csv")

        # Generate requested chart types
        generated_charts = []
        
        if 'bar' in charts_to_generate:
            self.to_bar_chart(output_dir / f"{basename}_bar.png")
            generated_charts.append('bar')

        if 'pie' in charts_to_generate:
            self.to_pie_chart(output_dir / f"{basename}_pie.png")
            generated_charts.append('pie')

        if 'line' in charts_to_generate:
            self.to_line_chart(output_dir / f"{basename}_line.png")
            generated_charts.append('line')

        print(f"\n✓ Generated: MD, CSV, {', '.join(generated_charts)} chart(s) in {output_dir}/")


# Example usage helper
def from_json(json_file, transform_func):
    """
    Helper to convert JSON to table structure

    Args:
        json_file: Path to JSON results file
        transform_func: Function that converts JSON → table dict

    Returns:
        TableVisualizer instance
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    table_data = transform_func(data)
    return TableVisualizer(table_data)


if __name__ == "__main__":
    # Quick demo - Example 1: Bar chart only (default)
    demo_table_1 = {
        'title': 'Parser Performance',
        'headers': ['Field', 'Accuracy', 'Correct', 'Total'],
        'rows': [
            ['Destination', '98.0%', '49', '50'],
            ['Duration', '88.0%', '44', '50'],
            ['Budget', '100.0%', '50', '50'],
            ['People', '76.0%', '38', '50']
        ],
        'footer': ['Overall', '90.5%', '181', '200'],
        'charts': ['bar']  # Specify chart type in table!
    }

    viz1 = TableVisualizer(demo_table_1)
    viz1.generate_all('demo_output', 'parser_performance')

    # Example 2: Bar + Pie charts
    # demo_table_2 = {
    #     'title': 'Planner Success Distribution',
    #     'headers': ['Level', 'Count', 'Percentage'],
    #     'rows': [
    #         ['Complete', '21', '70%'],
    #         ['Partial', '9', '30%'],
    #         ['Failed', '0', '0%']
    #     ],
    #     'charts': ['bar', 'pie']  # Generate both!
    # }
    #
    # viz2 = TableVisualizer(demo_table_2)
    # viz2.generate_all('demo_output', 'planner_distribution')

    table_20251208_004748 = {
        "title": "Planner Performance (2025-12-08 00:47:48)",
        "headers": ["Level", "Accuracy", "Count", "Total"],
        "rows": [
            ["Complete", "92.0%", 46, 50],
            ["Partial", "8.0%", 4, 50],
            ["Failed", "0.0%", 0, 50],
        ],
        "footer": ["Overall Success", "100.0%", 50, 50],
        "charts": ["bar", "pie"]
    }
    viz1 = TableVisualizer(table_20251208_004748)
    viz1.generate_all('demo_output', 'parser_performance')

    # Example 3: Override chart types
    # viz1.generate_all('demo_output', 'parser_all_types', chart_types=['bar', 'pie', 'line'])