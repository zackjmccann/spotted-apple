import os
import re
import streamlit as st

def handle_app_request():
    if validate_email_input():
        if check_if_user_has_app_access():
            st.session_state['app_access_request'] = 'granted'
        else:
            st.session_state['app_access_request'] = 'pending'
    else:
        st.session_state['app_access_request'] = 'invalid'


def check_if_user_has_app_access():
    #TODO: Add check >> store users with development access to redis and validate
    if st.session_state['user_email'] == os.getenv('SPOTIFY_ADMIN'):
        return True
    else:
        return False


def validate_email_input():
  regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

  try:
    if not re.fullmatch(regex, st.session_state['user_email']) or st.session_state['user_email'] == '':
        return False
    else:
        return True

  except TypeError:
        return False
