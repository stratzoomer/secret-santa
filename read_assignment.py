import json
from pathlib import Path
import getpass

def read_assignment():
    # Get participant name
    name = input("Enter your name: ").strip()
    
    # Check if assignment file exists
    assignment_file = Path("secret_santa_pairings") / f"{name}.json"
    if not assignment_file.exists():
        print(f"Error: No assignment found for {name}")
        return
    
    # Get password
    password = getpass.getpass("Enter your password: ")
    
    try:
        # Read the assignment file
        with open(assignment_file, "r") as f:
            assignment = json.load(f)
        
        # Verify password
        if assignment["password"] != password:
            print("Error: Invalid password")
            return
        
        # Display assignment
        print("\nYour Secret Santa Assignment:")
        print("-" * 30)
        print(f"You are giving to: {assignment['receiver']}")
        
    except json.JSONDecodeError:
        print("Error: Invalid assignment file")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Secret Santa Assignment Reader")
    print("=" * 30)
    read_assignment() 