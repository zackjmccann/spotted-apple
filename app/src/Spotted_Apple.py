import re
import time
import streamlit as st
from helpers import handle_app_request
from text_blocks import TEXT_BLOCKS
from logs.spotted_apple_logger import logger
from navigation import make_sidebar

logger.debug(f'app running...')
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

make_sidebar()

if 'is_logged_in' not in st.session_state:
  st.session_state['is_logged_in'] = False

st.title('Spotted Apple :apple::snake:')
st.header('Welcome!')
st.write('Share playlist between Spotify and Apple Music.')


# st.subheader('Getting Started')
# st.markdown(TEXT_BLOCKS['request_permission'])

# request_form, spacer, spacer_2 = st.columns(3)

# with request_form:
#   request_permission = st.form('spotted_apple_user', clear_on_submit=True, border=False)
#   request_permission.text_input(
#     label='Spotted Apple Access Request',
#     help='Please provide the email associated with your Spotify account.',
#     key='user_email',
#     placeholder='example@email.com'
#   )
#   request_permission.form_submit_button(
#     label='Request Access',
#     on_click=handle_app_request
#   )

# if st.session_state['app_access_request'] is not None:
#   if st.session_state['app_access_request'] == 'pending':
#     st.info('Thank you for request access. We will notify you when your request is reviewed.')
#   elif st.session_state['app_access_request'] == 'granted':
#     st.success('Access Granted!')
#     redirect_message, countdown, redirect_spacer = st.columns(spec=[3, .5, 4.5])
#     with redirect_message:
#       st.markdown('You are being redirected to the [Spotify authorization page](%s)...' % spotify.authorize(auto_open=False))
#     with countdown:
#       countdown = st.empty()

#       if not st.session_state['auto_redirected']:
#         redirect_delay = 1*5
#         for secs in range(redirect_delay, -1, -1):
#             time_remaining = secs%60
#             countdown.markdown(f'**{time_remaining}**')
#             time.sleep(1)
#         spotify.authorize()
#         st.session_state['auto_redirected'] = True
#     countdown.markdown('')
#     # TODO: Check authorization, get token, and query Spotify!

#   elif st.session_state['app_access_request'] == 'invalid':
#     st.error('Please enter a valid email.')
