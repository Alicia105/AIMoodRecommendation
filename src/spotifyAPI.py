import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import random
import mapping
from datetime import date
from pydub import AudioSegment
from pydub.playback import play
import requests
import io
import spotipy
import requests
import json
import datetime
import time

load_dotenv("../.env")
clientID=os.getenv("SPOTIPY_CLIENT_ID")
clientSecret=os.getenv("SPOTIPY_CLIENT_SECRET")
clientRedirectURI=os.getenv("SPOTIPY_REDIRECT_URI")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=clientID,
    client_secret=clientSecret,
    redirect_uri=clientRedirectURI,
    scope="user-top-read user-read-private user-read-email playlist-modify-public playlist-modify-private user-modify-playback-state user-read-playback-state user-read-currently-playing",
    cache_path=".cache"
))

def check_and_refresh_token():
    """Check if the token is expired and refresh it if necessary."""
    token_info = sp.auth_manager.cache_handler.get_cached_token()
    if token_info:
        expires_at = token_info['expires_at']
        if expires_at <= int(time.time()):
            print("Token expired, refreshing...")
            sp.auth_manager.cache_handler.refresh_access_token(token_info['refresh_token'])
            print("Token refreshed!")
        else:
            print(f"Token is still valid. Expires at: {expires_at}")
    else:
        print("No token found in cache.")

# Checking if the token is expired and refreshing it if necessary
#check_and_refresh_token()

me = sp.me()
print(f"Logged in as: {me['display_name']}")

#to fix
def giveRecommendations(emotion):
    global sp
    check_and_refresh_token()
    """with open('spotify_genres_seeds.json', 'r') as f:
        genre_data = json.load(f)

    valid_genres = genre_data['genres']"""
    #print(valid_genres)

    genres = mapping.map_seed_genres_to_emotion(emotion)
    if genres:
        seed_genres = random.sample(genres, min(5, len(genres)))
        print(seed_genres)
    else:
        #raise ValueError(f"No genres available for emotion '{emotion}'")
        return []
    
    charac=mapping.map_emotion_to_song_characteristics(emotion)

    if emotion=="anger":
        min_valence=charac[1]
        max_valence=charac[2]
        min_arousal=charac[3]
        max_arousal=charac[4]
        min_danceability=charac[5]
        max_danceability=charac[6]
        min_loudness=charac[7]
        max_loudness=charac[8]
        recommendations = sp.recommendations(
            seed_genres=seed_genres,
            min_valence=min_valence,
            max_valence=max_valence,
            min_energy=min_arousal,
            max_energy=max_arousal,
            min_danceability=min_danceability,
            max_danceability=max_danceability,
            min_loudness=min_loudness,
            max_loudness=max_loudness,
            limit=10
        )
   
    elif  emotion=="fear":
        min_valence=charac[1]
        max_valence=charac[2]
        min_arousal=charac[3]
        max_arousal=charac[4]
        min_acousticness=charac[5]
        max_acousticness=charac[6]
        min_instrumentalness=charac[7]
        max_instrumentalness=charac[8]
        recommendations = sp.recommendations(
            seed_genres=seed_genres,
            min_valence=min_valence,
            max_valence=max_valence,
            min_energy=min_arousal,
            max_energy=max_arousal,
            min_acousticness=min_acousticness,
            max_acousticness=max_acousticness,
            min_instrumentalness=min_instrumentalness,
            max_instrumentalness=max_instrumentalness,
            limit=10
        )

    else :
        min_valence=charac[1]
        max_valence=charac[2]
        min_arousal=charac[3]
        max_arousal=charac[4]
        recommendations = sp.recommendations(
            seed_genres=seed_genres,
            min_valence=min_valence,
            #max_valence=max_valence,
            min_energy=min_arousal,
            #max_energy=max_arousal,
            limit=1
        )
    return recommendations

#Generate a playlist, its name and uri
def generate_playlist(emotion,results):
    today = date.today()
    print("Today's date:", today)

    day = today.strftime("%m/%d/%y")
    print("Current date =",day)
    playlist_name=emotion.capitalize()+'-'+day

    #send request to make playlist
    playlist_id,playlist_uri=create_playlist(playlist_name,results)

    #return playlist_name for logs on GUI 
    return playlist_name, playlist_id, playlist_uri

#Create a playlist--good
def create_playlist(name,recommendations):
    global sp
    check_and_refresh_token()
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user=user_id, name=name, public=False)

    tracks_id=[]

    for track in recommendations:
        tracks_id.append(track['track_id'])
        #print(f"{track['name']} by {track['artists'][0]['name']}")

    sp.playlist_add_items(playlist_id=playlist['id'], items=tracks_id)
    print(f"Playlist created: {playlist['external_urls']['spotify']}")

    return playlist['id'],playlist['owner']['uri']

#Add tracks to a playlist(track_ids is a list)--good
def add_tracks_to_playlist(playlist_id, track_ids):
    global sp
    check_and_refresh_token()
    sp.playlist_add_items(playlist_id, track_ids,)
    print("Tracks added to playlist.")

#Remove tracks from a playlist(track_ids is a list)--good
def remove_tracks_from_playlist(playlist_id, track_ids):
    global sp
    check_and_refresh_token()
    sp.playlist_remove_all_occurrences_of_items(playlist_id, track_ids)
    print("Tracks removed from playlist.")

#Add song to queue--good
def add_to_queue(track_uri):
    global sp
    check_and_refresh_token()
    sp.add_to_queue(track_uri)
    print("Track added to queue.")

#Start playback / set current song--good
def to_start_playback(track_uri, device_id=None):
    global sp
    check_and_refresh_token()
    sp.start_playback(uris=[track_uri], device_id=device_id)
    print("Playback started.")

#Get preview URL of track--good but never played song--> see if deprecated
def get_preview_url(track_id):
    global sp
    check_and_refresh_token()
    track = sp.track(track_id)
    return track['preview_url']

#Play preview audio (external using pydub)--depends on get_preview_url
def play_preview(track_id):
    preview_url = get_preview_url(track_id)
    if preview_url:
        print(f"Playing preview: {preview_url}")
        response = requests.get(preview_url)
        audio = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
        play(audio)
    else:
        print("No preview available for this track.")

#Get active device--good but never played song--> see if deprecated
def get_devices():
    global sp

    check_and_refresh_token()
    devices = sp.devices()
    if not devices['devices']:
        print("No active devices found. Please open Spotify on your phone, desktop, or web player.")
        return None
    for device in devices['devices']:
        print(f"Name: {device['name']}, ID: {device['id']}, Type: {device['type']}, Active: {device['is_active']}")
    return devices['devices']

#to fix
def get_available_genre_seeds(sp):
    """
    Fetch available genre seeds from the Spotify Web API using Spotipy.
    This bypasses the deprecated sp.recommendation_genre_seeds() method.
    """
    try:
        # Make raw API call to Spotify endpoint
        response = sp._get('recommendations/available-genre-seeds')
        genres = response.get('genres', [])
        
        if not genres:
            print("Warning: No genres returned from Spotify API.")
        return genres
    
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error while fetching genre seeds: {e}")
        return []

def get_top_tracks():
    # Fetch the top 10 tracks of the current user
    results = sp.current_user_top_tracks(limit=10, time_range='medium_term')  # You can change time_range to 'short_term' or 'long_term'
    
    top_tracks = []
    for idx, item in enumerate(results['items']):
        top_tracks.append({
            'rank': idx + 1,
            'track_id':item['id'],
            'track_name': item['name'],
            'artist_name': item['artists'][0]['name'],
            'album_name': item['album']['name'],
            'track_uri': item['uri'],
            'track_url': item['external_urls']['spotify'],
            'track_image': item['album']['images'][0]['url']  # You can access album artwork here
        })
    
    return top_tracks

#store tracks as an easilly treatable format for our main recommender loop
def clean_tracks(results):
    # Fetch the top 10 tracks of the current user
    #results = sp.current_user_top_tracks(limit=10, time_range='medium_term')  # You can change time_range to 'short_term' or 'long_term'
    #

    #result is supposed to be the return value of the re
    all_tracks = []
    for idx, item in enumerate(results['items']):
        all_tracks.append({
            'rank': idx + 1,
            'track_id':item['id'],
            'track_name': item['name'],
            'artist_name': item['artists'][0]['name'],
            'album_name': item['album']['name'],
            'track_uri': item['uri'],
            'track_url': item['external_urls']['spotify'],
            'track_image': item['album']['images'][0]['url']  # You can access album artwork here
        })
    
    return all_tracks

def start_player(all_tracks):
    d=get_devices()
    if len(d)==1:
        device_id=d[0]['id']
    else :
        for device in d:
            if device['is_active']:
                device_id=device['id']
                break
        
    track_uris=[]
    for track in all_tracks:
        track_uris.append(track['track_uri'])
        add_to_queue(track['track_uri'])

    to_start_playback(track_uris[0], device_id=device_id)    

def play_playlist(playlist_uri):
    d=get_devices()
    if len(d)==1:
        device_id=d[0]['id']
    else :
        for device in d:
            if device['is_active']:
                device_id=device['id']
                break
    sp.start_playback(device_id=device_id, context_uri=playlist_uri)

if __name__ == "__main__":
    d=get_devices()
    #print(get_top_tracks())
    add_to_queue('spotify:track:7AFASza1mXqntmGtbxXprO')
    add_to_queue('spotify:track:7CW3Tjll8pUMZxsuo8GZgV')
    #start_playback('spotify:track:1q0qVL7cRYzdWqmLQXpTaC', device_id=d[0]['id'])
    
    
    
   


   



