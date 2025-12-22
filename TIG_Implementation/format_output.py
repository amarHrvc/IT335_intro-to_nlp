#!/usr/bin/env python3
"""
Format TIG JSON output to human-readable text
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def format_itinerary_to_text(json_file: str, output_file: str = None):
    """
    Convert JSON itinerary to human-readable text format.
    
    Args:
        json_file: Path to JSON file
        output_file: Optional output file path (defaults to .txt version)
    """
    # Read JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Parse nested JSON string if present
    if isinstance(data.get('itinerary'), str):
        itinerary_str = data['itinerary']
        
        # Strip markdown code blocks if present (defense in depth)
        if itinerary_str.strip().startswith("```"):
            itinerary_str = itinerary_str.strip()
            
            # Remove opening markdown
            if itinerary_str.startswith("```json"):
                itinerary_str = itinerary_str[7:]
            elif itinerary_str.startswith("```"):
                itinerary_str = itinerary_str[3:]
            
            # Remove closing markdown
            if itinerary_str.endswith("```"):
                itinerary_str = itinerary_str[:-3]
            
            itinerary_str = itinerary_str.strip()
        
        # Parse JSON
        itinerary = json.loads(itinerary_str)
        
        # Handle nested "Itinerary" key that OpenAI sometimes adds
        if "Itinerary" in itinerary and isinstance(itinerary["Itinerary"], dict):
            itinerary = itinerary["Itinerary"]
    else:
        itinerary = data.get('itinerary', {})
    
    # Build formatted output
    lines = []
    lines.append("=" * 70)
    lines.append("TRAVEL ITINERARY")
    lines.append("=" * 70)
    lines.append("")
    
    # Query information
    if 'query' in data:
        lines.append(f"Original Query: {data['query']}")
        lines.append("")
    
    # Parsed query details
    if 'parsed_query' in data:
        pq = data['parsed_query']
        lines.append("Trip Details:")
        lines.append(f"  • Destination: {pq.get('destination', 'N/A')}")
        lines.append(f"  • Duration: {pq.get('duration', 'N/A')} days")
        lines.append(f"  • Budget: ${pq.get('budget', 'N/A')}")
        lines.append(f"  • Number of People: {pq.get('people_number', 'N/A')}")
        if pq.get('interests'):
            lines.append(f"  • Interests: {', '.join(pq['interests'])}")
        lines.append("")
    
    # Generation timestamp
    if 'generated_at' in data:
        try:
            dt = datetime.fromisoformat(data['generated_at'])
            lines.append(f"Generated: {dt.strftime('%B %d, %Y at %I:%M %p')}")
        except:
            lines.append(f"Generated: {data['generated_at']}")
        lines.append("")
    
    lines.append("=" * 70)
    lines.append("")
    
    # Itinerary by day
    for day_key in sorted([k for k in itinerary.keys() if k.startswith('Day')], 
                          key=lambda x: int(x.split()[1])):
        day_num = day_key.split()[1]
        lines.append(f"{'─' * 70}")
        lines.append(f"DAY {day_num}")
        lines.append(f"{'─' * 70}")
        lines.append("")
        
        day_data = itinerary[day_key]
        
        # Handle different formats
        if isinstance(day_data, dict):
            # Time-based format (Morning, Afternoon, Evening)
            for time_period in ['Morning', 'Afternoon', 'Evening', 'Lunch', 'Dinner']:
                if time_period in day_data:
                    lines.append(f"🕐 {time_period.upper()}")
                    period_data = day_data[time_period]
                    
                    if isinstance(period_data, dict):
                        if 'Activity' in period_data:
                            lines.append(f"   📍 Activity: {period_data['Activity']}")
                        if 'Meal' in period_data:
                            lines.append(f"   🍽️  Meal: {period_data['Meal']}")
                        if 'Accommodation' in period_data:
                            lines.append(f"   🏨 {period_data['Accommodation']}")
                        
                        # Handle other keys
                        for key, value in period_data.items():
                            if key not in ['Activity', 'Meal', 'Accommodation']:
                                lines.append(f"   • {key}: {value}")
                    else:
                        lines.append(f"   {period_data}")
                    lines.append("")

            if 'Accommodation' in day_data:
                lines.append(f"🏨 ACCOMMODATION")
                lines.append(f"   {day_data['Accommodation']}")
                lines.append("")

            
            # Activity-based format (Activity 1, Activity 2, etc.)
            activities = sorted([k for k in day_data.keys() if k.startswith('Activity')],
                              key=lambda x: int(x.split()[1]) if len(x.split()) > 1 else 0)
            for activity_key in activities:
                activity = day_data[activity_key]
                if isinstance(activity, dict):
                    lines.append(f"📍 {activity.get('Title', 'Activity')}")
                    if 'Description' in activity:
                        lines.append(f"   {activity['Description']}")
                    if 'Cost' in activity:
                        lines.append(f"   💰 Cost: {activity['Cost']}")
                    if 'Duration' in activity:
                        lines.append(f"   ⏱️  Duration: {activity['Duration']}")
                    lines.append("")
            
            # Meals
            meals = sorted([k for k in day_data.keys() if k.startswith('Meal')],
                          key=lambda x: int(x.split()[1]) if len(x.split()) > 1 else 0)
            for meal_key in meals:
                meal = day_data[meal_key]
                if isinstance(meal, dict):
                    lines.append(f"🍽️  {meal.get('Title', 'Meal')}")
                    if 'Description' in meal:
                        lines.append(f"   {meal['Description']}")
                    if 'Cost' in meal:
                        lines.append(f"   💰 Cost: {meal['Cost']}")
                    lines.append("")
        
        lines.append("")
    
    # Budget summary
    budget_keys = ['Total Budget', 'Total Spent', 'Remaining Balance', 'Total Cost']
    has_budget = any(k in itinerary for k in budget_keys)
    
    if has_budget:
        lines.append("=" * 70)
        lines.append("BUDGET SUMMARY")
        lines.append("=" * 70)
        for key in budget_keys:
            if key in itinerary:
                lines.append(f"  {key}: {itinerary[key]}")
        lines.append("")
    
    # Write output
    output_text = '\n'.join(lines)
    
    if output_file is None:
        output_file = json_file.replace('.json', '.txt')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_text)
    
    print(f"✓ Formatted itinerary saved to: {output_file}")
    print(f"\nPreview (first 30 lines):")
    print("-" * 70)
    for i, line in enumerate(lines[:30]):
        print(line)
    if len(lines) > 30:
        print(f"\n... ({len(lines) - 30} more lines in file)")
    
    return output_text


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python format_output.py <json_file> [output_file]")
        print("\nFormatting all demo outputs...")
        
        # Format all demo outputs
        for i in range(1, 4):
            json_file = f"demo_output_{i}.json"
            if Path(json_file).exists():
                print(f"\n{'='*70}")
                print(f"Processing {json_file}...")
                print('='*70)
                format_itinerary_to_text(json_file)
            else:
                print(f"⚠️  {json_file} not found")
    else:
        json_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        format_itinerary_to_text(json_file, output_file)
