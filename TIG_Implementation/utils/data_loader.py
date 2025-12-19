"""
Travel planner data loader
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
import json

class TravelDataSet:
    """
    Travel planner data loader handles:
     - loading of data
     - finding similar queries
     - accessing city-specific data
    """
    
    def __init__(self, data_dir: str = "../../TravelPlanner_cleaned"):
        """Initialize dataset loader"""
        print("Loading TravelPlanner dataset...")
        self.data_dir = Path(data_dir)
        print(f"  Data directory: {self.data_dir.absolute()}")
        self.train_df = self._load_train_data()
        self.cities = self._load_cities()
        print(f"✓ Dataset ready: {len(self.train_df)} examples, {len(self.cities)} cities")

    def _load_train_data(self) -> pd.DataFrame:
        """Load training data from CSV file"""
        train_path = self.data_dir / "train_cleaned.csv"
        if not train_path.exists():
            print(f"⚠ Warning: {train_path} not found")
            print("  Creating empty DataFrame for development")
            return pd.DataFrame()
        try:
            df = pd.read_csv(train_path)
            print(f"✓ Loaded {len(df)} training examples")
            return df
        except Exception as e:
            print(f"⚠ Error loading train data: {e}")
            return pd.DataFrame()
    
    def _load_cities(self) -> List[str]:
        """Extract list of available cities from dataset"""
        if self.train_df.empty:
            # Fallback cities for development
            return ["Rome", "Paris", "London", "Tokyo", "New York"]
        
        # Get unique cities from origin and destination columns
        origins = self.train_df['org'].unique().tolist() if 'org' in self.train_df else []
        dests = self.train_df['dest'].unique().tolist() if 'dest' in self.train_df else []
        
        cities = list(set(origins + dests))
        print(f"✓ Found {len(cities)} cities in dataset")
        return cities

    def find_similar_queries(self, query_dict: Dict, k: int = 3) -> List[Dict]:
        """
        Find k most similar queries to the given query
        
        This is RETRIEVAL step from LARA

        Args:
            query_dict: Query dictionary
            k: Number of similar queries to return
        
        Returns:
            List of similar queries
        """
        

        if self.train_df.empty:
            print("⚠ Warning: No training data loaded")
            return []

        print(f"[Retrieval]Finding {k} similar queries from {query_dict}")

        # start with all training examples  
        similar_queries = self.train_df.copy()
        
        # filter by destination
        destination = query_dict.get("destination")
        if destination:
            similar_queries = similar_queries[similar_queries['dest'].str.contains(destination, case=False, na=False)]
            print(f"  Filtered by destination '{destination}': {len(similar_queries)} matches")

        # sort by duration
        duration = query_dict.get("duration")
        if duration and 'days' in similar_queries.columns:
            similar_queries['duration_diff'] = abs(similar_queries['days'] - duration)
            similar_queries = similar_queries.sort_values('duration_diff')  
            print(f"  Sorted by duration similarity (target: {duration} days)")

        # get top k results
        similar_queries = similar_queries.head(k)
        
        # convert list to dictionairies
        # Convert to list of dictionaries
        examples = []
        for idx, row in similar_queries.iterrows():
            example = {
                'query': row.get('query', ''),
                'destination': row.get('dest', ''),
                'duration': row.get('days', 0),
                'budget': row.get('budget', None),
                'plan':  row.get('annotated_plan', None),
            }
            examples.append(example)
            print(f"  ✓ Example {len(examples)}: {example['destination']}, {example['duration']} days")
        
        return examples
    
    def _parse_plan(self, plan_str: Optional[str]) -> Optional[Dict]:
        """Parse plan from string to dictionary"""
        if not plan_str or pd.isna(plan_str):
            return None
        
        try:
            # If it's already a dict, return it
            if isinstance(plan_str, dict):
                return plan_str
            
            # Try to parse as JSON
            return json.loads(plan_str)
        except (json.JSONDecodeError, TypeError):
            # If parsing fails, return None
            return None
    
    def get_city_info(self, city: str) -> Dict:
        """
        Get available options for a city
        
        Args:
            city: City name
            
        Returns:
            Dictionary with hotels, restaurants, attractions
        """
        # TODO: Implement actual database queries
        # For now, return mock data
        return {
            'city': city,
            'hotels': [
                f'{city} Hotel Central',
                f'{city} Grand Hotel',
                f'{city} Budget Inn'
            ],
            'restaurants': [
                f'{city} Traditional Restaurant',
                f'{city} Fine Dining',
                f'{city} Casual Cafe'
            ],
            'attractions': [
                f'{city} Main Museum',
                f'{city} Historic Site',
                f'{city} City Park'
            ]
        }
