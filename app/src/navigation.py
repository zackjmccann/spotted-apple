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
    with st.sidebar:
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/signup.py", label="Sign Up")
            st.page_link("pages/login.py", label="Login")
            st.write("")
            st.write("")
            if st.button("Log out"):
                logout()
        elif get_current_page_name() != "app":
            st.switch_page("app.py")

def logout():
    st.session_state.logged_in = False
    logger.info("Logged out successfully!")
    st.switch_page("app.py")
