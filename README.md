# Spotify-Verizon Integration: Send Top 10 Songs to a Friend

This Flask-based web application integrates the Spotify API and Verizon API to allow users to search for their favorite artists, view their top 10 songs, and send those songs to a friend's device using Verizon's messaging services.

## Features

- **Spotify Integration**: Search for artists and retrieve their top 10 tracks
- **Verizon Integration**: List available devices and send messages
- **Modern UI**: Responsive design with Bootstrap 5
- **Interactive Audio**: Preview songs directly in the browser (when available)

## Prerequisites

Before running the application, you'll need:

1. Python 3.7 or higher
2. A Spotify Developer account and API credentials
3. Access to Verizon API Sandbox environment

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd spotify-verizon-app
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   
   Rename `.env.example` to `.env` and update the following variables:
   
   ```
   # Spotify API Credentials
   SPOTIFY_CLIENT_ID=your-spotify-client-id
   SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
   
   # Verizon API Credentials
   VERIZON_API_KEY=your-verizon-api-key
   ```

4. **Run the application**:
   ```
   flask run
   ```

5. **Access the application**:
   
   Open your browser and navigate to `http://127.0.0.1:5000`

## Obtaining API Credentials

### Spotify API

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Log in with your Spotify account
3. Create a new application
4. Copy the Client ID and Client Secret to your `.env` file

### Verizon API

1. Access the Verizon API Sandbox environment
2. Register for API access
3. Generate an API key
4. Copy the API key to your `.env` file

## Project Structure

```
spotify-verizon-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create from .env.example)
├── README.md              # This file
├── static/                # Static assets (CSS, JS, images)
├── templates/             # HTML templates
│   ├── base.html          # Base template with layout
│   ├── index.html         # Home page
│   ├── search_results.html # Artist search results
│   ├── top_tracks.html    # Top tracks for an artist
│   ├── devices.html       # Device selection
│   └── success.html       # Success page
└── utils/                 # Utility modules
    ├── spotify_utils.py   # Spotify API integration
    └── verizon_utils.py   # Verizon API integration
```

## Usage Flow

1. Search for an artist on the home page
2. Select an artist from the search results
3. View the artist's top 10 tracks
4. Click "Send to a Friend" to see available devices
5. Select a device to send the tracks to
6. View the success page when the message is sent

## Development Mode

For testing without a valid Verizon API key, set `SIMULATE_VERIZON_SUCCESS=true` in your `.env` file to simulate successful message sending.

## Submission Process

For competition submission, prepare:

1. The completed project code in a ZIP file
2. A completed feedback form
3. A screenshot of successful compilation output
4. A short video showcasing the working project
5. Chat history and prompts (if your AI assistant allows it) 