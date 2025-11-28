import pytest
from pathlib import Path
import json
import tempfile
from secret_santa import SecretSanta

@pytest.fixture
def santa():
    return SecretSanta()

@pytest.fixture
def sample_participants():
    return {
        "participants": [
            {
                "name": "Alice",
                "exclusions": ["Bob", "Charlie"]
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

def test_add_participant(santa):
    santa.add_participant("Alice", ["Bob"])
    assert "Alice" in santa.participants
    assert santa.participants["Alice"] == {"Bob"}
    assert "Alice" in santa.passwords
    assert len(santa.passwords["Alice"]) == 6  # Password length check

def test_add_participant_no_exclusions(santa):
    santa.add_participant("Alice")
    assert "Alice" in santa.participants
    assert santa.participants["Alice"] == set()

def test_validate_exclusions_valid(santa):
    santa.add_participant("Alice", ["Bob"])
    santa.add_participant("Bob", ["Alice"])
    assert santa.validate_exclusions() is True

def test_validate_exclusions_invalid(santa):
    santa.add_participant("Alice", ["Bob", "Charlie"])
    santa.add_participant("Bob", ["Alice"])
    assert santa.validate_exclusions() is False

def test_load_from_file(santa, sample_participants):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_participants, f)
        temp_path = f.name

    try:
        assert santa.load_from_file(temp_path) is True
        assert "Alice" in santa.participants
        assert "Bob" in santa.participants
        assert "Charlie" in santa.participants
        assert santa.participants["Alice"] == {"Bob", "Charlie"}
        assert santa.participants["Bob"] == {"Alice"}
        assert santa.participants["Charlie"] == set()
    finally:
        Path(temp_path).unlink()

def test_load_from_file_invalid_json(santa):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("invalid json")
        temp_path = f.name

    try:
        assert santa.load_from_file(temp_path) is False
    finally:
        Path(temp_path).unlink()

def test_generate_pairings_valid(santa):
    santa.add_participant("Alice", ["Bob"])
    santa.add_participant("Bob", ["Alice"])
    santa.add_participant("Charlie")
    santa.add_participant("Diana")
    
    pairings = santa.generate_pairings()
    assert pairings is not None
    assert len(pairings) == 4
    
    # Check that no one is paired with themselves
    for giver, receiver in pairings.items():
        assert giver != receiver
    
    # Check that exclusions are respected
    assert pairings["Alice"] != "Bob"
    assert pairings["Bob"] != "Alice"

def test_generate_pairings_impossible(santa):
    santa.add_participant("Alice", ["Bob", "Charlie"])
    santa.add_participant("Bob", ["Alice", "Charlie"])
    santa.add_participant("Charlie", ["Alice", "Bob"])
    
    pairings = santa.generate_pairings()
    assert pairings is None

def test_save_pairings(santa, tmp_path):
    santa.add_participant("Alice")
    santa.add_participant("Bob")
    
    pairings = {"Alice": "Bob", "Bob": "Alice"}
    # Pass base_dir to save in tmp_path
    base_dir = str(tmp_path / "secret_santa_pairings")
    santa.save_pairings(pairings, base_dir=base_dir)
    
    # Check that files were created
    assert (tmp_path / "secret_santa_pairings" / "Alice.json").exists()
    assert (tmp_path / "secret_santa_pairings" / "Bob.json").exists()
    assert (tmp_path / "secret_santa_pairings" / "master_list.json").exists()
    
    # Check file contents
    with open(tmp_path / "secret_santa_pairings" / "Alice.json") as f:
        alice_data = json.load(f)
        assert alice_data["giver"] == "Alice"
        assert alice_data["receiver"] == "Bob"
        assert "password" in alice_data 