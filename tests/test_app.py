import pytest
from pathlib import Path
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

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
        client.post('/upload', data={
            'file': (f, 'participants.json')
        })
    
    # Then generate pairings
    response = client.post('/generate')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'passwords' in data
    assert len(data['passwords']) == 3

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