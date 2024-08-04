import streamlit as st
from navigation import make_sidebar

make_sidebar()

if st.session_state['is_logged_in']:
    st.title('Spotted Apple :apple::snake:')
    st.session_state
    st.header(f'Hello {st.session_state["user_name"]}!')
    st.write(f'Here is your id: {st.session_state["user_id"]}.')
else:
  st.switch_page('pages/2_Login.py')
