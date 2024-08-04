import streamlit as st
from auth.spotted_apple import signup_new_user
from logs.spotted_apple_logger import logger
from navigation import make_sidebar

make_sidebar()

if 'signup_feedback' not in st.session_state:
  st.session_state['signup_feedback'] = None

if 'user_id' not in st.session_state:
  st.session_state['user_id'] = None

st.subheader('Sign up with Spotted Apple :snake::apple:')
st.write('Create an account and begin sharing music!')

sign_up, spacer, spacer_2 = st.columns(3)
with sign_up:
  sign_up = st.form('new_user', clear_on_submit=False, border=False)
  sign_up.text_input(
    label='Email',
    help='Please provide an email for your account.',
    key='signup_email',
    placeholder='example@email.com'
  )
  
  sign_up.text_input(
    label='Password',
    type='password',
    help='Please enter a password for your account.',
    key='signup_password',
  )

  sign_up.text_input(
    label='Password Confirm',
    type='password',
    help='Please confirm the password entered above.',
    key='signup_password_confirm',
  )

  sign_up.form_submit_button(
    label='Create Account',
    on_click=signup_new_user
  )

if st.session_state['signup_feedback'] is not None:
  if st.session_state['signup_feedback']['type'] == 'error':
    st.error(st.session_state['signup_feedback']['message'])
  elif st.session_state['signup_feedback']['type'] == 'info':
    st.info(st.session_state['signup_feedback']['message'])

if st.session_state['user_id']:
  st.switch_page('pages/2_Login.py')
