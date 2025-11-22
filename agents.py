"""
Multi-agent system for tourism planning
"""
from openai import OpenAI
from typing import Optional, Dict, List
from api_clients import NominatimClient, OpenMeteoClient, OverpassClient
import os
from dotenv import load_dotenv

load_dotenv()


class WeatherAgent:
    """
    Child Agent 1: Handles weather queries
    
    IMPORTANT: This agent uses Open-Meteo API (https://api.open-meteo.com/v1/forecast)
    to fetch real weather data. It does NOT use AI's own knowledge.
    
    Requirements Compliance:
    - ✅ Uses Open-Meteo API for weather data
    - ✅ Uses Nominatim API for geocoding (getting coordinates)
    - ❌ Does NOT use AI knowledge for weather information
    """
    
    def __init__(self):
        # Initialize API clients (NOT AI)
        self.nominatim = NominatimClient()  # Nominatim API for geocoding
        self.open_meteo = OpenMeteoClient()  # Open-Meteo API for weather
    
    def get_weather_info(self, place_name: str) -> Optional[str]:
        """
        Get weather information for a place using Open-Meteo API.
        
        This method uses REAL API calls, NOT AI knowledge:
        1. Nominatim API to get coordinates
        2. Open-Meteo API to get weather data
        
        Args:
            place_name: Name of the place
            
        Returns:
            Formatted weather information string or None if place not found
        """
        # Step 1: Get coordinates using Nominatim API (NOT AI)
        coords = self.nominatim.get_coordinates(place_name)
        if not coords:
            return None
        
        lat, lon = coords
        
        # Step 2: Get weather data using Open-Meteo API (NOT AI)
        weather_data = self.open_meteo.get_weather(lat, lon)
        if not weather_data:
            return None
        
        # Format the real API data
        temp = weather_data.get("temperature")
        precip_prob = weather_data.get("precipitation_probability", 0)
        unit = weather_data.get("unit", "°C")
        
        return f"In {place_name} it's currently {temp}{unit} with a chance of {precip_prob}% to rain."


class PlacesAgent:
    """
    Child Agent 2: Handles tourist attraction queries
    
    IMPORTANT: This agent uses Overpass API (https://overpass-api.de/api/interpreter)
    to fetch real tourist attraction data from OpenStreetMap. It does NOT use AI's own knowledge.
    
    Requirements Compliance:
    - ✅ Uses Overpass API for tourist attractions
    - ✅ Uses Nominatim API for geocoding (getting coordinates)
    - ❌ Does NOT use AI knowledge for places information
    """
    
    def __init__(self):
        # Initialize API clients (NOT AI)
        self.nominatim = NominatimClient()  # Nominatim API for geocoding
        self.overpass = OverpassClient()  # Overpass API for tourist attractions
    
    def get_places_info(self, place_name: str, limit: int = 5) -> Optional[str]:
        """
        Get tourist attractions for a place using Overpass API.
        
        This method uses REAL API calls, NOT AI knowledge:
        1. Nominatim API to get coordinates
        2. Overpass API to get tourist attractions from OpenStreetMap
        
        Args:
            place_name: Name of the place
            limit: Maximum number of places to return
            
        Returns:
            Formatted places information string or None if place not found
        """
        # Step 1: Get coordinates using Nominatim API (NOT AI)
        coords = self.nominatim.get_coordinates(place_name)
        if not coords:
            return None
        
        lat, lon = coords
        
        # Step 2: Get tourist attractions using Overpass API (NOT AI)
        attractions = self.overpass.get_tourist_attractions(lat, lon, limit)
        
        if not attractions:
            return f"In {place_name} these are the places you can go, - - - - -\n(No tourist attractions found in the database)"
        
        # Format the real API data
        places_list = "\n".join([f"{place['name']}" for place in attractions])
        return f"In {place_name} these are the places you can go, - - - - -\n{places_list}"


class TourismAIAgent:
    """Parent Agent: Orchestrates the tourism system"""
    
    def __init__(self):
        self.weather_agent = WeatherAgent()
        self.places_agent = PlacesAgent()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)
        self.nominatim = NominatimClient()
    
    def extract_place_name(self, user_input: str) -> Optional[str]:
        """
        Extract place name from user input using LLM.
        
        Args:
            user_input: User's input text
            
        Returns:
            Extracted place name or None
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts place names from user input. Return only the place name, nothing else. If no place is mentioned, return 'NONE'."},
                    {"role": "user", "content": f"Extract the place name from: {user_input}"}
                ],
                temperature=0.7,
                max_tokens=50
            )
            place_name = response.choices[0].message.content.strip()
            
            if place_name.upper() == "NONE" or not place_name:
                return None
            return place_name
        except Exception as e:
            print(f"Error extracting place name: {e}")
            return None
    
    def determine_intent(self, user_input: str) -> Dict[str, bool]:
        """
        Determine what the user is asking for.
        
        Args:
            user_input: User's input text
            
        Returns:
            Dictionary with flags for weather and places
        """
        user_lower = user_input.lower()
        
        weather_keywords = ["temperature", "weather", "rain", "temperature there", "hot", "cold", "forecast"]
        places_keywords = ["places", "visit", "attractions", "tourist", "see", "go", "plan my trip"]
        
        needs_weather = any(keyword in user_lower for keyword in weather_keywords)
        needs_places = any(keyword in user_lower for keyword in places_keywords)
        
        # If no specific intent, default to places
        if not needs_weather and not needs_places:
            needs_places = True
        
        return {
            "weather": needs_weather,
            "places": needs_places
        }
    
    def process_query(self, user_input: str) -> str:
        """
        Process user query and return response.
        
        Args:
            user_input: User's input text
            
        Returns:
            Formatted response string
        """
        # Extract place name
        place_name = self.extract_place_name(user_input)
        
        if not place_name:
            return "I couldn't identify a place name in your message. Please specify a location."
        
        # Verify place exists with strict checking
        exists, place_details, _ = self.nominatim.verify_place_exists(place_name, strict=True)
        if not exists:
            # Use AI to generate a natural response
            try:
                prompt = f"""The user asked about a place called "{place_name}", but this place doesn't exist in the database. 
                Respond naturally and politely that you don't know this place exists. 
                Keep it brief and friendly, similar to: "I don't know this place exists."
                
                Your response:"""
                
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful tourism assistant. When a place doesn't exist, respond naturally and politely."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=50
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                # Fallback to simple message if AI fails
                return f"I don't know this place exists. Could you please check the spelling or provide more details about the location?"
        
        # Determine intent
        intent = self.determine_intent(user_input)
        
        # Get information from child agents
        weather_info = None
        places_info = None
        
        if intent["weather"]:
            try:
                weather_info = self.weather_agent.get_weather_info(place_name)
            except Exception as e:
                print(f"Weather agent error: {e}")
                weather_info = None
        
        if intent["places"]:
            try:
                places_info = self.places_agent.get_places_info(place_name)
            except Exception as e:
                print(f"Places agent error: {e}")
                places_info = None
        
        # Combine responses
        response_parts = []
        
        if weather_info:
            response_parts.append(weather_info)
        
        if places_info:
            if weather_info:
                # Extract just the places list from places_info
                if "\n" in places_info:
                    places_list = places_info.split("\n", 1)[1]  # Get everything after first line
                    response_parts.append(f"And these are the places you can go: - - - - -\n{places_list}")
                else:
                    response_parts.append(f"And {places_info}")
            else:
                response_parts.append(places_info)
        
        if not response_parts:
            return f"I found {place_name}, but couldn't retrieve information. Please try again."
        
        return " ".join(response_parts)

