from .config import Config
from requests import get, post
from model.errors.spotify_error import SpotifyError


class Spotify():
    token = ""
    playlist_id = ""
    
    def __init__(self):
        config = Config()
        client_id = config.get("SPOTIFY_CLIENT_ID")
        client_secret = config.get("SPOTIFY_CLIENT_SECRET")
        self.token = self.get_access_token(client_id, client_secret)
        self.playlist_id = config.get("SPOTIFY_PLAYLIST_ID")
        
    def get_access_token(self, client_id, client_secret):
        payload = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }
        
        res = post(url="https://accounts.spotify.com/api/token", data=payload)
        
        if res.status_code != 200:
            raise SpotifyError(f"Can not get access token\n{res.text}")
        
        return res.json()["access_token"]
            
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
    