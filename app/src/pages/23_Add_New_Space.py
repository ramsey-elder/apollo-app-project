import datetime
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Add New Bookable Space")

# Initialize session state
if "show_success_modal" not in st.session_state:
    st.session_state.show_success_modal = False
if "success_space_name" not in st.session_state:
    st.session_state.success_space_name = ""
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False
if "form_key_counter" not in st.session_state:
    st.session_state.form_key_counter = 0


@st.dialog("Success")
def show_success_dialog(space_name):
    st.markdown(f"### {space_name} has been successfully added to the system!")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Return to Admin Home", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_space_name = ""
            st.switch_page("pages/20_Admin_Home.py")

    with col2:
        if st.button("Add Another Space", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_space_name = ""
            st.session_state.reset_form = True
            st.rerun()


if st.session_state.reset_form:
    st.session_state.form_key_counter += 1
    st.session_state.reset_form = False

# Fetch buildings from API
try:
    buildings_response = requests.get("http://web-api:4000/buildings")
    if buildings_response.status_code == 200:
        buildings_data = buildings_response.json()
        building_options = {b["building_id"]: b["building_name"] for b in buildings_data}
    else:
        building_options = {}
        st.warning("Could not load buildings from the server.")
except requests.exceptions.RequestException:
    building_options = {}
    st.warning("Could not connect to the API to load buildings.")

SPACES_API_URL = "http://web-api:4000/spaces"

with st.form(f"add_space_form_{st.session_state.form_key_counter}"):
    st.subheader("Space Information")

    room_name = st.text_input("Room Name *")

    space_type = st.selectbox(
        "Space Type *",
        options=["room", "dance_studio", "field", "lecture_hall", "music_studio"],
        format_func=lambda x: x.replace("_", " ").title(),
    )

    if building_options:
        building_name = st.selectbox(
            "Building *",
            options=list(building_options.values()),
        )
    else:
        building_name = st.selectbox("Building *", options=[])
        st.caption("No buildings available — please add a building first.")

    permissions = st.selectbox(
        "Permissions *",
        options=["all", "club"],
        format_func=lambda x: "All Users" if x == "all" else "Club Members Only",
    )

    col1, col2 = st.columns(2)
    with col1:
        availability_start = st.time_input(
            "Availability Start *",
            value=datetime.time(8, 0),
        )
    with col2:
        availability_end = st.time_input(
            "Availability End *",
            value=datetime.time(22, 0),
        )

    size = st.selectbox(
        "Size (optional)",
        options=["", "small", "medium", "large"],
        format_func=lambda x: "— Select —" if x == "" else x.title(),
    )

    submitted = st.form_submit_button("Add Space")

    if submitted:
        if not building_options:
            st.error("No buildings are available. Please add a building before creating a space.")
        elif not all([room_name, space_type, building_name, permissions, availability_start, availability_end]):
            st.error("Please fill in all required fields marked with *")
        elif availability_end <= availability_start:
            st.error("Availability end time must be after start time.")
        else:
            building_id = next(k for k, v in building_options.items() if v == building_name)
            creator_id = st.session_state.get("user_id", 2)

            space_data = {
                "room_name": room_name,
                "space_type": space_type,
                "building_id": building_id,
                "permissions": permissions,
                "availability_start": availability_start.strftime("%H:%M:%S"),
                "availability_end": availability_end.strftime("%H:%M:%S"),
                "creator_id": creator_id,
            }
            if size:
                space_data["size"] = size

            try:
                response = requests.post(SPACES_API_URL, json=space_data)

                if response.status_code == 201:
                    st.session_state.show_success_modal = True
                    st.session_state.success_space_name = room_name
                    st.rerun()
                else:
                    st.error(
                        f"Failed to add space: {response.json().get('error', 'Unknown error')}"
                    )

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {str(e)}")
                st.info("Please ensure the API server is running")

if st.session_state.show_success_modal:
    show_success_dialog(st.session_state.success_space_name)

if st.button("Return to Admin Home"):
    st.switch_page("pages/20_Admin_Home.py")
