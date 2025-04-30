# Secret Santa Web Application

A modern web application for managing Secret Santa gift exchanges. This application allows organizers to manage participants, generate pairings, and lets participants securely view their assignments.

Built with https://www.cursor.com/

## Features

- **Participant Management**
  - Upload participant lists via JSON file
  - Support for exclusion lists (people who can't be paired with each other)
  - Validation of participant data

- **Secure Pairing Generation**
  - Random, fair pairing algorithm
  - Respects exclusion rules
  - Multiple attempts to find valid pairings

- **Secure Assignment Viewing**
  - Password-protected assignments
  - Each participant can only view their own assignment
  - Modern, responsive web interface

## Usage

### For Organizers

1. **Upload Participants**
   - Prepare a JSON file with participant information (see example below)
   - Use the "Upload Participants" form to upload the file
   - Verify the upload was successful

2. **Generate Pairings**
   - Click the "Generate Pairings" button
   - The system will create valid pairings
   - Passwords will be displayed for distribution to participants

### For Participants

1. **View Assignment**
   - Enter your name and password
   - Click "Check Assignment"
   - View your Secret Santa assignment

### Participant JSON Format

```json
{
    "participants": [
        {
            "name": "Alice",
            "exclusions": []
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
            "name": "Thor",
            "exclusions": []
        },
        {
            "name": "Zuckerberg",
            "exclusions": []
        },
        {
            "name": "Elon",
            "exclusions": []
        }, 
        {
            "name": "Elektra",
            "exclusions": []
        },
        {
            "name": "Adele",
            "exclusions": []
        }
            
    ]
}
```


## Acknowledgments

- Created using https://www.cursor.com/
- Built with Flask
- Uses Bootstrap for the frontend
- Deployed on Render

