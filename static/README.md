# Secret Santa Web Application

A modern web application for managing Secret Santa gift exchanges. This application allows organizers to manage participants, generate pairings, and lets participants securely view their assignments.

**🌐 Live Application**: Available at [https://secret-santa-idlx.onrender.com/](https://secret-santa-idlx.onrender.com/)

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

- **Session-Based Isolation**
  - Each Secret Santa event gets a unique Event ID
  - Multiple organizers can run events simultaneously without conflicts
  - Participants can check assignments from any device using the Event ID

## Usage

### For Organizers

1. **Upload Participants**
   - Prepare a JSON file with participant information (see example below)
   - Use the "Upload Participants" form to upload the file
   - Verify the upload was successful
   - **Note**: A unique Event ID will be automatically generated and displayed in the Event ID section

2. **Generate Pairings**
   - Click the "Generate Pairings" button
   - The system will create valid pairings
   - Passwords will be displayed for distribution to participants
   - **Important**: Copy the Event ID using the "Copy" button and share it with all participants

3. **Share with Participants**
   - Distribute the Event ID to all participants (they'll need it to check assignments from different devices)
   - Share individual passwords with each participant privately
   - Participants will need both the Event ID and their password to view assignments

### For Participants

1. **View Assignment**
   - Enter your name and password (provided by your organizer)
   - **If checking from a different browser or device**: Enter the Event ID provided by your organizer in the optional Event ID field
   - Click "Check Assignment"
   - View your Secret Santa assignment

**Note**: If you're using the same browser where the organizer created the event, you can leave the Event ID field blank - it will be automatically detected.

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


## Understanding Event IDs

Each Secret Santa event gets a unique Event ID when participants are uploaded. This allows:

- **Multiple Events**: Different organizers can run Secret Santa events simultaneously without any conflicts
- **Cross-Device Access**: Participants can check their assignments from any device by entering the Event ID
- **Data Privacy**: Each event's data is completely isolated from others

The Event ID is displayed in the Organizer tab after uploading participants or generating pairings. Organizers should copy and share this Event ID with all participants.

## Security

- Passwords are generated randomly for each participant
- Assignments are stored securely, isolated by Event ID
- Each participant can only view their own assignment with their unique password
- HTTPS is enforced for all connections

## Acknowledgments

- Created using https://www.cursor.com/
- Built with Flask
- Uses Bootstrap for the frontend
- Deployed on Render

