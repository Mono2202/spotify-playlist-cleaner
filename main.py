import os
import spotipy
import tkinter as tk

from spotipy.oauth2 import SpotifyOAuth
from tkinter import simpledialog

from spotify_playlist_filter_app import SpotifyPlaylistFilterApp

SPOTIFY_SCOPE = "user-read-playback-state user-read-currently-playing playlist-modify-public playlist-modify-private user-modify-playback-state"

def get_spotify_playlist() -> str:
    input_spotify_playlist_window = tk.Tk()
    input_spotify_playlist_window.withdraw()

    spotify_playlist = simpledialog.askstring(
        title="Spotify Playlist",
        prompt="Insert the Spotify playlist you want to clean: "
    )
    spotify_playlist = spotify_playlist.split("playlist/")[1].split("?si")[0]    
    print(spotify_playlist)

    input_spotify_playlist_window.destroy()
    return spotify_playlist


def main():
    spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.environ["SPOTIFY_CLIENT_ID"],
        client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
        redirect_uri=os.environ["SPOTIFY_REDIRECT_URI"],
        scope=SPOTIFY_SCOPE
    ))

    spotify_playlist = get_spotify_playlist()

    spotify_playlist_filter_app = SpotifyPlaylistFilterApp(
        spotify_client,
        spotify_playlist
    )
    spotify_playlist_filter_app.run()


if __name__ == "__main__":
    main()
