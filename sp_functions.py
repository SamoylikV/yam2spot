import json
import os
import spotipy

def sp_save_tracks_to_json(tracks, directory='data', filename='saved_tracks.json'):
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    try:
        with open(filepath, 'r') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    for item in tracks['items']:
        track = item['track']
        if not any(existing_track['name'] == track['name'] for existing_track in existing_data):
            existing_data.append({'name': track['name'], 'artist': track['artists'][0]['name']})

    with open(filepath, 'w') as f:
        json.dump(existing_data, f, indent=2)

def sp_like_track():
    pass
