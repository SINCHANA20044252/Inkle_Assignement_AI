# Setup Instructions

Follow these steps to set up and run the Multi-Agent Tourism System:

## Step 1: Install Dependencies

Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

If you're using Python 3, you might need to use:
```bash
pip3 install -r requirements.txt
```

## Step 2: Set Up OpenAI API Key

1. Get your OpenAI API key from: https://platform.openai.com/api-keys

2. Create a `.env` file in the project root directory with the following content:

```
OPENAI_API_KEY=your_actual_api_key_here
```

Replace `your_actual_api_key_here` with your actual OpenAI API key.

**Important**: The `.env` file is already in `.gitignore`, so it won't be committed to version control.

## Step 3: Test the System

Run the test script to verify everything works:

```bash
python test_system.py
```

This will test all three example scenarios from the assignment.

## Step 4: Run the Application

Start the interactive application:

```bash
python main.py
```

Then you can interact with the system by typing queries like:
- "I'm going to go to Bangalore, let's plan my trip."
- "I'm going to go to Paris, what is the temperature there"
- "I'm going to go to Tokyo, what is the temperature there? And what are the places I can visit?"

Type `quit` or `exit` to stop the application.

## Troubleshooting

### Issue: "OPENAI_API_KEY not found"
- Make sure you've created the `.env` file
- Check that the file is named exactly `.env` (not `.env.txt`)
- Verify the API key is correct

### Issue: Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're using Python 3.7 or higher

### Issue: API rate limits
- The Nominatim API requires a User-Agent header (already implemented)
- If you hit rate limits, wait a few seconds between requests
- The Overpass API may take a few seconds to respond



