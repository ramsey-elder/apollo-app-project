import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
    This is Apollo Booking, a campus space reservation platform developed for CS 3200 at Northeastern University.

    The app demonstrates a full-stack data-driven application that centralizes facility booking across campus, using Streamlit for the frontend and Flask for the backend API, backed by a MySQL database. 

    This project was developed by Team Rocket: Brandon Zau, Alayna Fu, Nicholas Lee, Ramsey Elder, and Michael Jia.
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
