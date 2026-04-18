import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome Data Analyst, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

if st.button('Booking Analytics',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/41_Booking_Analytics.py')

if st.button('Building Usage',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/42_Building_Usage.py')

if st.button('Anomaly Report',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/43_Anomaly_Report.py')
