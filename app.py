from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
from pathlib import Path
from secret_santa import SecretSanta
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Initialize SecretSanta
santa = SecretSanta()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.json'):
        return jsonify({'error': 'File must be JSON'}), 400
    
    # Save the file temporarily
    temp_path = Path('temp_participants.json')
    file.save(temp_path)
    
    # Load participants
    if santa.load_from_file(str(temp_path)):
        # Clean up
        temp_path.unlink()
        return jsonify({'message': 'Participants loaded successfully'})
    else:
        # Clean up
        temp_path.unlink()
        return jsonify({'error': 'Failed to load participants'}), 400

@app.route('/generate', methods=['POST'])
def generate_pairings():
    pairings = santa.generate_pairings()
    if pairings:
        santa.save_pairings(pairings)
        return jsonify({
            'message': 'Pairings generated successfully',
            'passwords': santa.passwords
        })
    else:
        return jsonify({'error': 'Could not generate valid pairings'}), 400

@app.route('/check_assignment', methods=['POST'])
def check_assignment():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    
    if not name or not password:
        return jsonify({'error': 'Name and password required'}), 400
    
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

if __name__ == '__main__':
    app.run(debug=True) 