"""
Test script for offline mode - tests APIs without OpenAI
"""
from offline_main import TourismSystemOffline


def test_offline_examples():
    """Test the offline system with example queries"""
    
    print("=" * 60)
    print("Testing Multi-Agent Tourism System - OFFLINE MODE")
    print("=" * 60)
    
    system = TourismSystemOffline()
    
    # Test place
    place_name = "Bangalore"
    
    # Example 1: Places only
    print("\n" + "=" * 60)
    print("Example 1: Places query")
    print("=" * 60)
    print(f"\nPlace: {place_name}")
    print("Request: Tourist places only")
    print("\nProcessing...")
    response1 = system.process_query(place_name, get_weather=False, get_places=True)
    print(f"\nOutput:\n{response1}")
    
    # Example 2: Weather only
    print("\n" + "=" * 60)
    print("Example 2: Weather query")
    print("=" * 60)
    print(f"\nPlace: {place_name}")
    print("Request: Weather only")
    print("\nProcessing...")
    response2 = system.process_query(place_name, get_weather=True, get_places=False)
    print(f"\nOutput:\n{response2}")
    
    # Example 3: Both weather and places
    print("\n" + "=" * 60)
    print("Example 3: Weather and Places query")
    print("=" * 60)
    print(f"\nPlace: {place_name}")
    print("Request: Both weather and places")
    print("\nProcessing...")
    response3 = system.process_query(place_name, get_weather=True, get_places=True)
    print(f"\nOutput:\n{response3}")
    
    # Test error handling
    print("\n" + "=" * 60)
    print("Example 4: Error handling (non-existent place)")
    print("=" * 60)
    fake_place = "XyzAbc123"
    print(f"\nPlace: {fake_place}")
    print("Request: Tourist places")
    print("\nProcessing...")
    response4 = system.process_query(fake_place, get_weather=False, get_places=True)
    print(f"\nOutput:\n{response4}")
    
    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_offline_examples()

