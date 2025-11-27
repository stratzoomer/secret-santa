from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
from pathlib import Path
from secret_santa import SecretSanta
import os
import random
import datetime
import uuid
import tempfile

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Store SecretSanta instances per event (session-based isolation)
# In production, consider using Redis or a database for this
event_santas = {}

# List of whimsical locations and activities
LOCATIONS = [
    "in the kitchen, trying to cook with a lightsaber",
    "at the gym, bench-pressing Baby Yoda",
    "in the bathroom, having a lightsaber duel with his reflection",
    "at the grocery store, looking for Beskar steel in the frozen foods",
    "in the garage, trying to fix the Razor Crest with duct tape",
    "at the beach, building sandcastles with his helmet on",
    "in the library, reading 'The Art of Bounty Hunting'",
    "at the coffee shop, ordering a 'Dark Side Roast'",
    "in the park, teaching Baby Yoda to use the Force on squirrels",
    "at the mall, looking for a new cape in the clearance section",
    "in the garden, growing space carrots",
    "at the bar, trying to explain why he never takes off his helmet",
    "in the attic, organizing his collection of bounty pucks",
    "at the zoo, trying to communicate with the Wookiees",
    "in the basement, practicing his 'I have spoken' speech"
]

@app.route('/')
def index():
    return render_template('index.html')

def get_or_create_event_id():
    """Get the event ID from session or create a new one."""
    if 'event_id' not in session:
        session['event_id'] = str(uuid.uuid4())
    return session['event_id']

def get_santa_for_session():
    """Get the SecretSanta instance for the current session."""
    event_id = get_or_create_event_id()
    if event_id not in event_santas:
        event_santas[event_id] = SecretSanta()
    return event_santas[event_id]

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.json'):
        return jsonify({'error': 'File must be JSON'}), 400
    
    # Get session-specific SecretSanta instance
    santa = get_santa_for_session()
    event_id = get_or_create_event_id()
    
    # Use unique temporary filename to prevent conflicts
    temp_filename = f"temp_participants_{event_id}_{uuid.uuid4().hex[:8]}.json"
    temp_path = Path(tempfile.gettempdir()) / temp_filename
    
    try:
        file.save(temp_path)
        
        # Load participants
        if santa.load_from_file(str(temp_path)):
            # Clean up
            temp_path.unlink()
            return jsonify({'message': 'Participants loaded successfully', 'event_id': event_id})
        else:
            # Clean up
            temp_path.unlink()
            return jsonify({'error': 'Failed to load participants'}), 400
    except Exception as e:
        # Ensure cleanup on error
        if temp_path.exists():
            temp_path.unlink()
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/generate', methods=['POST'])
def generate_pairings():
    santa = get_santa_for_session()
    event_id = get_or_create_event_id()
    
    pairings = santa.generate_pairings()
    if pairings:
        # Save to event-specific directory
        event_dir = f"secret_santa_pairings/{event_id}"
        santa.save_pairings(pairings, base_dir=event_dir)
        return jsonify({
            'message': 'Pairings generated successfully',
            'passwords': santa.passwords,
            'event_id': event_id
        })
    else:
        return jsonify({'error': 'Could not generate valid pairings'}), 400

@app.route('/check_assignment', methods=['POST'])
def check_assignment():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    event_id = data.get('event_id') or session.get('event_id')
    
    if not name or not password:
        return jsonify({'error': 'Name and password required'}), 400
    
    if not event_id:
        return jsonify({'error': 'Event ID required. Please provide event_id or upload participants first.'}), 400
    
    # Check in event-specific directory first, then fall back to root for backward compatibility
    assignment_file = Path(f"secret_santa_pairings/{event_id}") / f"{name}.json"
    if not assignment_file.exists():
        # Fallback to root directory for backward compatibility
        assignment_file = Path("secret_santa_pairings") / f"{name}.json"
    
    if not assignment_file.exists():
        return jsonify({'error': 'No assignment found'}), 404
    
    try:
        with open(assignment_file, "r") as f:
            assignment = json.load(f)
        
        if assignment["password"] != password:
            return jsonify({'error': 'Invalid password'}), 401
        
        return jsonify({
            'receiver': assignment['receiver']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/where_is_mando', methods=['GET'])
def where_is_mando():
    location = random.choice(LOCATIONS)
    return jsonify({
        'message': f"Mando is {location}",
        'timestamp': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True) 