import datetime
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Create New Booking")

# Initialize session state
if "show_success_modal" not in st.session_state:
    st.session_state.show_success_modal = False
if "success_booking_id" not in st.session_state:
    st.session_state.success_booking_id = None
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False
if "form_key_counter" not in st.session_state:
    st.session_state.form_key_counter = 0


@st.dialog("Success")
def show_success_dialog(booking_id):
    st.markdown(f"### Booking #{booking_id} has been successfully created!")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Return to Home", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_booking_id = None
            st.switch_page("pages/00_Student_Home.py")

    with col2:
        if st.button("Create Another Booking", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_booking_id = None
            st.session_state.reset_form = True
            st.rerun()


if st.session_state.reset_form:
    st.session_state.form_key_counter += 1
    st.session_state.reset_form = False

# Fetch spaces from API
try:
    spaces_response = requests.get("http://web-api:4000/spaces")
    if spaces_response.status_code == 200:
        spaces_data = spaces_response.json()
        space_options = {
            s["space_id"]: f"{s['room_name']} ({s['space_type'].replace('_', ' ').title()})"
            for s in spaces_data
        }
    else:
        space_options = {}
        st.warning("Could not load spaces from the server.")
except requests.exceptions.RequestException:
    space_options = {}
    st.warning("Could not connect to the API to load spaces.")

# Fetch clubs from API
try:
    clubs_response = requests.get("http://web-api:4000/clubs")
    if clubs_response.status_code == 200:
        clubs_data = clubs_response.json()
        club_options = {c["club_id"]: c["club_name"] for c in clubs_data}
    else:
        club_options = {}
except requests.exceptions.RequestException:
    club_options = {}

BOOKINGS_API_URL = "http://web-api:4000/bookings"

with st.form(f"new_booking_form_{st.session_state.form_key_counter}"):
    st.subheader("Booking Details")

    if space_options:
        selected_space_name = st.selectbox(
            "Space *",
            options=list(space_options.values()),
        )
    else:
        selected_space_name = st.selectbox("Space *", options=[])
        st.caption("No spaces available.")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date *", value=datetime.date.today())
        start_time = st.time_input("Start Time *", value=datetime.time(9, 0))
    with col2:
        end_date = st.date_input("End Date *", value=datetime.date.today())
        end_time = st.time_input("End Time *", value=datetime.time(10, 0))

    # Optional club association
    club_names = ["— None —"] + list(club_options.values())
    selected_club_name = st.selectbox("Club (optional)", options=club_names)

    submitted = st.form_submit_button("Create Booking")

    if submitted:
        if not space_options:
            st.error("No spaces are available. Please try again later.")
        else:
            time_start = datetime.datetime.combine(start_date, start_time)
            time_end = datetime.datetime.combine(end_date, end_time)

            if time_end <= time_start:
                st.error("End time must be after start time.")
            else:
                space_id = next(k for k, v in space_options.items() if v == selected_space_name)
                creator_id = st.session_state.get("user_id", 1)

                booking_data = {
                    "time_start": time_start.strftime("%Y-%m-%d %H:%M:%S"),
                    "time_end": time_end.strftime("%Y-%m-%d %H:%M:%S"),
                    "space_id": space_id,
                    "creator_id": creator_id,
                }

                if selected_club_name != "— None —":
                    club_id = next(k for k, v in club_options.items() if v == selected_club_name)
                    booking_data["club_id"] = club_id

                try:
                    response = requests.post(BOOKINGS_API_URL, json=booking_data)

                    if response.status_code == 201:
                        st.session_state.show_success_modal = True
                        st.session_state.success_booking_id = response.json().get("booking_id")
                        st.rerun()
                    else:
                        st.error(
                            f"Failed to create booking: {response.json().get('error', 'Unknown error')}"
                        )

                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to the API: {str(e)}")
                    st.info("Please ensure the API server is running.")

if st.session_state.show_success_modal:
    show_success_dialog(st.session_state.success_booking_id)
