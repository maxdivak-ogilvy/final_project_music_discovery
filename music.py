import spotipy
import sys
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET
from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_top_five_tracks(what_id):
    # return the selected recommended artists top 5 songs
    preview_top_five = what_id
    results_top_five = spotify.artist_top_tracks(preview_top_five)
    # print(f"-------\nResults_top_five is: {results_top_five}\n-------")
    for tracks in results_top_five['tracks'][:5]:
        print('track    : ' + tracks['name'])
        if tracks['preview_url']==None:
            print('audio    : ' + "None")
        else:
            print('audio    : ' + tracks['preview_url'])
        print('cover art: ' + tracks['album']['images'][0]['url'])
        print()
