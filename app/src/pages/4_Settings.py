import streamlit as st
from navigation import make_sidebar
from auth.spotify import SpotifyOAuth
from auth.apple_music import authorize_apple_music

make_sidebar()
if not st.session_state.get('is_logged_in', False):
    st.switch_page("Spotted_Apple.py")

spotify = SpotifyOAuth(user_id=st.session_state['user_id'])

if 'spotify_auth' not in st.session_state:
    st.session_state['spotify_auth'] = False
if 'apple_music_auth' not in st.session_state:
    st.session_state['apple_music_auth'] = False

st.title('Spotted Apple :apple::snake:')

st.header('Account Authorizations')
spotify_widget, apple_widget = st.columns(2)

with spotify_widget:
    # TODO: Write the user_id to local storage, that way when the authorization occurs, you can reference
    # TODO: the logged in user in the auth_landing page, associate the token with the account on the
    # TODO: backend, then refresh the session with the authoriation token.

    st.subheader('Spotify')
    if not st.session_state['spotify_auth']:
        st.button(
            label='Authorize',
            key='spotify_auth_2',
            on_click=spotify.authorize)

with apple_widget:
    st.subheader('Apple Music')
    if not st.session_state['apple_music_auth']:
        st.button(
            label='Authorize',
            key='apple_music_auth_2',
            on_click=authorize_apple_music)
