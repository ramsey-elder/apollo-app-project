# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has functions to add links to the left sidebar based on the user's role.

import streamlit as st


# ---- General ----------------------------------------------------------------

def home_nav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def about_page_nav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")

def help_ticket_nav():
    st.sidebar.page_link(
        "pages/03_New_Help_Ticket.py", label="Submit Help Ticket", icon="🆘"
    )


# ---- Role: student ------------------------------------------------

def student_home_nav():
    st.sidebar.page_link(
        "pages/00_Student_Home.py", label="Student Home", icon="👤"
    )

def student_booking_nav():
    st.sidebar.page_link(
        "pages/04_New_Student_Booking.py", label="Create Booking", icon="📅"
    )

def student_reservations_nav():
    st.sidebar.page_link(
        "pages/05_My_Reservations.py", label="My Reservations", icon="📋"
    )

def spaces_nav():
    st.sidebar.page_link(
        "pages/11_Spaces.py", label="Browse Spaces", icon="🏢"
    )


# ---- Role: club_rep -----------------------------------------------------

def club_rep_home_nav():
    st.sidebar.page_link(
        "pages/10_Club_Rep_Home.py", label="Club Rep Home", icon="🏠"
    )

def club_booking_nav():
    st.sidebar.page_link(
        "pages/17_New_Club_Booking.py", label="Create Booking", icon="📅"
    )

def club_reservations_nav():
    st.sidebar.page_link(
        "pages/12_Club_Reservations.py", label="Club Reservations", icon="📋"
    )


# ---- Role: data_analyst ----------------------------------------------------

def data_analyst_home_nav():
    st.sidebar.page_link("pages/40_Data_Analyst_Home.py", label="Data Analyst Home", icon="🖥️")


# ---- Role: administrator ----------------------------------------------------

def admin_home_nav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin Home", icon="🖥️")

def user_directory_nav():
    st.sidebar.page_link("pages/22_Users_Directory.py", label="User Directory", icon="👤")

def space_directory_nav():
    st.sidebar.page_link("pages/24_Spaces_Directory.py", label="Space Directory", icon="🏢")

def add_new_space_nav():
    st.sidebar.page_link("pages/23_Add_New_Space.py", label="Add New Space", icon="➕")

def booking_directory_nav():
    st.sidebar.page_link("pages/25_Bookings_Directory.py", label="Booking Directory", icon="📅")

def facility_managers_nav():
    st.sidebar.page_link("pages/26_Facility_Managers.py", label="Facility Managers", icon="📞")

def booking_analytics_nav():
    st.sidebar.page_link("pages/41_Booking_Analytics.py", label="Booking Analytics", icon="📊")

def building_usage_nav():
    st.sidebar.page_link("pages/42_Building_Usage.py", label="Building Usage", icon="🏗️")

def anomaly_report_nav():
    st.sidebar.page_link("pages/43_Anomaly_Report.py", label="Anomaly Report", icon="⚠️")

# ---- Sidebar assembly -------------------------------------------------------

def SideBarLinks(show_home=False):
    """
    Renders sidebar navigation links based on the logged-in user's role.
    The role is stored in st.session_state when the user logs in on Home.py.
    """

    # Logo appears at the top of the sidebar on every page
    st.sidebar.image("assets/logo.png", width=275)

    # If no one is logged in, send them to the Home (login) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        home_nav()

    if st.session_state["authenticated"]:

        if st.session_state["role"] == "student":
            student_home_nav()
            student_booking_nav()
            student_reservations_nav()
            spaces_nav()
            help_ticket_nav()

        if st.session_state["role"] == "club_rep":
            club_rep_home_nav()
            club_booking_nav()
            club_reservations_nav()
            help_ticket_nav()

        if st.session_state["role"] == "data_analyst":
            data_analyst_home_nav()
            booking_analytics_nav()
            building_usage_nav()
            anomaly_report_nav()

        if st.session_state["role"] == "administrator":
            admin_home_nav()
            booking_directory_nav()
            user_directory_nav()
            space_directory_nav()
            add_new_space_nav()
            facility_managers_nav()

    # About link appears at the bottom for all roles
    about_page_nav()

    if st.session_state["authenticated"]:
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
