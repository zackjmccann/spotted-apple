import streamlit as st
from navigation import make_sidebar
from auth.spotify import SpotifyOAuth
from auth.spotted_apple import save_access_token

make_sidebar()

st.session_state['user_id'] = st.query_params["state"]
st.session_state['spotify_auth_code'] = st.query_params['code']

spotify = SpotifyOAuth(state=st.session_state['user_id'])
access_token_info = spotify.get_access_token_info(st.session_state['spotify_auth_code'])
access_token = save_access_token('spotify', access_token_info)

if access_token:
    st.success('Authorized with Spotify!')
    st.write('You can close this window.')
else:
    st.error('Unable to authorize Spotify. Please try again.')
