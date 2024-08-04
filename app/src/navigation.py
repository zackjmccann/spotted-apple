import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
from logs.spotted_apple_logger import logger


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")
    pages = get_pages("")
    return pages[ctx.page_script_hash]["page_name"]

def make_sidebar():
    if 'is_logged_in' not in st.session_state:
        st.session_state['is_logged_in'] = False

    with st.sidebar:
        st.title('Spotted Apple :apple::snake:')
        st.write('')
        st.write('')

        if st.session_state.get("is_logged_in", False):
            st.page_link("Spotted_Apple.py", label="Home")
            st.page_link("pages/3_Profile.py", label="Profile")
            st.write("")
            st.write("")
            if st.button("Log out"):
                logout()

        else:
            st.page_link("Spotted_Apple.py", label="Home")
            st.page_link("pages/1_Signup.py", label="Sign Up")
            st.page_link("pages/2_Login.py", label="Login")
            st.write("")
            st.write("")

def logout():
    st.session_state['is_logged_in'] = False
    del st.session_state['user_id']
    del st.session_state['user_email']

    logger.info("Logged out successfully!")
    st.switch_page("Spotted_Apple.py")
