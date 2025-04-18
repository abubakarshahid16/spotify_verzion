import os
import requests
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'

# Disable simulation mode to use real Spotify API
SIMULATE_SPOTIFY = False
print("Spotify simulation mode: False")

def get_spotify_token():
    """
    Get an access token from Spotify API using client credentials flow.
    
    Returns:
        str: Access token if successful, None otherwise
    """
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        print("Error: Spotify credentials not found in environment variables")
        return None
        
    # Encode credentials for basic auth
    auth_header = base64.b64encode(
        f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()
    ).decode()
    
    # Request token
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    
    try:
        response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)
        response.raise_for_status()
        return response.json()['access_token']
    except requests.exceptions.RequestException as e:
        print(f"Error getting Spotify token: {e}")
        return None

def search_artist(token, artist_name, limit=10):
    """
    Search for artists on Spotify by name.
    
    Args:
        token (str): Spotify access token
        artist_name (str): Name of the artist to search for
        limit (int): Maximum number of results to return
        
    Returns:
        list: List of artist dictionaries with id, name, and images
    """
    if not token:
        print("Error: No valid Spotify token provided")
        return []
        
    headers = {'Authorization': f'Bearer {token}'}
    params = {
        'q': artist_name,
        'type': 'artist',
        'limit': limit
    }
    
    try:
        response = requests.get(
            f"{SPOTIFY_API_BASE_URL}/search",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        
        artists = response.json()['artists']['items']
        return [{
            'id': artist['id'],
            'name': artist['name'],
            'image_url': artist['images'][0]['url'] if artist['images'] else None,
            'popularity': artist['popularity'],
            'genres': artist['genres']
        } for artist in artists]
    except requests.exceptions.RequestException as e:
        print(f"Error searching Spotify artists: {e}")
        return []

def get_top_tracks(token, artist_id, country='US'):
    """
    Get top tracks for an artist from Spotify.
    
    Args:
        token (str): Spotify access token
        artist_id (str): Spotify artist ID
        country (str): Country code for market
        
    Returns:
        list: List of track dictionaries with name, id, album, and artists
    """
    if not token:
        print("Error: No valid Spotify token provided")
        return []
        
    headers = {'Authorization': f'Bearer {token}'}
    params = {'market': country}
    
    try:
        response = requests.get(
            f"{SPOTIFY_API_BASE_URL}/artists/{artist_id}/top-tracks",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        
        tracks = response.json()['tracks']
        return [{
            'id': track['id'],
            'name': track['name'],
            'album': {
                'name': track['album']['name'],
                'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None
            },
            'artists': [{'name': artist['name']} for artist in track['artists']],
            'preview_url': track['preview_url'],
            'external_url': track['external_urls']['spotify']
        } for track in tracks]
    except requests.exceptions.RequestException as e:
        print(f"Error getting Spotify top tracks: {e}")
        return [] 