import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome student, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

if st.button('Create a booking',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/04_New_Booking.py')

if st.button('Submit Help Ticket',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/03_New_Help_Ticket.py')



# if st.button('View World Bank Data Visualization',
#              type='primary',
#              use_container_width=True):
#     st.switch_page('pages/01_World_Bank_Viz.py')

# if st.button('View World Map Demo',
#              type='primary',
#              use_container_width=True):
#     st.switch_page('pages/02_Map_Demo.py')
