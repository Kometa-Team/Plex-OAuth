"""
Plex OAuth Flask Application
A minimal Flask app for Plex OAuth authentication
"""

import os
import uuid
import requests
from flask import Flask, render_template, redirect, url_for, session, request, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Plex API endpoints
PLEX_API_URL = "https://plex.tv/api/v2"
PLEX_AUTH_URL = "https://app.plex.tv/auth"

# App configuration
APP_NAME = os.environ.get('APP_NAME', 'Kometa Plex Auth')
APP_VERSION = os.environ.get('APP_VERSION', '1.0')


def get_client_identifier():
    """Get or create a client identifier for this session."""
    if 'client_id' not in session:
        session['client_id'] = str(uuid.uuid4())
    return session['client_id']


def get_plex_headers():
    """Get common headers for Plex API requests."""
    return {
        'X-Plex-Client-Identifier': get_client_identifier(),
        'X-Plex-Product': APP_NAME,
        'X-Plex-Version': APP_VERSION,
        'Accept': 'application/json'
    }


@app.route('/')
def index():
    """Home page with authentication button."""
    return render_template('index.html', app_name=APP_NAME)


@app.route('/auth/start')
def auth_start():
    """Start the authentication flow by creating a PIN."""
    try:
        # Create a PIN
        response = requests.post(
            f"{PLEX_API_URL}/pins",
            headers=get_plex_headers(),
            params={'strong': 'true'}
        )
        response.raise_for_status()
        pin_data = response.json()
        
        # Store PIN ID in session
        session['pin_id'] = pin_data['id']
        session['pin_code'] = pin_data['code']
        
        # Construct auth URL
        base_url = request.url_root.rstrip('/')
        forward_url = f"{base_url}/auth/callback"
        
        auth_url = (
            f"{PLEX_AUTH_URL}#?"
            f"clientID={get_client_identifier()}&"
            f"code={pin_data['code']}&"
            f"forwardUrl={forward_url}&"
            f"context[device][product]={APP_NAME}"
        )
        
        # Redirect to Plex auth
        return redirect(auth_url)
        
    except requests.RequestException as e:
        return render_template('error.html', error=f"Failed to start authentication: {str(e)}")


@app.route('/auth/callback')
def auth_callback():
    """Handle the callback from Plex after authentication."""
    pin_id = session.get('pin_id')
    
    if not pin_id:
        return render_template('error.html', error="No authentication session found")
    
    try:
        # Check the PIN to get the auth token
        response = requests.get(
            f"{PLEX_API_URL}/pins/{pin_id}",
            headers=get_plex_headers()
        )
        response.raise_for_status()
        pin_data = response.json()
        
        auth_token = pin_data.get('authToken')
        
        if auth_token:
            # Get user info
            user_response = requests.get(
                f"{PLEX_API_URL}/user",
                headers={**get_plex_headers(), 'X-Plex-Token': auth_token}
            )
            user_response.raise_for_status()
            user_data = user_response.json()
            
            return render_template(
                'success.html',
                token=auth_token,
                username=user_data.get('username', 'Unknown'),
                email=user_data.get('email', 'Unknown')
            )
        else:
            return render_template('error.html', error="Authentication was not completed")
            
    except requests.RequestException as e:
        return render_template('error.html', error=f"Failed to verify authentication: {str(e)}")


@app.route('/health')
def health():
    """Health check endpoint for monitoring."""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', 'False') == 'True')
