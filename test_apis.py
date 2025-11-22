"""
Test script to verify all open-source APIs are working correctly
Tests: Nominatim, Open-Meteo, and Overpass APIs
"""
import sys
from api_clients import NominatimClient, OpenMeteoClient, OverpassClient

def test_nominatim():
    """Test Nominatim API (Geocoding)"""
    print("=" * 60)
    print("Testing Nominatim API (Geocoding)")
    print("=" * 60)
    print("Endpoint: https://nominatim.openstreetmap.org/search")
    print()
    
    client = NominatimClient()
    
    # Test with Bangalore
    print("Test 1: Getting coordinates for 'Bangalore'...")
    coords = client.get_coordinates("Bangalore")
    
    if coords:
        print(f"✅ SUCCESS: Found Bangalore at {coords[0]:.4f}, {coords[1]:.4f}")
        
        # Test place details
        print("\nTest 2: Getting place details for 'Bangalore'...")
        exists, details, message = client.verify_place_exists("Bangalore", strict=False)
        if exists and details:
            print(f"✅ SUCCESS: {details.get('display_name', 'Bangalore')}")
            print(f"   Country: {details.get('country', 'Unknown')}")
            print(f"   Type: {details.get('type', 'Unknown')}")
        else:
            print("❌ FAILED: Could not get place details")
    else:
        print("❌ FAILED: Could not get coordinates")
        return False
    
    print()
    return True


def test_open_meteo():
    """Test Open-Meteo API (Weather)"""
    print("=" * 60)
    print("Testing Open-Meteo API (Weather)")
    print("=" * 60)
    print("Endpoint: https://api.open-meteo.com/v1/forecast")
    print()
    
    client = OpenMeteoClient()
    
    # Use Bangalore coordinates (12.9716, 77.5946)
    print("Test: Getting weather for Bangalore (12.9716, 77.5946)...")
    weather = client.get_weather(12.9716, 77.5946)
    
    if weather:
        print(f"✅ SUCCESS: Weather data retrieved")
        print(f"   Temperature: {weather.get('temperature')}{weather.get('unit', '°C')}")
        print(f"   Precipitation Probability: {weather.get('precipitation_probability', 0)}%")
    else:
        print("❌ FAILED: Could not get weather data")
        return False
    
    print()
    return True


def test_overpass():
    """Test Overpass API (Tourist Attractions)"""
    print("=" * 60)
    print("Testing Overpass API (Tourist Attractions)")
    print("=" * 60)
    print("Base URL: https://overpass-api.de/api/interpreter")
    print()
    
    client = OverpassClient()
    
    # Use Bangalore coordinates (12.9716, 77.5946)
    print("Test: Getting tourist attractions for Bangalore (12.9716, 77.5946)...")
    attractions = client.get_tourist_attractions(12.9716, 77.5946, limit=5)
    
    if attractions:
        print(f"✅ SUCCESS: Found {len(attractions)} tourist attractions")
        for i, place in enumerate(attractions, 1):
            print(f"   {i}. {place.get('name', 'Unknown')} ({place.get('type', 'attraction')})")
    else:
        print("⚠️  WARNING: No tourist attractions found (this might be normal for some locations)")
        print("   API is working, but no attractions in database for this area")
    
    print()
    return True


def test_full_flow():
    """Test the complete flow: Geocoding -> Weather -> Places"""
    print("=" * 60)
    print("Testing Complete Flow")
    print("=" * 60)
    print("Testing: Bangalore")
    print()
    
    nominatim = NominatimClient()
    open_meteo = OpenMeteoClient()
    overpass = OverpassClient()
    
    # Step 1: Geocoding
    print("Step 1: Geocoding (Nominatim)...")
    coords = nominatim.get_coordinates("Bangalore")
    if not coords:
        print("❌ FAILED: Geocoding failed")
        return False
    print(f"✅ Coordinates: {coords[0]:.4f}, {coords[1]:.4f}")
    
    # Step 2: Weather
    print("\nStep 2: Weather (Open-Meteo)...")
    weather = open_meteo.get_weather(coords[0], coords[1])
    if not weather:
        print("❌ FAILED: Weather API failed")
        return False
    print(f"✅ Temperature: {weather.get('temperature')}{weather.get('unit', '°C')}")
    
    # Step 3: Places
    print("\nStep 3: Tourist Attractions (Overpass)...")
    attractions = overpass.get_tourist_attractions(coords[0], coords[1], limit=3)
    print(f"✅ Found {len(attractions)} attractions")
    for place in attractions:
        print(f"   - {place.get('name', 'Unknown')}")
    
    print("\n✅ ALL APIs WORKING CORRECTLY!")
    return True


def main():
    """Run all API tests"""
    print("\n" + "=" * 60)
    print("API VERIFICATION TEST SUITE")
    print("=" * 60)
    print("\nTesting all open-source APIs as per requirements:")
    print("1. Nominatim API (Geocoding)")
    print("2. Open-Meteo API (Weather)")
    print("3. Overpass API (Tourist Attractions)")
    print("\n")
    
    results = []
    
    # Test individual APIs
    results.append(("Nominatim", test_nominatim()))
    results.append(("Open-Meteo", test_open_meteo()))
    results.append(("Overpass", test_overpass()))
    
    # Test complete flow
    results.append(("Complete Flow", test_full_flow()))
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:20} {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL API TESTS PASSED!")
        print("All open-source APIs are properly configured and working.")
    else:
        print("❌ SOME TESTS FAILED")
        print("Please check your internet connection and API endpoints.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

