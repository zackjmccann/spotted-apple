import streamlit as st
from helpers import signup_new_user
from logs.spotted_apple_logger import logger


if 'signup_attempted' not in st.session_state:
  st.session_state['signup_attempted'] = None

if 'valid_email' not in st.session_state:
  st.session_state['valid_email'] = None


st.subheader('Sign up with Spotted Apple :snake::apple:')
st.write('Create an account and begin sharing music!')

sign_up, spacer, spacer_2 = st.columns(3)
with sign_up:
  sign_up = st.form('new_user', clear_on_submit=True, border=False)
  sign_up.text_input(
    label='Email',
    help='Please provide an email for your account.',
    key='user_email',
    placeholder='example@email.com'
  )
  
  sign_up.text_input(
    label='Password',
    type='password',
    help='Please a password for your account.',
    key='user_password',
  )
  
  sign_up.text_input(
    label='Password Confirm',
    type='password',
    help='Please confirm the password entered above.',
    key='user_password_confirm',
  )

  sign_up.form_submit_button(
    label='Create Account',
    on_click=signup_new_user
  )

if st.session_state['valid_email']:
    st.switch_page("Welcome.py")
else:
    if st.session_state['signup_attempted']:
        if not st.session_state['valid_email']:
            st.error('Please enter a valid email.')
