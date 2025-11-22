"""
Flask web application for Multi-Agent Tourism System
"""
from flask import Flask, render_template, request, jsonify
from offline_main import TourismSystemOffline
from agents import TourismAIAgent
from translator import translator, LANGUAGES
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tourism-system-secret-key'

# Initialize systems
offline_system = TourismSystemOffline()

# Try to initialize online system (may fail if no API key)
try:
    online_system = TourismAIAgent()
    has_openai = True
    print("✓ AI Mode initialized successfully")
except ValueError as e:
    has_openai = False
    online_system = None
    print(f"⚠ AI Mode disabled: {str(e)}")
except Exception as e:
    has_openai = False
    online_system = None
    print(f"⚠ AI Mode disabled: {str(e)}")


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', has_openai=has_openai, languages=LANGUAGES)


@app.route('/api/query', methods=['POST'])
def query():
    """API endpoint for processing queries"""
    try:
        data = request.json
        place_name = data.get('place', '').strip()
        mode = data.get('mode', 'offline')  # 'offline' or 'online'
        get_weather = data.get('weather', False)
        get_places = data.get('places', False)
        user_input = data.get('user_input', '')  # For online mode
        target_lang = data.get('language', 'en')  # Translation language
        
        if not place_name and not user_input:
            return jsonify({
                'success': False,
                'error': 'Please provide a place name or query'
            }), 400
        
        # Use online mode if requested and available
        if mode == 'online':
            if not has_openai:
                return jsonify({
                    'success': False,
                    'error': 'AI Mode is not available. OpenAI API key is missing. Please use Offline Mode instead.',
                    'fallback': True
                }), 400
            
            if not user_input:
                return jsonify({
                    'success': False,
                    'error': 'Please enter your query in the text area'
                }), 400
            
            try:
                response = online_system.process_query(user_input)
                
                # Check if response is an error message
                if not response or response.startswith("I couldn't identify") or response.startswith("I don't know"):
                    # Translate response if needed
                    if target_lang != 'en':
                        response = translator.translate_response(response, target_lang)
                    return jsonify({
                        'success': True,
                        'response': response,
                        'mode': 'online',
                        'is_info': True
                    })
                
                # Translate response if needed
                if target_lang != 'en':
                    response = translator.translate_response(response, target_lang)
                
                return jsonify({
                    'success': True,
                    'response': response,
                    'mode': 'online'
                })
            except ValueError as e:
                # API key or initialization error
                return jsonify({
                    'success': False,
                    'error': f'AI Mode initialization error: {str(e)}. Please check your OpenAI API key.',
                    'fallback': True
                }), 500
            except Exception as e:
                # Log the full error for debugging
                import traceback
                error_trace = traceback.format_exc()
                print(f"AI Mode Error: {error_trace}")
                
                # Check for specific OpenAI errors
                error_str = str(e).lower()
                if 'quota' in error_str or 'insufficient' in error_str:
                    return jsonify({
                        'success': False,
                        'error': 'OpenAI API quota exceeded. Please check your account billing or try again later.',
                        'fallback': True
                    }), 429
                elif 'api key' in error_str or 'authentication' in error_str:
                    return jsonify({
                        'success': False,
                        'error': 'Invalid OpenAI API key. Please check your .env file.',
                        'fallback': True
                    }), 401
                else:
                    return jsonify({
                        'success': False,
                        'error': f'Error processing query: {str(e)}. Try using Offline Mode instead.',
                        'fallback': True,
                        'details': error_trace if app.debug else None
                    }), 500
        
        # Use offline mode
        if not place_name:
            return jsonify({
                'success': False,
                'error': 'Please provide a place name for offline mode'
            }), 400
        
        # Verify place exists with strict checking
        exists, place_details, message = offline_system.nominatim.verify_place_exists(place_name, strict=True)
        
        if not exists:
            # Generate natural AI response for non-existent place
            error_message = generate_error_response(place_name, target_lang, has_openai)
            return jsonify({
                'success': False,
                'error': error_message,
                'coordinates': None,
                'is_ai_response': True,
                'found_place': place_details.get('display_name') if place_details else None
            }), 404
        
        coords = (place_details['lat'], place_details['lon'])
        
        # Process query
        response = offline_system.process_query(place_name, get_weather, get_places)
        
        # Translate response if needed
        if target_lang != 'en':
            response = translator.translate_response(response, target_lang, place_name)
        
        return jsonify({
            'success': True,
            'response': response,
            'place': place_name,
            'coordinates': coords,
            'mode': 'offline',
            'language': target_lang
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/api/verify-place', methods=['POST'])
def verify_place():
    """Verify if a place exists and get coordinates"""
    try:
        data = request.json
        place_name = data.get('place', '').strip()
        target_lang = data.get('language', 'en')
        
        if not place_name:
            error_msg = 'Please provide a place name'
            if target_lang != 'en':
                error_msg = translator.translate(error_msg, target_lang)
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400
        
        # Verify place with strict checking
        exists, place_details, message = offline_system.nominatim.verify_place_exists(place_name, strict=True)
        
        if exists and place_details:
            # Show what was actually found
            display_name = place_details.get('display_name', place_name)
            coords = (place_details['lat'], place_details['lon'])
            
            if target_lang != 'en':
                message = translator.translate(message, target_lang)
            
            return jsonify({
                'success': True,
                'place': place_name,
                'found_place': display_name,
                'place_type': place_details.get('type', ''),
                'country': place_details.get('country', ''),
                'coordinates': coords,
                'message': message,
                'confidence': place_details.get('match_confidence', 'medium')
            })
        else:
            # Generate natural AI response
            error_msg = generate_error_response(place_name, target_lang, has_openai)
            found_place = place_details.get('display_name') if place_details else None
            return jsonify({
                'success': False,
                'error': error_msg,
                'is_ai_response': True,
                'found_place': found_place,
                'reason': 'Low confidence match or very small place'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error: {str(e)}'
        }), 500


def generate_error_response(place_name: str, target_lang: str = 'en', use_ai: bool = False) -> str:
    """
    Generate a natural AI response for non-existent places.
    
    Args:
        place_name: The place name that doesn't exist
        target_lang: Target language for translation
        use_ai: Whether to use OpenAI for response generation
        
    Returns:
        Natural error message
    """
    # Try to use AI for natural response if available
    if use_ai and has_openai:
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                client = OpenAI(api_key=api_key)
                prompt = f"""The user asked about a place called "{place_name}", but this place doesn't exist in the database. 
Respond naturally and politely that you don't know this place exists. 
Keep it brief and friendly, similar to: "I don't know this place exists."
Do not suggest alternatives or ask questions, just state that you don't know this place exists.

Your response:"""
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful tourism assistant. When a place doesn't exist, respond naturally and politely saying you don't know this place exists."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=50
                )
                error_msg = response.choices[0].message.content.strip()
                
                # Translate if needed
                if target_lang != 'en':
                    error_msg = translator.translate(error_msg, target_lang)
                
                return error_msg
        except Exception as e:
            print(f"AI error response generation failed: {e}")
            # Fall through to default message
    
    # Default natural message
    error_msg = f"I don't know this place exists."
    
    # Translate if needed
    if target_lang != 'en':
        error_msg = translator.translate(error_msg, target_lang)
    
    return error_msg


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

