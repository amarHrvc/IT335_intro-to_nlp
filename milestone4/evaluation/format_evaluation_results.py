"""
Format Planner Evaluation Results to Human-Readable Text

Creates detailed TXT files showing:
- Query and parsed query
- LLM prompt (truncated if long)
- Raw LLM response
- Processed response
- Each criterion check with pass/fail
- Failure reasons
- Final verdict
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def format_single_result(result: dict, index: int) -> str:
    """
    Format a single evaluation result to readable text

    Args:
        result: Dictionary with evaluation data
        index: Query number

    Returns:
        Formatted string
    """
    lines = []

    # Header
    lines.append("=" * 80)
    lines.append(f"QUERY #{index}")
    lines.append("=" * 80)
    lines.append("")

    # Query details
    query = result.get('query', {})
    lines.append("📋 QUERY DETAILS:")
    lines.append(f"   Destination: {query.get('destination', 'N/A')}")
    lines.append(f"   Duration: {query.get('duration', 'N/A')} days")
    lines.append(f"   Budget: ${query.get('budget', 'N/A')}")
    lines.append(f"   People: {query.get('people_number', 'N/A')}")
    lines.append("")

    # Debug info (if available)
    debug_info = result.get('debug_info')
    if debug_info:
        lines.append("-" * 80)
        lines.append("🔍 DEBUG INFORMATION:")
        lines.append("-" * 80)
        lines.append("")

        # LLM Prompt (FULL - no truncation for debugging)
        prompt = debug_info.get('prompt', '')
        lines.append("📤 LLM PROMPT:")
        lines.append("-" * 80)
        lines.append(prompt)
        lines.append("")
        lines.append(f"(Length: {len(prompt)} chars)")
        lines.append("")

        # Raw LLM Response (FULL - no truncation for debugging)
        raw_response = debug_info.get('raw_response', '')
        lines.append("📥 RAW LLM RESPONSE:")
        lines.append("-" * 80)
        lines.append(raw_response)
        lines.append("")
        lines.append(f"(Length: {len(raw_response)} chars)")
        lines.append("")

        # Processed Response (FULL - no truncation for debugging)
        processed = debug_info.get('processed_response', '')
        lines.append("⚙️  PROCESSED RESPONSE:")
        lines.append("-" * 80)
        lines.append(processed)
        lines.append("")
        lines.append(f"(Length: {len(processed)} chars)")
        lines.append("")

    # Criteria evaluation
    lines.append("-" * 80)
    lines.append("✅ CRITERIA EVALUATION:")
    lines.append("-" * 80)
    lines.append("")

    criteria = result.get('criteria', {})
    criteria_names = {
        'generated': '1. Itinerary Generated',
        'days': '2. Correct Number of Days',
        'budget': '3. Within Budget',
        'people': '4. Correct People Count',
        'destination': '5. Contains Destination'
    }

    for key, name in criteria_names.items():
        status = "✓ PASS" if criteria.get(key, False) else "✗ FAIL"
        lines.append(f"   {name}: {status}")

    lines.append("")
    lines.append(f"   Total: {result.get('count', 0)}/5 criteria met")
    lines.append("")

    # Failure reasons
    failure_reasons = result.get('failure_reasons', [])
    if failure_reasons:
        lines.append("-" * 80)
        lines.append("❌ FAILURE REASONS:")
        lines.append("-" * 80)
        lines.append("")
        for reason in failure_reasons:
            lines.append(f"   • {reason}")
        lines.append("")

    # Final verdict
    level = result.get('level', 'unknown')
    level_icons = {
        'complete': '🎉',
        'partial': '⚠️',
        'failed': '❌'
    }
    icon = level_icons.get(level, '❓')

    lines.append("-" * 80)
    lines.append(f"📊 FINAL VERDICT: {icon} {level.upper()}")
    lines.append("-" * 80)
    lines.append("")
    lines.append("")

    return "\n".join(lines)


def format_evaluation_results(json_file: str, output_file: str = None):
    """
    Format evaluation results JSON to detailed text file

    Args:
        json_file: Path to planner_results_*.json
        output_file: Optional output file (defaults to *_detailed.txt)
    """
    # Read JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Default output file
    if output_file is None:
        output_file = json_file.replace('.json', '_detailed.txt')

    # Build output
    lines = []

    # Header
    lines.append("=" * 80)
    lines.append("PLANNER EVALUATION - DETAILED DEBUG REPORT")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    lines.append("")

    # Summary
    lines.append("📊 SUMMARY:")
    lines.append(f"   Total Queries: {data.get('total', 0)}")
    lines.append(f"   Complete (5/5): {data.get('complete', 0)}")
    lines.append(f"   Partial (3-4/5): {data.get('partial', 0)}")
    lines.append(f"   Failed (0-2/5): {data.get('failed', 0)}")
    lines.append("")
    lines.append("")

    # Individual results
    details = data.get('details', [])
    for i, result in enumerate(details, 1):
        lines.append(format_single_result(result, i))

    # Write to file
    output_text = "\n".join(lines)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_text)

    print(f"✓ Detailed report saved to: {output_file}")
    return output_file


def main():
    """Main function for command-line usage"""
    if len(sys.argv) < 2:
        print("Usage: python format_evaluation_results.py <planner_results.json>")
        sys.exit(1)

    json_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    format_evaluation_results(json_file, output_file)


if __name__ == "__main__":
    main()