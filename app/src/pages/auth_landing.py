import streamlit as st
from navigation import make_sidebar
from auth.spotify import SpotifyOAuth
from auth.spotted_apple import get_access_token

make_sidebar()

st.session_state['user_id'] = st.query_params["state"]
st.session_state['spotify_auth_code'] = st.query_params['code']

access_token_info = spotify.get_access_token(st.session_state['spotify_auth_code'])

if access_token_info:
    pass # TODO: Call spotted_apple function to store token data

st.header('Authorized with Spotify!')
st.write('You can close this window.')
