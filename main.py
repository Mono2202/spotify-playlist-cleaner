import os
import spotipy

from spotipy.oauth2 import SpotifyOAuth

from spotify_playlist_filter_app import SpotifyPlaylistFilterApp

SPOTIFY_SCOPE = "user-read-playback-state user-read-currently-playing playlist-modify-public playlist-modify-private user-modify-playback-state"


def main():
    spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.environ["SPOTIFY_CLIENT_ID"],
        client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
        redirect_uri=os.environ["SPOTIFY_REDIRECT_URI"],
        scope=SPOTIFY_SCOPE
    ))

    spotify_playlist_filter_app = SpotifyPlaylistFilterApp(
        spotify_client,
        "https://open.spotify.com/playlist/5vkNtdvELKN7HliI9asYNn?si=ca860839a07f439c"
    )
    spotify_playlist_filter_app.run()


if __name__ == "__main__":
    main()
