import streamlit as st
from navigation import make_sidebar
from auth.spotify import SpotifyOAuth
from auth.spotted_apple import get_access_token

make_sidebar()
if not st.session_state.get('is_logged_in', False):
    st.switch_page("Spotted_Apple.py")

spotify = SpotifyOAuth(state=st.session_state['user_id'])

if 'spotify_access_token' not in st.session_state:
    st.session_state['spotify_access_token'] = get_access_token('spotify', st.session_state['user_id'])

st.title('Settings :gear:')

st.header('Account Authorizations')
spotify_widget, apple_widget = st.columns(2)

with spotify_widget:
    st.subheader('Spotify')
    if not st.session_state['spotify_access_token']:
        st.button(
            label='Authorize',
            on_click=spotify.authorize)
    else:
        st.info('You have authorized access to Spotify.')
        st.button(
            label='Refresh Token',
            on_click=spotify.refresh_access_token)

with apple_widget:
    st.subheader('Apple Music')
    st.button(
        label='Authorize',
        key='apple_music_auth')

st.write('##')
st.write('##')
if st.button('Refresh Authorizations'):
    st.rerun()
