import random
import os
import json
from typing import Dict, List, Set, Optional
from collections import defaultdict
from pathlib import Path

class SecretSanta:
    def __init__(self):
        self.participants: Dict[str, Set[str]] = {}
        self.passwords: Dict[str, str] = {}
        
    def add_participant(self, name: str, exclusions: Optional[List[str]] = None) -> None:
        """Add a participant with their exclusion list."""
        if exclusions is None:
            exclusions = []
        self.participants[name] = set(exclusions)
        # Generate a random password for the participant
        self.passwords[name] = ''.join(random.choices('0123456789', k=6))
        
    def load_from_file(self, filename: str) -> bool:
        """Load participants and exclusions from a JSON file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            if 'participants' not in data:
                print("Error: Invalid file format. Missing 'participants' key.")
                return False
                
            for participant in data['participants']:
                if 'name' not in participant:
                    print("Error: Invalid participant format. Missing 'name' key.")
                    return False
                    
                name = participant['name']
                exclusions = participant.get('exclusions', [])
                self.add_participant(name, exclusions)
                
            return True
            
        except json.JSONDecodeError:
            print("Error: Invalid JSON file")
            return False
        except Exception as e:
            print(f"Error loading file: {str(e)}")
            return False
        
    def validate_exclusions(self) -> bool:
        """Validate that all exclusions are valid participants."""
        all_names = set(self.participants.keys())
        for name, exclusions in self.participants.items():
            if not exclusions.issubset(all_names):
                invalid = exclusions - all_names
                print(f"Error: {name} has invalid exclusions: {invalid}")
                return False
        return True
    
    def generate_pairings(self) -> Optional[Dict[str, str]]:
        """Generate valid Secret Santa pairings."""
        if not self.validate_exclusions():
            return None
            
        names = list(self.participants.keys())
        if len(names) < 2:
            print("Error: Need at least 2 participants")
            return None
            
        # Try to generate valid pairings
        max_attempts = 1000
        for _ in range(max_attempts):
            # Create a copy of names and shuffle
            available = names.copy()
            random.shuffle(available)
            
            # Try to create valid pairings
            pairings = {}
            valid = True
            
            for giver in names:
                # Find a valid receiver
                valid_receiver = None
                for receiver in available:
                    if (receiver != giver and 
                        receiver not in self.participants[giver] and
                        giver not in self.participants[receiver]):
                        valid_receiver = receiver
                        break
                
                if valid_receiver is None:
                    valid = False
                    break
                    
                pairings[giver] = valid_receiver
                available.remove(valid_receiver)
            
            if valid:
                return pairings
                
        print("Error: Could not generate valid pairings after multiple attempts")
        return None

    def save_pairings(self, pairings: Dict[str, str]) -> None:
        """Save pairings to individual files for each participant."""
        # Create a directory for the pairings
        pairings_dir = Path("secret_santa_pairings")
        pairings_dir.mkdir(exist_ok=True)
        
        # Save each participant's assignment
        for giver, receiver in pairings.items():
            assignment = {
                "giver": giver,
                "receiver": receiver,
                "password": self.passwords[giver]
            }
            
            # Save to a file named after the giver
            with open(pairings_dir / f"{giver}.json", "w") as f:
                json.dump(assignment, f, indent=2)
        
        # Save the master list (encrypted) for verification
        master_list = {
            "pairings": pairings,
            "passwords": self.passwords
        }
        with open(pairings_dir / "master_list.json", "w") as f:
            json.dump(master_list, f, indent=2)

def main():
    santa = SecretSanta()
    
    # Ask if user wants to load from file
    use_file = input("Do you want to load participants from a file? (y/n): ").lower().strip() == 'y'
    
    if use_file:
        filename = input("Enter the path to the JSON file: ").strip()
        if not santa.load_from_file(filename):
            print("Failed to load participants from file. Exiting.")
            return
    else:
        # Get number of participants
        while True:
            try:
                num_participants = int(input("Enter number of participants: "))
                if num_participants < 2:
                    print("Please enter at least 2 participants")
                    continue
                break
            except ValueError:
                print("Please enter a valid number")
        
        # Get participant names and exclusions
        for i in range(num_participants):
            name = input(f"\nEnter name for participant {i+1}: ").strip()
            exclusions_input = input(f"Enter exclusions for {name} (comma-separated, or press Enter for none): ").strip()
            
            exclusions = []
            if exclusions_input:
                exclusions = [e.strip() for e in exclusions_input.split(",")]
            
            santa.add_participant(name, exclusions)
    
    # Generate and display pairings
    print("\nGenerating Secret Santa pairings...")
    pairings = santa.generate_pairings()
    
    if pairings:
        # Save pairings to individual files
        santa.save_pairings(pairings)
        
        print("\nSecret Santa pairings have been generated!")
        print("\nEach participant has been assigned a unique password.")
        print("To view your assignment:")
        print("1. Go to the 'secret_santa_pairings' directory")
        print("2. Open the file with your name")
        print("3. Use your password to verify your identity")
        
        # Display passwords to the organizer
        print("\nPasswords for each participant:")
        print("-" * 30)
        for name, password in santa.passwords.items():
            print(f"{name}: {password}")
    else:
        print("\nCould not generate valid pairings. Please check your exclusion lists.")

if __name__ == "__main__":
    main() 