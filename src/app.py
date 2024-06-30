import re
import time
import streamlit as st
from helpers import handle_app_request
from spotify import Spotify

st.set_page_config(
  page_title="Spotted Apple",
  page_icon=":headphones:",
  layout="wide",
  initial_sidebar_state="expanded",
  menu_items={
    'About': 'https://github.com/zackjmccann/spotted-apple',
    'Get Help': "https://github.com/zackjmccann/spotted-apple/blob/master/README.md",
    'Report a Bug': "https://github.com/zackjmccann/spotted-apple/issues"
    }
  )

spotify = Spotify()
if 'app_access_request' not in st.session_state:
  st.session_state['app_access_request'] = None

if 'auto_redirected' not in st.session_state:
  st.session_state['auto_redirected'] = False

st.title('Spotted Apple :apple::snake:')
st.header('Welcome!')
st.write('Spotted Apple helps transfers playlists from Spotify to Apple Music.')

st.subheader('How it Works')
how_it_works_text = """
**Spotted Apple** downloads all playlists on your Spotify Account and dumps the contents into a 
Google Sheet, with each sheet representing a playlist. You can select, review, edit, and delete the playlists you 
would like transferred to Apple Music (**Note:** Spotify and Apple  Music tracks are not always aligned, 
and sometimes need to be interpolated. Additions to playlists are best administered  via your Spotify 
account.) Once each playlist is configured as desired, simply click "Transfer Playlists" and Spotted Apple 
will load all playlists from the Google Sheet into your Apple Music account!

"""
st.markdown(how_it_works_text)

st.subheader('Getting Started')
request_permission_text = """
Before you can authorize Spotted Apple to access your Spotify account, you must be added as a 
user of the application. In order to request access to Spotted Apple, please enter your email below:
"""
st.markdown(request_permission_text)

request_form, spacer, spacer_2 = st.columns(3)

with request_form:
  request_permission = st.form('spotted_apple_user', clear_on_submit=True, border=False)
  request_permission.text_input(
    label='Spotted Apple Access Request',
    help='Please provide the email associated with your Spotify account.',
    key='user_email',
    placeholder='example@email.com'
  )
  request_permission.form_submit_button(
    label='Request Access',
    on_click=handle_app_request
  )

if st.session_state['app_access_request'] is not None:
  if st.session_state['app_access_request'] == 'pending':
    st.info('Thank you for request access. We will notify you when your request is reviewed.')
  elif st.session_state['app_access_request'] == 'granted':
    st.success('Access Granted!')
    redirect_message, countdown, redirect_spacer = st.columns(spec=[3, .5, 4.5])
    with redirect_message:
      st.markdown('You are being redirected to the [Spotify authorization page](%s)...' % spotify.authorize(auto_open=False))
    with countdown:
      countdown = st.empty()

      if not st.session_state['auto_redirected']:
        redirect_delay = 1*5
        for secs in range(redirect_delay, -1, -1):
            time_remaining = secs%60
            countdown.markdown(f'**{time_remaining}**')
            time.sleep(1)
        spotify.authorize()
        st.session_state['auto_redirected'] = True
    countdown.markdown('')
    # TODO: Check authorization, get token, and query Spotify!

  elif st.session_state['app_access_request'] == 'invalid':
    st.error('Please enter a valid email.')
