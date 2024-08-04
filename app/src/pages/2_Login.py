import streamlit as st
from auth.spotted_apple import login_user
from logs.spotted_apple_logger import logger
from navigation import make_sidebar

make_sidebar()

if 'login_attempted' not in st.session_state:
  st.session_state['login_attempted'] = False

if 'is_logged_in' not in st.session_state:
  st.session_state['is_logged_in'] = False

st.subheader('Login to Spotted Apple :snake::apple:')

login, spacer, spacer_2 = st.columns(3)
with login:
  login = st.form('existing_user', clear_on_submit=True, border=False)
  login.text_input(
    label='Email',
    help='Please provide the email for your account.',
    key='login_email',
    placeholder='example@email.com'
  )
  
  login.text_input(
    label='Password',
    type='password',
    help='Please a password for your account.',
    key='login_password',
  )
  
  login.form_submit_button(
    label='Login',
    on_click=login_user
  )

if st.session_state.get('login_attempted', False):
  del st.session_state['login_attempted']

  if st.session_state['is_logged_in']:
    st.success('Logged in!')
    st.switch_page('pages/3_Profile.py')

  else:
    if st.session_state['login_failed']:
      del st.session_state['login_failed']
      st.error('Incorrect username or password.')
