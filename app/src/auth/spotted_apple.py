import re
import psycopg
import streamlit as st
from db.spotted_apple_db import SpottedAppleDB
from logs.spotted_apple_logger import logger

def validate_email_input():
    logger.debug(f'validating email: {st.session_state["signup_email"]}')
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    try:
        if not re.fullmatch(regex, st.session_state['signup_email']) or st.session_state['signup_email'] == '':
            return False
        else:
            return True

    except TypeError:
            return False

def validate_entered_passwords():
    try:
        assert st.session_state['signup_password'] == st.session_state['signup_password_confirm']
        return True
    except AssertionError:
        return False

def validate_signup_form():
    try:
        assert validate_email_input()
    except AssertionError:
        return 'Please enter a valild email.'
    
    try:
        assert validate_entered_passwords()
    except AssertionError:
        return 'The provided password fields do not match.'

def signup_new_user():
    form_invalidity = validate_signup_form()
    if form_invalidity:
        st.session_state['signup_feedback'] = {'type': 'error', 'message': form_invalidity}
    else:
        spotted_apple_db = SpottedAppleDB()
        new_user = (st.session_state['signup_email'], st.session_state['signup_password'])
        st.session_state['user_id'] = spotted_apple_db.create_new_user(new_user)
        if isinstance(st.session_state['user_id'], psycopg.errors.UniqueViolation):
            del st.session_state['user_id']
            st.session_state['signup_feedback'] = {
                'type': 'error',
                'message': 'An account with that email already exists. Please login.'
                }
        else:
            st.session_state['signup_feedback'] = {
                'type': 'info',
                'message': 'Creating account...'
                }

def login_user():
    st.session_state['login_attempted'] = True
    spotted_apple_db = SpottedAppleDB()
    try:
        user_data = spotted_apple_db.get_user(st.session_state['login_email'])
        if spotted_apple_db.verify_password(st.session_state['login_password'], user_data[2]):
            st.session_state['user_id'] = user_data[0]
            st.session_state['user_email'] = user_data[1]
            st.session_state['user_name'] = user_data[1].split('@')[0]
            st.session_state['is_logged_in'] = True
            clear_login_and_signup_data()
        else:
            st.session_state['login_failed'] = True
    except IndexError:
        logger.info(f'User not found: {st.session_state["login_email"]}')
        st.session_state['login_failed'] = True

def clear_login_and_signup_data():
    """
    This is called once a user is successfully logged in.

    The session state variables associated with signing up and/or logging in
    are no longer needed for the activate session, and are therefore removed.
    """
    signup_and_login_keys = [
        'signup_feedback',
        'signup_email',
        'signup_password',
        'signup_password_confirm',
        'login_email',
        'login_password',
        # 'login_attempted',
        # 'login_failed'
        ]

    for signup_and_login_key in signup_and_login_keys:
        try:
            del st.session_state[signup_and_login_key]
        except KeyError:
            logger.debug(f'Sign up or Login key not found: {signup_and_login_key}')

def add_spotify_authorization_data():
    """Associate a Spotify Authorization Code and Refresh Token with a user"""
    spotted_apple_db = SpottedAppleDB()
    try:
        refresh_token = spotted_apple_db.add_spotify_authorization_data(
            user_id=st.session_state['user_id'],
            auth_code=st.session_state['spotify_auth_code'],
            refresh_token=st.session_state['spotify_refresh_token'])
        return refresh_token
    except psycopg.errors.ForeignKeyViolation as err:
            return err
