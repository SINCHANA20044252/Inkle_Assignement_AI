"""
Offline version of Multi-Agent Tourism System
Works without OpenAI - uses direct user input and API calls only
"""
from api_clients import NominatimClient, OpenMeteoClient, OverpassClient
from typing import Optional, Tuple


class TourismSystemOffline:
    """Offline version that works without OpenAI"""
    
    def __init__(self):
        self.nominatim = NominatimClient()
        self.open_meteo = OpenMeteoClient()
        self.overpass = OverpassClient()
    
    def get_weather_info(self, place_name: str) -> Optional[str]:
        """Get weather information for a place"""
        coords = self.nominatim.get_coordinates(place_name)
        if not coords:
            return None
        
        lat, lon = coords
        weather_data = self.open_meteo.get_weather(lat, lon)
        if not weather_data:
            return None
        
        temp = weather_data.get("temperature")
        precip_prob = weather_data.get("precipitation_probability", 0)
        unit = weather_data.get("unit", "°C")
        
        return f"In {place_name} it's currently {temp}{unit} with a chance of {precip_prob}% to rain."
    
    def get_places_info(self, place_name: str, limit: int = 5) -> Optional[str]:
        """Get tourist attractions for a place"""
        coords = self.nominatim.get_coordinates(place_name)
        if not coords:
            return None
        
        lat, lon = coords
        attractions = self.overpass.get_tourist_attractions(lat, lon, limit)
        
        if not attractions:
            return f"In {place_name} these are the places you can go, - - - - -\n(No tourist attractions found in the database)"
        
        places_list = "\n".join([f"{place['name']}" for place in attractions])
        return f"In {place_name} these are the places you can go, - - - - -\n{places_list}"
    
    def process_query(self, place_name: str, get_weather: bool, get_places: bool) -> str:
        """Process query and return combined response"""
        response_parts = []
        
        if get_weather:
            weather_info = self.get_weather_info(place_name)
            if weather_info:
                response_parts.append(weather_info)
            else:
                response_parts.append(f"Could not retrieve weather information for {place_name}.")
        
        if get_places:
            places_info = self.get_places_info(place_name)
            if places_info:
                if get_weather and response_parts:
                    # Extract just the places list
                    if "\n" in places_info:
                        places_list = places_info.split("\n", 1)[1]
                        response_parts.append(f"And these are the places you can go: - - - - -\n{places_list}")
                    else:
                        response_parts.append(f"And {places_info}")
                else:
                    response_parts.append(places_info)
            else:
                response_parts.append(f"Could not retrieve tourist attractions for {place_name}.")
        
        if not response_parts:
            return f"Could not retrieve information for {place_name}. Please try again."
        
        return " ".join(response_parts)


def get_user_choice(prompt: str, options: list) -> str:
    """Get user choice from options"""
    while True:
        print(f"\n{prompt}")
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        
        try:
            choice = input("\nEnter your choice (1-{}): ".format(len(options))).strip()
            choice_num = int(choice)
            if 1 <= choice_num <= len(options):
                return options[choice_num - 1]
            else:
                print(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            return None


def main():
    """Main application loop for offline mode"""
    print("=" * 60)
    print("Multi-Agent Tourism System - OFFLINE MODE")
    print("=" * 60)
    print("\nThis version works without OpenAI API.")
    print("You can test weather and places APIs directly.")
    print("Type 'quit' or 'exit' to stop.\n")
    
    system = TourismSystemOffline()
    
    while True:
        try:
            # Get place name
            place_name = input("\nEnter the place you want to visit: ").strip()
            
            if not place_name:
                continue
            
            if place_name.lower() in ['quit', 'exit', 'q']:
                print("\nThank you for using the Tourism System. Have a great trip!")
                break
            
            # Verify place exists with strict checking
            print(f"\nVerifying {place_name}...")
            exists, place_details, message = system.nominatim.verify_place_exists(place_name, strict=True)
            
            if not exists:
                print(f"\n❌ I don't know this place exists.")
                if place_details:
                    print(f"   (Note: Found similar place: {place_details.get('display_name', 'Unknown')})")
                continue
            
            coords = (place_details['lat'], place_details['lon'])
            display_name = place_details.get('display_name', place_name)
            print(f"✓ Found: {display_name}")
            print(f"  Location: {place_details.get('country', 'Unknown')}")
            print(f"  Coordinates: {coords[0]:.4f}, {coords[1]:.4f}")
            
            # Get what user wants
            info_options = ["Weather only", "Tourist places only", "Both weather and places"]
            choice = get_user_choice("What information would you like?", info_options)
            
            if choice is None:
                break
            
            get_weather = "weather" in choice.lower() or "both" in choice.lower()
            get_places = "places" in choice.lower() or "tourist" in choice.lower() or "both" in choice.lower()
            
            # Process query
            print("\nProcessing your request...")
            response = system.process_query(place_name, get_weather, get_places)
            print(f"\n{'='*60}")
            print("RESULT:")
            print('='*60)
            print(response)
            print('='*60)
            
        except KeyboardInterrupt:
            print("\n\nThank you for using the Tourism System. Have a great trip!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()

