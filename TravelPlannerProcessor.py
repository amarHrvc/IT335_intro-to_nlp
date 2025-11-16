"""
TravelPlanner Dataset Preprocessing Script
Normalizes and cleans the TravelPlanner dataset for downstream processing.
"""
import pandas as pd
import re
from datetime import datetime
import os

class TravelPlannerProcessor:
    """Preprocessor for TravelPlanner dataset"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.date_format = "%Y-%m-%d"
    
    @staticmethod
    def normalize_text(text):
        """Lowercase and remove special characters from text"""
        if pd.isna(text):
            return ""
        
        text = str(text).lower()
        # Remove white spaces
        text = text.strip()
        # Remove special characters
        text = re.sub(r'[^a-z0-9\s]', '', text)
        return text
    
    @staticmethod
    def normalize_cities(city):
        """Normalize city names"""
        if pd.isna(city):
            return "unknown"
            
        city = str(city).lower().strip().title()
        return city if city else "unknown"
    
    def parse_date(self, date_str):
        """Parse date string to datetime object"""
        if pd.isna(date_str):
            return None
        
        try:
            return datetime.strptime(str(date_str), self.date_format)
        except ValueError:
            return str(date_str)  # return as is if parsing fails
            
    def preprocess_data_frame(self, df, split_name='unknown'):
        """Preprocess data frame"""
        print(f"Preprocessing {split_name} data frame with {len(df)} records.")
        df_clean = df.copy()

        # Normalize text fields
        if 'query' in df_clean.columns:
            df_clean['query_normalized'] = df_clean['query'].apply(self.normalize_text)
            df_clean['query_length_words'] = df_clean['query'].str.split().str.len()
            df_clean['query_length_chars'] = df_clean['query'].str.len()

        # Normalize city names
        city_fields = ['org', 'dest']
        for field in city_fields:
            if field in df_clean.columns:
                df_clean[field+'_normalized'] = df_clean[field].apply(self.normalize_cities)

        # Parse date fields
        date_fields = ['start_date', 'end_date']
        for field in date_fields:
            if field in df_clean.columns:
                df_clean[field+'_normalized'] = df_clean[field].apply(self.parse_date)

        # Handle missing values
        df_clean.fillna({
            'title': 'unknown',
            'description': 'no description',
            'org': 'unknown',
            'dest': 'unknown',
            'people_number': 1,
            'level': 'easy',
            'days': 1
        }, inplace=True)

        # Add metadata about the split
        df_clean['data_split'] = split_name
        print(f"Completed preprocessing {split_name} data frame.")
        print(f"Columns after preprocessing: {df_clean.columns.tolist()}")
        print(f"Row count after preprocessing: {len(df_clean)}")
        return df_clean
        
    def save_cleaned_data(self, df, output_path):
        """Save cleaned data to CSV"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Saved cleaned data to {output_path}")


def main():
    """Main function to run the preprocessing pipeline"""
    print("="*60)
    print("TravelPlanner Dataset Preprocessing Pipeline")
    print("="*60)
    
    # Initialize preprocessor
    filepath = "TravelPlanner"  # Default path to data directory
    processor = TravelPlannerProcessor(filepath=filepath)

    # Create output directory
    os.makedirs('TravelPlanner_cleaned', exist_ok=True)

    # Process each data split
    for split in ['train', 'validation', 'test']:
        print(f"\nProcessing {split} data...")
        df = pd.read_csv(os.path.join(filepath, f"{split}.csv"))
        df_clean = processor.preprocess_data_frame(df, split_name=split)
        output_path = os.path.join('TravelPlanner_cleaned', f"{split}_cleaned.csv")
        processor.save_cleaned_data(df_clean, output_path)

if __name__ == "__main__":
    main()