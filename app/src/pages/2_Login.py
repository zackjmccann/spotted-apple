import streamlit as st
from helpers import login_user
from logs.spotted_apple_logger import logger


if 'login_attempted' not in st.session_state:
  st.session_state['login_attempted'] = None

if 'is_logged_in' not in st.session_state:
  st.session_state['is_logged_in'] = None

st.subheader('Login to Spotted Apple :snake::apple:')

login, spacer, spacer_2 = st.columns(3)
with login:
  login = st.form('existing_user', clear_on_submit=True, border=False)
  login.text_input(
    label='Email',
    help='Please provide the email for your account.',
    key='user_email',
    placeholder='example@email.com'
  )
  
  login.text_input(
    label='Password',
    type='password',
    help='Please a password for your account.',
    key='user_password',
  )
  
  login.form_submit_button(
    label='Login',
    on_click=login_user
  )

if st.session_state['is_logged_in']:
    st.switch_page("Profile.py")
else:
    if st.session_state['login_attempted']:
        if not st.session_state['is_logged_in']:
            st.error('Sorry, we could not log you in.')
