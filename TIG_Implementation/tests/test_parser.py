"""
Test Query Parser
Run: python -m tests.test_parser

Usage:
    To run these tests, execute the following command from the TIG_Implementation directory:
    python -m tests.test_parser
    
    Ensure you have the required dependencies installed:
    pip install spacy openai python-dotenv
    python -m spacy download en_core_web_sm
"""

import sys
import os

# Add parent directory to path so we can import agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.query_parser import QueryParser

def test_basic_queries():
    """Test with simple queries"""
    
    print("\nTesting Basic Queries (Rule-based)...")
    # Force rule-based for basic test by not providing API key or setting use_llm=False
    # But here we just instantiate default, if no env var it falls back to rules
    parser = QueryParser(use_llm=False)
    
    # Test cases
    queries = [
        "Plan a 3-day trip to Rome for $2000",
        "I want to visit Paris for 5 days with a budget of 1500 euros",
        "7-day trip to Tokyo, interested in sightseeing and food",
        "Trip from New York to London, 4 days, $3000"
    ]
    
    for query in queries:
        result = parser.parse(query)
        valid, missing = parser.validate_query(result)
        
        print(f"\n{'='*60}")
        print(f"Valid: {valid}")
        if not valid:
            print(f"Missing: {missing}")
        print(f"{'='*60}\n")

def test_with_llm():
    """Test with LLM enabled"""
    print("\nTesting with LLM...")
    
    # Check if API key is present
    from dotenv import load_dotenv
    load_dotenv()
    if not os.getenv('OPENAI_API_KEY'):
        print("SKIPPING LLM TEST: No OPENAI_API_KEY found in .env")
        return

    parser = QueryParser(use_llm=True)
    
    # Try a more complex query
    query = "I'm traveling from Boston to Barcelona with my family (4 people) for a week. Budget is around 5000 euros. We love museums and food."
    
    result = parser.parse(query)
    print(f"\nFinal result: {result}")

if __name__ == "__main__":
    test_basic_queries()
    test_with_llm()
