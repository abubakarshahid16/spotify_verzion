from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import requests
import base64
import json
from dotenv import load_dotenv
from utils.spotify_utils import get_spotify_token, search_artist, get_top_tracks
from utils.verizon_utils import get_devices, send_message

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'spotify-verizon-app-secret')

@app.route('/')
def index():
    """Home page route."""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Search for artists on Spotify."""
    artist_name = request.form.get('artist_name')
    if not artist_name:
        return render_template('index.html', error='Please enter an artist name')
    
    # Get Spotify token
    token = get_spotify_token()
    if not token:
        return render_template('index.html', error='Failed to authenticate with Spotify')
    
    # Search for artist
    artists = search_artist(token, artist_name)
    if not artists:
        return render_template('index.html', error='No artists found')
    
    return render_template('search_results.html', artists=artists)

@app.route('/artist/<artist_id>')
def artist_top_tracks(artist_id):
    """Get top tracks for an artist."""
    # Get Spotify token
    token = get_spotify_token()
    if not token:
        return redirect(url_for('index'))
    
    # Get top tracks
    top_tracks = get_top_tracks(token, artist_id)
    if not top_tracks:
        return render_template('index.html', error='Failed to retrieve top tracks')
    
    # Store top tracks in session
    session['top_tracks'] = top_tracks
    
    return render_template('top_tracks.html', tracks=top_tracks)

@app.route('/verizon_devices')
def verizon_devices():
    """Get available Verizon devices."""
    print("Verizon devices route called")
    
    # Get devices from Verizon API
    devices = get_devices()
    
    print(f"Devices returned: {devices}")
    return render_template('devices.html', 
                          devices=devices, 
                          tracks=session.get('top_tracks', []))

@app.route('/send_message', methods=['POST'])
def send_message_route():
    """Send top tracks to a device."""
    device_id = request.form.get('device_id')
    if not device_id:
        return jsonify({'success': False, 'message': 'No device selected'})
    
    top_tracks = session.get('top_tracks', [])
    if not top_tracks:
        return jsonify({'success': False, 'message': 'No tracks to send'})
    
    # Format the message
    message = "Top 10 Songs:\n"
    for i, track in enumerate(top_tracks[:10], 1):
        message += f"{i}. {track['name']} - {track['artists'][0]['name']}\n"
    
    # Send message using Verizon API
    result = send_message(device_id, message)
    
    if result['success']:
        return render_template('success.html', message=result['message'])
    else:
        return render_template('error.html', message=result['message'])

@app.route('/test_verizon')
def test_verizon():
    """Test route for Verizon devices."""
    print("Test Verizon route called")
    devices = get_devices()
    print(f"Devices returned: {devices}")
    
    if not devices:
        return jsonify({
            'success': False,
            'message': 'Failed to retrieve Verizon devices',
            'devices': []
        })
    
    return jsonify({
        'success': True,
        'message': f'Successfully retrieved {len(devices)} devices',
        'devices': devices
    })

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    print(f"Starting Flask app on {host}:{port} with debug={debug}")
    app.run(host=host, port=port, debug=debug) 