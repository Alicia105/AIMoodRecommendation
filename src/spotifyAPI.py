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

load_dotenv("../.env")
clientID=os.getenv("SPOTIPY_CLIENT_ID")
clientSecret=os.getenv("SPOTIPY_CLIENT_SECRET")
clientRedirectURI=os.getenv("SPOTIPY_REDIRECT_URI")


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=clientID,
    client_secret=clientSecret,
    redirect_uri=clientRedirectURI,
    scope="playlist-modify-public playlist-modify-private user-modify-playback-state user-read-playback-state user-read-currently-playing"
))

me = sp.me()
print(f"Logged in as: {me['display_name']}")

# Get available genres
#genres = sp.recommendation_genre_seeds()
#print(genres['genres'])

def giveRecommendations(emotion):
    global sp

    genres = mapping.map_seed_genres_to_emotion(emotion)
    if genres:
        seed_genres = random.sample(genres, min(5, len(genres)))
    else:
        raise ValueError(f"No genres available for emotion '{emotion}'")
    
    seed_genres = random.sample(genres, min(5, len(genres)))
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
            max_valence=max_valence,
            min_energy=min_arousal,
            max_energy=max_arousal,
            limit=10
        )
    return recommendations

def generate_playlist(emotion):
    today = date.today()
    print("Today's date:", today)

    day = today.strftime("%m/%d/%y")
    print("Current date =",day)
    playlist_name=emotion.capitalize()+'-'+day

    #get mood mapping parameters
    recs=giveRecommendations(emotion)

    #send request to make playlist
    create_playlist(playlist_name,recs)

    #return playlist_name for logs on GUI 
    return playlist_name   

def create_playlist(name,recommendations):
    global sp
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user=user_id, name=name, public=False)

    tracks_id=[]

    for track in recommendations['tracks']:
        tracks_id.append(track['id'])
        #print(f"{track['name']} by {track['artists'][0]['name']}")

    sp.playlist_add_items(playlist_id=playlist['id'], items=tracks_id)
    print(f"Playlist created: {playlist['external_urls']['spotify']}")

#Add tracks to a playlist
def add_tracks_to_playlist(playlist_id, track_ids):
    sp.playlist_add_items(playlist_id, track_ids)
    print("Tracks added to playlist.")

#Remove tracks from a playlist
def remove_tracks_from_playlist(playlist_id, track_ids):
    sp.playlist_remove_all_occurrences_of_items(playlist_id, track_ids)
    print("Tracks removed from playlist.")

#Add song to queue
def add_to_queue(track_uri):
    sp.add_to_queue(track_uri)
    print("Track added to queue.")

#Start playback / set current song
def start_playback(track_uri, device_id=None):
    sp.start_playback(uris=[track_uri], device_id=device_id)
    print("Playback started.")

#Get preview URL of track
def get_preview_url(track_id):
    track = sp.track(track_id)
    return track['preview_url']

#Play preview audio (external using pydub)
def play_preview(track_id):
    preview_url = get_preview_url(track_id)
    if preview_url:
        print(f"Playing preview: {preview_url}")
        response = requests.get(preview_url)
        audio = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
        play(audio)
    else:
        print("No preview available for this track.")

def get_devices():
    devices = sp.devices()
    if not devices['devices']:
        print("No active devices found. Please open Spotify on your phone, desktop, or web player.")
        return None
    for device in devices['devices']:
        print(f"Name: {device['name']}, ID: {device['id']}, Type: {device['type']}, Active: {device['is_active']}")
    return devices['devices']

if __name__ == "__main__":
    generate_playlist("joy")



"""sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=clientID,
    client_secret=clientSecret,
    redirect_uri=clientRedirectURI,
    scope='user-library-read'
))

# Get recommendations
recommendations = sp.recommendations(seed_genres=['pop'],
                                     limit=10,
                                     target_danceability=0.8,
                                     target_energy=0.8)

# Print track names
for track in recommendations['tracks']:
    name = track['name']
    artist = track['artists'][0]['name']
    danceability = sp.audio_features([track['id']])[0]['danceability']
    energy = sp.audio_features([track['id']])[0]['energy']
    print(f"{name} by {artist} → Danceability: {danceability}, Energy: {energy}")"""