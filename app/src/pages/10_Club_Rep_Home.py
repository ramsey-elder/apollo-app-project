import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Club Representative, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

if st.button('View Reservations',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/11_Club_Reservations.py')

if st.button('View Spaces',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/11_Spaces.py')
