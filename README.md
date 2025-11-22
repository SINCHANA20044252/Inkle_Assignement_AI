Multi-Agent Tourism System
A multi-agent AI-powered tourism assistant that helps users plan trips by providing real-time weather updates, tourist attraction suggestions, and natural language responses — all powered by open-source APIs.
This project includes weather forecasting, tourist place recommendations, offline testing mode, and a modern web UI built with Flask.

🚀 Web Application Available!
A clean, modern, interactive web dashboard is included.
Run the app and open:
http://localhost:5000


✨ Features


🧠 Multi-Agent System


Parent: Tourism AI Agent


Child Agents:
✓ Weather Agent (Open-Meteo API)
✓ Places Agent (Overpass API)




🌐 Web Interface
Modern responsive UI built with Flask templates


🌍 Multi-Language Support
Translate responses into 30+ languages (Japanese, French, Spanish, Chinese, etc.)


⚡ Dual Mode System


Online Mode (AI-powered) — Uses OpenAI API for natural conversational responses


Offline Mode (API only) — Works without any API key




✔ Error Handling
Detects and gracefully responds to invalid or unknown place names


🧪 Full Offline Testing Suite
API test scripts included: geocoding, weather, attractions



📦 Setup Instructions
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ (Optional) Add OpenAI API key for AI Mode
Create a .env file:
OPENAI_API_KEY=your_api_key_here

3️⃣ Run the Web Application (Recommended)
python app.py

👉 Open: http://localhost:5000
4️⃣ Run the CLI Version
python main.py

5️⃣ Run Offline Mode (No API Key Needed)
python offline_main.py


🕹 Usage
✅ Online Mode (AI Powered)
Ask natural language questions:
Examples:


“I’m going to Bangalore, let’s plan my trip.”


“I’m going to Bangalore, what is the temperature there?”


“I’m going to Bangalore — give me weather + places to visit.”


📴 Offline Mode (API-Only)
Runs without OpenAI — perfect for testing:
python offline_main.py

You can test:


Geocoding


Weather


Tourist attractions


Combined workflow



🌐 APIs Used
All APIs are free & open-source, accessed through HTTP calls.
📍 Nominatim API (Geocoding)
Gets coordinates from place name
Docs: https://nominatim.org/release-docs/develop/api/Search/
☁ Open-Meteo API (Weather)
Fetches:


Temperature


Rain probability


Forecast
Docs: https://open-meteo.com/en/docs


🗺 Overpass API (Tourist Attractions)
Fetches up to 5 nearest POIs
Docs: https://wiki.openstreetmap.org/wiki/Overpass_API

🧪 API Testing
Verify that all APIs are working:
python test_apis.py

This test checks:


✔ Nominatim (geocoding)


✔ Open-Meteo (weather)


✔ Overpass API (places)


✔ Combined flow



📂 Folder Structure
Inkle_Assignement_AI/
│── app.py                 # Web UI
│── main.py                # Online CLI version
│── offline_main.py        # API-only version
│── test_apis.py           # API test script
│── templates/             # HTML templates for web app
│── static/                # CSS / images / JS
│── utils/                 # Helper modules for agents
│── requirements.txt
│── README.md


