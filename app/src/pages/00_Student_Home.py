import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome student, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

if st.button('Create a Booking',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/04_New_Student_Booking.py')

if st.button('My Reservations',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/05_My_Reservations.py')

if st.button('Browse Spaces',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/11_Spaces.py')

if st.button('Submit Help Ticket',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/03_New_Help_Ticket.py')
