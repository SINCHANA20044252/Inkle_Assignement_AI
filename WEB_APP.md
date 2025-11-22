# Web Application Guide

## 🚀 Quick Start

1. **Install Flask** (if not already installed):
   ```bash
   pip install flask
   ```

2. **Start the web server**:
   ```bash
   python app.py
   ```

3. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

## Features

### 🌐 Web Interface
- **Modern, responsive design** that works on desktop and mobile
- **Dual mode support**: 
  - **Offline Mode**: Direct API access (no OpenAI needed)
  - **AI Mode**: Natural language processing (requires OpenAI API key)

### 📍 Offline Mode
- Enter place name directly
- Select what you want: Weather, Places, or Both
- Verify place before searching
- Works without OpenAI API key

### 🤖 AI Mode
- Natural language queries
- Example: "I'm going to Bangalore, what's the weather?"
- Automatically extracts place name and intent
- Requires OpenAI API key in `.env` file

## API Endpoints

### POST `/api/query`
Process a tourism query.

**Request body (Offline mode):**
```json
{
  "place": "Bangalore",
  "weather": true,
  "places": true,
  "mode": "offline"
}
```

**Request body (Online mode):**
```json
{
  "user_input": "I'm going to Bangalore, what's the weather?",
  "mode": "online"
}
```

### POST `/api/verify-place`
Verify if a place exists.

**Request body:**
```json
{
  "place": "Bangalore"
}
```

## Customization

### Change Port
Set the `PORT` environment variable:
```bash
# Windows PowerShell
$env:PORT=8080; python app.py

# Linux/Mac
PORT=8080 python app.py
```

### Debug Mode
The app runs in debug mode by default. To disable:
```python
app.run(host='0.0.0.0', port=port, debug=False)
```

## Troubleshooting

### Port Already in Use
If port 5000 is busy, change it:
```python
# In app.py, change:
port = int(os.environ.get('PORT', 5000))
# to:
port = int(os.environ.get('PORT', 8000))
```

### Static Files Not Loading
Make sure the directory structure is:
```
project/
├── app.py
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

### OpenAI Not Working
- Check `.env` file exists and has `OPENAI_API_KEY`
- AI Mode button won't appear if API key is missing
- Use Offline Mode instead (works without OpenAI)

## Production Deployment

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Or use platforms like:
- **Heroku**: Add `Procfile` with `web: gunicorn app:app`
- **PythonAnywhere**: Upload files and configure WSGI
- **AWS Elastic Beanstalk**: Deploy Flask app
- **DigitalOcean App Platform**: Connect GitHub repo

