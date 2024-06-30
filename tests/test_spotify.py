from src.spotify import Spotify

def test_spotify__get_redirect_url():
    spotify = Spotify()
    assert spotify.redirect_uri is not None
