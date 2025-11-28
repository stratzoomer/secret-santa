# Secret Santa Web Application

A modern web application for managing Secret Santa gift exchanges. This application allows organizers to manage participants, generate pairings, and lets participants securely view their assignments.

**🌐 Live Application**: The application is deployed and available for anyone to use at [https://secret-santa-idlx.onrender.com/](https://secret-santa-idlx.onrender.com/)

Built with https://www.cursor.com/

## Features

- **Participant Management**
  - Upload participant lists via JSON file. See [participants.json](participants.json)
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
  - Event-specific data storage prevents cross-contamination
  - Participants can check assignments from any device using the Event ID

- **Cloud-Ready**
  - Deployable to cloud platforms (e.g., Render)
  - Production-ready configuration
  - Scalable architecture

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd secret-santa
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Local Development

1. Run the development server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

### For Organizers

1. **Upload Participants**
   - Prepare a JSON file with participant information (see example below)
   - Use the "Upload Participants" form to upload the file
   - Verify the upload was successful
   - **Note**: A unique Event ID will be automatically generated for your event

2. **Generate Pairings**
   - Click the "Generate Pairings" button
   - The system will create valid pairings
   - Passwords will be displayed for distribution to participants
   - **Important**: Copy and share the Event ID with your participants (displayed in the Event ID section)

3. **Share with Participants**
   - Distribute the Event ID to all participants
   - Share individual passwords with each participant
   - Participants will need both the Event ID and their password to view assignments

### For Participants

1. **View Assignment**
   - Enter your name and password
   - If checking from a different browser or device, enter the Event ID provided by your organizer
   - Click "Check Assignment"
   - View your Secret Santa assignment

**Note**: If you're using the same browser where the organizer created the event, the Event ID field is optional as it will be automatically detected.

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

## Cloud Deployment

### Deploying to Render

1. Create a GitHub repository and push your code:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. Go to [Render](https://render.com):
   - Sign up for a free account
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Select the repository
   - Render will automatically detect the `render.yaml` configuration
   - Click "Create Web Service"

3. Your application will be deployed and available at:
```
https://your-app-name.onrender.com
```

## Project Structure

```
secret-santa/
├── app.py                 # Main Flask application
├── secret_santa.py        # Core Secret Santa logic
├── requirements.txt       # Python dependencies
├── gunicorn_config.py     # Production server configuration
├── build.sh              # Build script for deployment
├── render.yaml           # Render deployment configuration
├── templates/
│   └── index.html        # Web interface
└── secret_santa_pairings/ # Directory for assignment files (organized by Event ID)
```

## How It Works

### Session-Based Isolation

The application uses Flask sessions to create isolated environments for each Secret Santa event:

- **Event ID Generation**: When an organizer uploads participants, a unique Event ID (UUID) is automatically generated and stored in the session
- **Data Isolation**: Each event's data (participants, pairings, passwords) is stored separately, preventing conflicts when multiple organizers use the application simultaneously
- **File Organization**: Pairings are saved in `secret_santa_pairings/{event_id}/` directories, ensuring complete separation between events
- **Cross-Device Support**: Participants can check their assignments from any device by providing the Event ID along with their credentials

## Security Considerations

- Passwords are generated randomly for each participant
- Assignments are stored in separate files, isolated by Event ID
- Passwords are never displayed in plain text
- HTTPS is enforced in production
- Session-based isolation prevents data conflicts between multiple concurrent events
- Each event's data is stored in a separate directory, ensuring privacy and security

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Created using https://www.cursor.com/
- Built with Flask
- Uses Bootstrap for the frontend
- Deployed on Render