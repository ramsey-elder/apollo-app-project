import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
    This is a demo app for the CS3200 Intro to Database course at Northeastern University.

    The focus of this project is to demonstrate how to build a full-stack application that interacts with a MySQL database, using Streamlit for the frontend and Flask for the backend API.

    This project was developed by ___.
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
