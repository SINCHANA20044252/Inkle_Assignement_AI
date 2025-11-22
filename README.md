
````markdown
# 🌍 Multi-Agent Tourism System

A multi-agent system that helps users plan their trips by providing real-time weather information and tourist attraction suggestions for any place.

---

## 🌐 Live Web Application

The system is deployed and available online here:  
[https://inkle-assignement-ai.onrender.com](https://inkle-assignement-ai.onrender.com)

---

## ✨ Features

* **🌐 Web Interface** — Elegant and responsive UI
* **🌍 Multi-Language Support** — Translate results into 30+ languages
* **Weather Agent** — Fetches current weather + forecast using *Open-Meteo API*
* **Places Agent** — Suggests up to 5 tourist attractions using *Overpass API*
* **Tourism AI Agent** — Provides natural language responses using OpenAI API
* **Error Handling** — Identifies invalid or non-existent places
* **Lightweight** — Uses OpenAI SDK, minimal dependencies
* **Dual Mode Support**
  * Online AI mode
  * Offline API-only mode

---

## ⚙️ Setup

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
````

### 2️⃣ Create a `.env` file (required for AI mode)

```
OPENAI_API_KEY=your_api_key_here
```

### 3️⃣ Run the Web Application (Recommended)

```bash
python app.py
```

Then open:
[http://localhost:5000](http://localhost:5000)

Or access the **live deployment** here:
[https://inkle-assignement-ai.onrender.com](https://inkle-assignement-ai.onrender.com)

### 4️⃣ Run the CLI Version

```bash
python main.py
```

### 5️⃣ Run Offline Mode (No OpenAI API Key Needed)

```bash
python offline_main.py
```

---

## 🕹 Usage

### ▶️ Online Mode (with OpenAI)

Run:

```bash
python main.py
```

Then ask questions such as:

* “I'm going to go to Bangalore, let's plan my trip.”
* “I'm going to go to Bangalore, what is the temperature there?”
* “I'm going to Bangalore — weather + places to visit?”

### ▶️ Offline Mode (API Testing Only)

```bash
python offline_main.py
```

Or automated tests:

```bash
python test_offline.py
```

Offline mode:

* Works without OpenAI API key
* Tests Nominatim, Open-Meteo, Overpass
* Useful when API quota is exceeded

---

## 🌐 APIs Used

All APIs are **open-source** and accessed over HTTP:

### 📍 Nominatim API — Geocoding

* Converts place name → coordinates
* Docs: [https://nominatim.org/release-docs/develop/api/Search/](https://nominatim.org/release-docs/develop/api/Search/)

### ☁ Open-Meteo API — Weather Forecast

* Provides temperature, rain probability, and more
* Docs: [https://open-meteo.com/en/docs](https://open-meteo.com/en/docs)

### 🗺 Overpass API — Tourist Attractions

* Fetches POIs around given coordinates
* Docs: [https://wiki.openstreetmap.org/wiki/Overpass_API](https://wiki.openstreetmap.org/wiki/Overpass_API)

---

## 🧪 Verify APIs Are Working

Test all APIs:

```bash
python test_apis.py
```

This validates:

* ✅ Nominatim (Geocoding)
* ✅ Open-Meteo (Weather)
* ✅ Overpass (Places)
* ✅ Full end-to-end flow

```

---


