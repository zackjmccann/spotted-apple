import re
import psycopg
import streamlit as st
from src.db.spotted_apple_db import SpottedAppleDB


def validate_email_input():
    logger.debug(f'validating email: {st.session_state["user_email"]}')
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    try:
        if not re.fullmatch(regex, st.session_state['user_email']) or st.session_state['user_email'] == '':
            return False
        else:
            return True

    except TypeError:
            return False

def validate_entered_passwords():
    logger.debug(f'validating passwords: {st.session_state["user_password"]}, {st.session_state["user_password_confirm"]}')
    try:
        assert st.session_state['user_password'] == st.session_state['user_password_confirm']
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
        new_user = (st.session_state['user_email'], st.session_state['user_password'])
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
        user_data = spotted_apple_db.get_user(st.session_state['user_email'])
        if spotted_apple_db.verify_password(st.session_state['user_password'], user_data[2]):
            st.session_state['user_id'] = user_data[0]
            st.session_state['user_email'] = user_data[1]
            st.session_state['is_logged_in'] = True
        else:
            st.session_state['login_failed'] = True
    except IndexError:
        st.session_state['login_failed'] = True
