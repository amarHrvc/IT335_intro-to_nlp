"""
Test TravelPlanner Dataset Loader
Run: python -m tests.test_data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import TravelDataSet

def test_dataset_loading():
    """Test basic dataset loading"""
    print("\n" + "="*60)
    print("TEST 1: Dataset Loading")
    print("="*60)
    
    dataset = TravelDataSet()
    
    print(f"\nDataset loaded successfully!")
    print(f"  Training examples: {len(dataset.train_df)}")
    print(f"  Available cities: {len(dataset.cities)}")
    print(f"  Sample cities: {dataset.cities[:5]}")

def test_retrieval():
    """Test query retrieval"""
    print("\n" + "="*60)
    print("TEST 2: Query Retrieval")
    print("="*60)
    
    dataset = TravelDataSet()
    
    # Test query
    query = {
        'destination': 'New York',
        'duration': 3,
        'budget': 2000
    }
    
    print(f"\nSearching for queries similar to: {query}")
    examples = dataset.find_similar_queries(query, k=3)
    
    print(f"\nFound {len(examples)} similar queries:")
    for i, ex in enumerate(examples, 1):
        print(f"\n  Example {i}:")
        print(f"    Query: {ex['query'][:60]}...")
        print(f"    Destination: {ex['destination']}")
        print(f"    Duration: {ex['duration']} days")
        print(f"    Has plan: {ex['plan'] is not None}")

def test_city_info():
    """Test city information retrieval"""
    print("\n" + "="*60)
    print("TEST 3: City Information")
    print("="*60)
    
    dataset = TravelDataSet()
    
    city = "New York"
    info = dataset.get_city_info(city)
    
    print(f"\nInformation for {city}:")
    print(f"  Hotels: {len(info['hotels'])}")
    print(f"  Restaurants: {len(info['restaurants'])}")
    print(f"  Attractions: {len(info['attractions'])}")
    
    print(f"\n  Sample hotels:")
    for hotel in info['hotels'][:3]:
        print(f"    - {hotel}")

if __name__ == "__main__":
    test_dataset_loading()
    test_retrieval()
    test_city_info()
    
    print("\n" + "="*60)
    print("✓ All tests completed!")
    print("="*60)