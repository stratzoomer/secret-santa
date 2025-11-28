import pytest
from pathlib import Path
import json
from app import app, event_santas

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key-for-sessions'
    # Clear event_santas dictionary before each test
    event_santas.clear()
    with app.test_client() as client:
        # Enable session support in test client
        with client.session_transaction() as sess:
            pass  # Initialize session
        yield client
    # Clear after test as well
    event_santas.clear()

@pytest.fixture
def sample_participants_file(tmp_path):
    participants = {
        "participants": [
            {
                "name": "Alice",
                "exclusions": ["Bob"]
            },
            {
                "name": "Bob",
                "exclusions": ["Alice"]
            },
            {
                "name": "Charlie",
                "exclusions": []
            },
            {
                "name": "Diana",
                "exclusions": []
            }
        ]
    }
    
    file_path = tmp_path / "participants.json"
    with open(file_path, 'w') as f:
        json.dump(participants, f)
    
    return file_path

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Secret Santa' in response.data

def test_upload_file_success(client, sample_participants_file):
    with open(sample_participants_file, 'rb') as f:
        response = client.post('/upload', data={
            'file': (f, 'participants.json')
        })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Participants loaded successfully'
    assert 'event_id' in data  # Verify event_id is returned

def test_upload_file_no_file(client):
    response = client.post('/upload')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'No file provided'

def test_upload_file_invalid_json(client, tmp_path):
    invalid_file = tmp_path / "invalid.json"
    with open(invalid_file, 'w') as f:
        f.write("invalid json")
    
    with open(invalid_file, 'rb') as f:
        response = client.post('/upload', data={
            'file': (f, 'invalid.json')
        })
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_generate_pairings_success(client, sample_participants_file):
    # First upload participants
    with open(sample_participants_file, 'rb') as f:
        upload_response = client.post('/upload', data={
            'file': (f, 'participants.json')
        })
    
    # Verify upload was successful
    assert upload_response.status_code == 200
    upload_data = json.loads(upload_response.data)
    assert upload_data['message'] == 'Participants loaded successfully'
    
    # Then generate pairings
    response = client.post('/generate')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'passwords' in data
    assert 'event_id' in data  # Verify event_id is returned
    assert len(data['passwords']) == 4

def test_generate_pairings_no_participants(client):
    response = client.post('/generate')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_check_assignment_success(client, sample_participants_file):
    # First upload participants and generate pairings
    with open(sample_participants_file, 'rb') as f:
        client.post('/upload', data={
            'file': (f, 'participants.json')
        })
    
    response = client.post('/generate')
    data = json.loads(response.data)
    password = data['passwords']['Alice']
    
    # Then check assignment
    response = client.post('/check_assignment', json={
        'name': 'Alice',
        'password': password
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'receiver' in data

def test_check_assignment_invalid_password(client, sample_participants_file):
    # First upload participants and generate pairings
    with open(sample_participants_file, 'rb') as f:
        client.post('/upload', data={
            'file': (f, 'participants.json')
        })
    
    client.post('/generate')
    
    # Then check assignment with invalid password
    response = client.post('/check_assignment', json={
        'name': 'Alice',
        'password': 'invalid'
    })
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['error'] == 'Invalid password'

def test_check_assignment_missing_name(client):
    response = client.post('/check_assignment', json={
        'password': '123456'
    })
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'Name and password required' 