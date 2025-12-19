import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from agents.query_parser import QueryParser
from agents.planner import ItineraryPlanner
from utils.data_loader import TravelDataSet
from dotenv import load_dotenv

def test_planner():

    print("\n" + "="*60)
    print("SETUP: start")
    print("="*60)


    load_dotenv()


    SECRET_KEY = os.getenv("SECRET_KEY")
    print(f"SECRET_KEY: {SECRET_KEY}")



    # Setup
    dataset = TravelDataSet()
    planner = ItineraryPlanner(dataset)
    parser = QueryParser()

    print("\n" + "="*60)
    print("SETUP: done")
    print("="*60)

    # parse query
    raw_query = "Plan a 5-day trip to Paris with a budget of $1500, inetested in sightseeing and local cuisine."
    structured = parser.parse(raw_query)

    print("\n" + "="*60)
    print(f"PARSED QUERY: {structured}")
    print("="*60)

    # generate itinerary
    itinerary = planner.generate_itinerary(structured, k=3)

        # Print result
    print("\n" + "="*60)
    print("GENERATED ITINERARY")
    print("="*60)
    import json
    print(json.dumps(itinerary, indent=2))

if __name__ == "__main__":
    test_planner()