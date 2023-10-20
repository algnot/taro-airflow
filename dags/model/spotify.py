from .config import Config
from requests import get
from model.errors.spotify_error import SpotifyError

class Spotify():
    token = ""
    playlist_id = ""
    
    def __init__(self):
        config = Config()
        self.token = config.get("SPOTIFY_TOKEN")
        self.playlist_id = config.get("SPOTIFY_PLAYLIST_ID")
        
    def get_count_song_in_playlist(self):
        url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}"
        res = get(url=url, headers={
            "Authorization": f"Bearer {self.token}"
        })
        
        if res.status_code != 200:
            raise SpotifyError(f"Can not get count song in playlist\n{res.text}")
        
        return res.json()["tracks"]["total"]
    
    def get_song_in_playlist_by_index(self, index):
        url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks?offset={index}&limit=1"
        res = get(url=url, headers={
            "Authorization": f"Bearer {self.token}"
        })
        
        if res.status_code != 200:
            raise SpotifyError(f"Can not get song in playlist by index\n{res.text}")
        
        return res.json()["items"][0]["track"]
    