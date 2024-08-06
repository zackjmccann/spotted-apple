import streamlit as st
from navigation import make_sidebar
from auth.oauth import AuthenticationError
from auth.spotify import SpotifyOAuth
from auth.spotted_apple import save_access_token

make_sidebar()

if st.query_params:
    st.session_state['user_id'] = st.query_params["state"]
    st.session_state['spotify_auth_code'] = st.query_params['code']

try:
    spotify = SpotifyOAuth(state=st.session_state['user_id'])
    access_token_info = spotify.get_access_token_info(st.session_state['spotify_auth_code'])
    access_token = save_access_token('spotify', access_token_info)
    if access_token:
        st.success('Authorized with Spotify!')
        st.write('You can close this window.')

except (AuthenticationError, KeyError):
    st.warning('The authorization information on this page is stale. Please revisit your original session and try agin.')
