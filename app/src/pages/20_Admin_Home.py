import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome System Admin, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

if st.button('View Booking Directory',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/25_Bookings_Directory.py')

if st.button('View User Directory',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/22_Users_Directory.py')

if st.button('View Space Directory',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/24_Spaces_Directory.py')

if st.button('Add New Space',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/23_Add_New_Space.py')

if st.button('Facility Managers',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/26_Facility_Managers.py')
