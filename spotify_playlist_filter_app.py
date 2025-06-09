import spotipy
import requests
import threading
import tkinter as tk

from PIL import Image, ImageTk
from io import BytesIO

class SpotifyPlaylistFilterApp():
    def __init__(self, spotify_client: spotipy.client.Spotify, playlist_id: str):
        self._spotify_client = spotify_client
        self._playlist_id = playlist_id

        self._root = tk.Tk()
        self._root.attributes("-topmost", True)
        self._root.title("SP-EATER")
        self._root.geometry("350x300")
        self._root.iconbitmap("snorlax.ico")
        self._root.configure(bg="#1e1e1e") 

        self._track_label = tk.Label(self._root, text="", wraplength=300, font=("JetBrains Mono", 10))
        self._image_label = tk.Label(self._root)
        self._check_button = tk.Button(self._root, text="😍  Save! I love <3", width=20, command=self._keep_in_playlist_callback, bg="#20c40e", font=("JetBrains Mono", 12))
        self._delete_button = tk.Button(self._root, text="🚮 DELETE FOREVER", width=20, command=self._remove_from_playlist_callback, bg="#e32012", fg="#ffffff", font=("JetBrains Mono", 12))

        self._track_label.pack(pady=10)
        self._image_label.pack(pady=10)
        self._check_button.pack(pady=5)
        self._delete_button.pack(pady=5)

    def run(self):
        self._update_song()
        self._root.mainloop()

    def _remove_from_playlist_callback(self):
        self._remove_from_playlist_action("", "")

    def _keep_in_playlist_callback(self):
        self._keep_in_playlist_action("", "")

    @staticmethod
    def _handle_song(action: callable):
        def inner(self, track_id, track_name):
            current_track = self._spotify_client.current_playback()
            track_id = current_track["item"]["id"]
            track_name = current_track["item"]["name"]
            action(self, track_id=track_id, track_name=track_name)
            self._spotify_client.next_track()
        return inner

    @_handle_song
    def _remove_from_playlist_action(self, track_id: str, track_name: str):
        track_uri = f"spotify:track:{track_id}"
        self._spotify_client.playlist_remove_all_occurrences_of_items(self._playlist_id, [track_uri])
        print(f"Removed track {track_name}...")

    @_handle_song
    def _keep_in_playlist_action(self, _, track_name: str):
        print(f"Kept track {track_name}!")
    
    def _fetch_song(self):
        current = self._spotify_client.current_playback()
        if current is None:
            self._track_label.config(text="No Track Playing...")
            return

        track_name = current["item"]["name"] 
        track_artist = current["item"]["artists"][0]["name"]
        self._track_label.config(text=f"{track_name} - {track_artist}")

        image_url = current["item"]["album"]["images"][0]["url"]
        img_data = requests.get(image_url).content
        img = Image.open(BytesIO(img_data)).resize((100, 100))
        tk_img = ImageTk.PhotoImage(img)
        self._image_label.config(image=tk_img)
        self._image_label.image = tk_img

    def _update_song(self):
        update_song_thread = threading.Thread(target=self._fetch_song)
        update_song_thread.start()

        self._root.after(1000, self._update_song)
