"""
API clients for external services: Nominatim, Open-Meteo, and Overpass
"""
import requests
from typing import Optional, Dict, List, Tuple
import time


class NominatimClient:
    """
    Client for Nominatim API (geocoding)
    
    Base URL: https://nominatim.openstreetmap.org/search
    Documentation: https://nominatim.org/release-docs/develop/api/Search/
    
    This client fetches REAL geocoding data from Nominatim API.
    It does NOT use AI knowledge.
    """
    
    BASE_URL = "https://nominatim.openstreetmap.org/search"
    
    def get_coordinates(self, place_name: str) -> Optional[Tuple[float, float]]:
        """
        Get latitude and longitude for a place name.
        
        Args:
            place_name: Name of the place
            
        Returns:
            Tuple of (latitude, longitude) or None if not found
        """
        params = {
            "q": place_name,
            "format": "json",
            "limit": 1
        }
        
        headers = {
            "User-Agent": "Tourism-AI-Agent/1.0"
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                return (lat, lon)
            return None
        except Exception as e:
            print(f"Error fetching coordinates: {e}")
            return None
    
    def get_place_details(self, place_name: str) -> Optional[Dict]:
        """
        Get detailed information about a place including name, type, and country.
        
        Args:
            place_name: Name of the place
            
        Returns:
            Dictionary with place details or None if not found
        """
        params = {
            "q": place_name,
            "format": "json",
            "limit": 1,
            "addressdetails": 1
        }
        
        headers = {
            "User-Agent": "Tourism-AI-Agent/1.0"
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                result = data[0]
                place_details = {
                    "name": result.get("name", place_name),
                    "display_name": result.get("display_name", place_name),
                    "type": result.get("type", "unknown"),
                    "lat": float(result.get("lat", 0)),
                    "lon": float(result.get("lon", 0)),
                    "country": result.get("address", {}).get("country", "Unknown"),
                    "state": result.get("address", {}).get("state", ""),
                    "city": result.get("address", {}).get("city", ""),
                    "importance": result.get("importance", 0),
                    "osm_type": result.get("osm_type", "")
                }
                
                # Check if the found place name closely matches the search term
                found_name = place_details["name"].lower()
                search_term = place_name.lower().strip()
                
                # Calculate match confidence
                # Exact match or contains the search term
                if found_name == search_term or search_term in found_name:
                    place_details["match_confidence"] = "high"
                # Partial match (e.g., "Valhalla" matches "Valhalla, NY")
                elif any(word in found_name for word in search_term.split()):
                    place_details["match_confidence"] = "medium"
                else:
                    place_details["match_confidence"] = "low"
                
                return place_details
            return None
        except Exception as e:
            print(f"Error fetching place details: {e}")
            return None
    
    def verify_place_exists(self, place_name: str, strict: bool = True) -> Tuple[bool, Optional[Dict], str]:
        """
        Verify if a place exists with confidence checking.
        
        Args:
            place_name: Name of the place to verify
            strict: If True, requires high confidence match
            
        Returns:
            Tuple of (exists, place_details, message)
        """
        place_details = self.get_place_details(place_name)
        
        if not place_details:
            return (False, None, "I don't know this place exists.")
        
        # Check if it's a very small place or has low importance
        importance = place_details.get("importance", 0)
        place_type = place_details.get("type", "").lower()
        
        # Filter out very small places or non-tourist locations in strict mode
        if strict:
            # Reject very small places (hamlets, villages with low importance)
            if importance < 0.3 and place_type in ["hamlet", "village", "locality"]:
                return (False, place_details, "I don't know this place exists.")
            
            # Check match confidence
            confidence = place_details.get("match_confidence", "low")
            if confidence == "low":
                return (False, place_details, "I don't know this place exists.")
        
        # Place exists and is valid
        return (True, place_details, f"Found {place_details['display_name']}")


class OpenMeteoClient:
    """
    Client for Open-Meteo API (weather)
    
    Endpoint: https://api.open-meteo.com/v1/forecast
    Documentation: https://open-meteo.com/en/docs
    
    This client fetches REAL weather data from Open-Meteo API.
    It does NOT use AI knowledge.
    """
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    def get_weather(self, latitude: float, longitude: float) -> Optional[Dict]:
        """
        Get current weather and forecast for given coordinates.
        
        Args:
            latitude: Latitude of the location
            longitude: Longitude of the location
            
        Returns:
            Dictionary with weather data or None if error
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,precipitation_probability",
            "forecast_days": 1
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if "current" in data:
                return {
                    "temperature": data["current"].get("temperature_2m"),
                    "precipitation_probability": data["current"].get("precipitation_probability"),
                    "unit": data["current_units"].get("temperature_2m", "°C")
                }
            return None
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return None


class OverpassClient:
    """
    Client for Overpass API (tourist attractions)
    
    Base URL: https://overpass-api.de/api/interpreter
    Documentation: https://wiki.openstreetmap.org/wiki/Overpass_API
    
    This client fetches REAL tourist attraction data from OpenStreetMap via Overpass API.
    It does NOT use AI knowledge.
    """
    
    BASE_URL = "https://overpass-api.de/api/interpreter"
    
    def get_tourist_attractions(self, latitude: float, longitude: float, limit: int = 5) -> List[Dict]:
        """
        Get tourist attractions near given coordinates.
        
        Args:
            latitude: Latitude of the location
            longitude: Longitude of the location
            limit: Maximum number of places to return
            
        Returns:
            List of dictionaries with place information
        """
        # Overpass QL query to find tourist attractions within 10km radius
        query = f"""[out:json][timeout:25];
        (
          node["tourism"](around:10000,{latitude},{longitude});
          way["tourism"](around:10000,{latitude},{longitude});
        );
        out body;
        >;
        out skel qt;"""
        
        try:
            response = requests.post(
                self.BASE_URL,
                data={"data": query},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            places = []
            seen_names = set()
            
            for element in data.get("elements", []):
                tags = element.get("tags", {})
                if not tags:
                    continue
                
                # Check if it's a tourism-related element
                if "tourism" not in tags:
                    continue
                
                name = tags.get("name") or tags.get("name:en") or tags.get("name:en-GB")
                
                if name and name not in seen_names:
                    places.append({
                        "name": name,
                        "type": tags.get("tourism", "attraction")
                    })
                    seen_names.add(name)
                    
                    if len(places) >= limit:
                        break
            
            return places[:limit]
        except Exception as e:
            print(f"Error fetching tourist attractions: {e}")
            return []

