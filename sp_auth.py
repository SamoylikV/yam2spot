# sp_auth.py
import json

def get_spotify_credentials():
    with open('credentials_prod.json') as f:
        credentials = json.load(f)

    return credentials['client_id'], credentials['client_secret'], credentials['redirect_uri']
