"""
Travel Itinerary Generator - Main Orchestrator
Milestone 3 - Simplified Demo Version

This is the main entry point that coordinates:
1. Query Parser (NLU)
2. Itinerary Planner
3. Output formatting

Note: Validator omitted due to time constraints - documented as future work.
"""

import os
import sys
import json
from typing import Dict, Optional
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
notebook_dir = Path.cwd()
print(f"Notebook Dir: {notebook_dir}")

sys.path.insert(0, str(notebook_dir.parent.resolve()))

print(sys.path)

load_dotenv(verbose=True)

from agents.query_parser import QueryParser
from agents.planner import ItineraryPlanner
from utils.data_loader import TravelDataSet


class TIGSystem:
    """
    Travel Itinerary Generator System
    
    Orchestrates the workflow:
    User Query → Parser → Planner → Itinerary
    """
    
    def __init__(self, use_llm: bool = False):
        """
        Initialize TIG system
        
        Args:
            use_llm: Whether to use LLM (requires API keys/Ollama)
                     If False, uses rule-based approaches
        """
        print("\n" + "="*60)
        print("TRAVEL ITINERARY GENERATOR - Initializing")
        print("="*60)
        
        # Initialize components
        print("\n[1/3] Loading Query Parser...")
        self.parser = QueryParser(use_llm=use_llm)
        
        print("\n[2/3] Loading Travel Dataset...")
        self.dataset = TravelDataSet()
        
        print("\n[3/3] Loading Itinerary Planner...")
        # Try to use LLM if requested, otherwise fallback
        try:
            self.planner = ItineraryPlanner(
                self.dataset,
                llm_provider="openai" if use_llm else None,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        except Exception as e:
            print(f"⚠️ LLM initialization failed: {e}")
            print("Using fallback planner...")
            self.planner = ItineraryPlanner(self.dataset)
        
        print("\n" + "="*60)
        print("✓ System Ready")
        print("="*60 + "\n")
    
    def generate_itinerary(self, user_query: str) -> Dict:
        """
        Generate complete itinerary from natural language query
        
        Args:
            user_query: Natural language travel request
            
        Returns:
            Complete itinerary dictionary
        """
        print("\n" + "="*60)
        print("GENERATING ITINERARY")
        print("="*60)
        print(f"Query: {user_query}\n")
        
        try:
            # Step 1: Parse query
            print("[Step 1/2] Parsing query...")
            structured_query = self.parser.parse(user_query)
            
            print("✓ Parsed query:")
            print(f"  Destination: {structured_query.get('destination', 'Unknown')}")
            print(f"  Duration: {structured_query.get('duration', '?')} days")
            print(f"  Budget: ${structured_query.get('budget', 'flexible')}")
            print(f"  People: {structured_query.get('people_number', 1)}")
            
            # Step 2: Generate itinerary
            print("\n[Step 2/2] Generating itinerary...")
            itinerary = self.planner.generate_itinerary(structured_query)

            # Add metadata
            itinerary['query'] = user_query
            itinerary['parsed_query'] = structured_query
            itinerary['generated_at'] = datetime.now().isoformat()
            
            print("✓ Itinerary generated!")
            print(f"  Days: {len(itinerary.get('days', []))}")
            print(f"  Status: {itinerary.get('status', 'success')}")
            
            return itinerary
            
        except Exception as e:
            print(f"\n❌ Error generating itinerary: {e}")
            import traceback
            traceback.print_exc()
            
            # Return error response
            return {
                'error': str(e),
                'query': user_query,
                'status': 'failed'
            }
    
    def print_itinerary(self, itinerary: Dict):
        """Pretty print itinerary"""
        print("\n" + "="*60)
        print("ITINERARY SUMMARY")
        print("="*60)
        
        if 'error' in itinerary:
            print(f"❌ Error: {itinerary['error']}")
            return
        
        # Print header
        query = itinerary.get('parsed_query', {})
        print(f"\nDestination: {query.get('destination', 'Unknown')}")
        print(f"Duration: {query.get('duration', '?')} days")
        print(f"Travelers: {query.get('people_number', 1)} people")
        
        # Print daily breakdown
        days = itinerary.get('days', [])
        print(f"\n{len(days)} Day Itinerary:")
        print("-" * 60)
        
        for day in days:
            day_num = day.get('day', '?')
            date = day.get('date', 'TBD')
            print(f"\nDay {day_num} ({date}):")
            
            # Morning
            if 'morning' in day:
                morning = day['morning']
                print(f"  🌅 Morning ({morning.get('time', '09:00')}): {morning.get('activity', 'Activity')}")
            
            # Lunch
            if 'lunch' in day:
                lunch = day['lunch']
                print(f"  🍽️  Lunch ({lunch.get('time', '13:00')}): {lunch.get('restaurant', 'Restaurant')}")
            
            # Afternoon
            if 'afternoon' in day:
                afternoon = day['afternoon']
                print(f"  ☀️  Afternoon ({afternoon.get('time', '15:00')}): {afternoon.get('activity', 'Activity')}")
            
            # Dinner
            if 'dinner' in day:
                dinner = day['dinner']
                print(f"  🌙 Dinner ({dinner.get('time', '19:00')}): {dinner.get('restaurant', 'Restaurant')}")
            
            # Accommodation
            if 'accommodation' in day:
                print(f"  🏨 Stay: {day['accommodation']}")
        
        # Budget breakdown
        if 'budget_breakdown' in itinerary:
            budget = itinerary['budget_breakdown']
            print("\n" + "-" * 60)
            print("Budget Breakdown:")
            for category, amount in budget.items():
                if category != 'total':
                    print(f"  {category.title()}: ${amount}")
            print(f"  {'='*20}")
            print(f"  Total: ${budget.get('total', 0)}")
        
        print("\n" + "="*60)


def demo():
    """
    Run demo with sample queries
    """
    print("\n" + "="*70)
    print(" "*15 + "TRAVEL ITINERARY GENERATOR DEMO")
    print("="*70)
    
    # Initialize system (use_llm=False for rule-based demo)
    system = TIGSystem(use_llm=True)
    
    # Demo queries
    queries = [
        "Plan a 3-day trip from Orlando to Rome for 2 people with a budget of $2000. We love history and food.",
        "I want to visit Paris for a weekend. Interested in museums and art.",
        "from Nashville 5-day New Orleans adventure for tech enthusiasts, budget $3000"
    ]
    
    results = []
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*70}")
        print(f"DEMO QUERY {i}/{len(queries)}")
        print(f"{'='*70}")
        
        # Generate itinerary
        itinerary = system.generate_itinerary(query)
        
        # Print result
        system.print_itinerary(itinerary)
        
        # Save result
        results.append(itinerary)
        
        # Save to file (JSON)
        output_file = f"data/demo_output_{i}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(itinerary, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Saved to: {output_file}")

        # Save human-readable text version
        txt_file = f"data/demo_output_{i}.txt"
        try:
            from format_output import format_itinerary_to_text
            format_itinerary_to_text(output_file, txt_file)
            print(f"   ✓ Text version: {txt_file}")
        except Exception as e:
            print(f"   ⚠️  Text version: {e}")


    print("\n" + "="*70)
    print(f"✓ Demo completed! Generated {len(results)} itineraries")
    print("="*70 + "\n")


def interactive():
    """
    Interactive mode - user can enter queries
    """
    print("\n" + "="*70)
    print(" "*15 + "TRAVEL ITINERARY GENERATOR - Interactive Mode")
    print("="*70)
    print("\nType your travel query or 'quit' to exit.\n")
    
    # Initialize system
    system = TIGSystem(use_llm=True)
    
    query_count = 0
    
    while True:
        try:
            query = input("\n🌍 Your travel query: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n✈️ Thanks for using Travel Itinerary Generator! Safe travels!")
                break
            
            # Generate itinerary
            itinerary = system.generate_itinerary(query)
            
            # Print result
            system.print_itinerary(itinerary)
            
            # Save result (JSON)
            query_count += 1
            output_file = f"interactive_output_{query_count}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(itinerary, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Saved to: {output_file}")
            
            # Save human-readable text version
            txt_file = f"interactive_output_{query_count}.txt"
            try:
                from format_output import format_itinerary_to_text
                format_itinerary_to_text(output_file, txt_file)
                print(f"   ✓ Text version: {txt_file}")
            except Exception as e:
                print(f"   ⚠️  Text version: {e}")

        except KeyboardInterrupt:
            print("\n\n✈️ Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


def main():
    """
    Main entry point with menu
    """
    print("\n" + "="*70)
    print(" "*20 + "TRAVEL ITINERARY GENERATOR")
    print(" "*25 + "Milestone 3 Demo")
    print("="*70)
    
    print("\nSelect mode:")
    print("1. Demo mode (run 3 example queries)")
    print("2. Interactive mode (enter your own queries)")
    print("3. Exit")
    
    choice = input("\nYour choice (1-3): ").strip()
    
    if choice == "1":
        demo()
    elif choice == "2":
        interactive()
    elif choice == "3":
        print("\n✈️ Goodbye!")
    else:
        print("\n❌ Invalid choice. Exiting.")


if __name__ == "__main__":
    main()
