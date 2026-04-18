import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome Club Representative, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

if st.button('Create a Booking',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/17_New_Club_Booking.py')

if st.button('View Reservations',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/12_Club_Reservations.py')

if st.button('View Spaces',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/11_Spaces.py')

if st.button('Submit Help Ticket',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/03_New_Help_Ticket.py')
