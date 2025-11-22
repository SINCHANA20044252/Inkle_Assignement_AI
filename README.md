# Multi-Agent Tourism System

A multi-agent system that helps users plan their trips by providing weather information and tourist attraction suggestions for any place.

## 🌐 Web Application Available!

The system is now available as a **beautiful web application** with a modern UI. Run `python app.py` to start the web server!

## Features

- **🌐 Web Interface**: Beautiful, modern web UI with responsive design
- **🌍 Multi-Language Support**: Translate results to 30+ languages (Japanese, Chinese, Spanish, French, etc.)
- **Weather Agent**: Fetches current weather and forecast using Open-Meteo API
- **Places Agent**: Suggests up to 5 tourist attractions using Overpass API
- **Tourism AI Agent**: Orchestrates the system and provides natural language responses using OpenAI API
- **Error Handling**: Gracefully handles non-existent places
- **Lightweight**: Uses OpenAI SDK directly (no heavy dependencies)
- **Dual Mode**: Online (AI-powered) and Offline (direct API) modes

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your OpenAI API key (optional, for AI mode):
```
OPENAI_API_KEY=your_api_key_here
```

3. **Run the Web Application** (Recommended):
```bash
python app.py
```
Then open your browser to: `http://localhost:5000`

4. Or run the CLI version:
```bash
python main.py
```

5. Or test the offline mode:
```bash
python offline_main.py
```

## Usage

### Online Mode (with OpenAI)

Run the main application:
```bash
python main.py
```

Enter a place you want to visit, and optionally ask about weather or places to visit.

Examples:
- "I'm going to go to Bangalore, let's plan my trip."
- "I'm going to go to Bangalore, what is the temperature there"
- "I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?"

### Offline Mode (without OpenAI - for testing APIs)

Test the weather and places APIs without needing OpenAI:

```bash
python offline_main.py
```

Or run automated tests:
```bash
python test_offline.py
```

The offline mode:
- Works without OpenAI API key
- Directly asks for place name and what information you want
- Tests all APIs (Nominatim, Open-Meteo, Overpass)
- Perfect for testing when OpenAI quota is exceeded

## APIs Used

All APIs are **open-source web services** (no installation needed, accessed via HTTP):

- **Nominatim API**: For geocoding (getting coordinates from place names)
  - Endpoint: `https://nominatim.openstreetmap.org/search`
  - Documentation: https://nominatim.org/release-docs/develop/api/Search/
  
- **Open-Meteo API**: For weather data
  - Endpoint: `https://api.open-meteo.com/v1/forecast`
  - Documentation: https://open-meteo.com/en/docs
  
- **Overpass API**: For tourist attractions and places of interest
  - Base URL: `https://overpass-api.de/api/interpreter`
  - Documentation: https://wiki.openstreetmap.org/wiki/Overpass_API

### Verify APIs are Working

Run the API test script to verify all APIs are accessible:
```bash
python test_apis.py
```

This will test:
- ✅ Nominatim API (geocoding)
- ✅ Open-Meteo API (weather)
- ✅ Overpass API (tourist attractions)
- ✅ Complete flow (all APIs together)

