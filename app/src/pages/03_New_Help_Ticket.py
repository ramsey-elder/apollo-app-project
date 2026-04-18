import datetime
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Initialize sidebar
SideBarLinks()

st.title("Submit Help Ticket")

