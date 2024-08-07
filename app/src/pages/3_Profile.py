import streamlit as st
from navigation import make_sidebar

make_sidebar()
if not st.session_state.get('is_logged_in', False):
    st.switch_page("Spotted_Apple.py")

st.title('Spotted Apple :apple::snake:')
st.session_state
