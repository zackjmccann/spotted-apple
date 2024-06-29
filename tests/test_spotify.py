from src.spotify import Spotify

def test_spotify_authorize():
    spotify = Spotify()
    spotify.authorize()
