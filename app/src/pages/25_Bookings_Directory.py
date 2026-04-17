import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Initialize sidebar
SideBarLinks()

st.title("Bookings Directory")

# API endpoints
BOOKINGS_URL = "http://web-api:4000/bookings"
CLUBS_URL = "http://web-api:4000/clubs"


try:
    # --- Filter / sort controls ---
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_status = st.selectbox(
            "Status",
            ["active", "All", "cancelled", "completed", "no_show"],
        )
    with col3:
        search_query = st.text_input(
            "Search by Space or Booking ID",
            placeholder="e.g. Study Room or 42",
        )

    # --- Fetch bookings ---
    params = {}
    if selected_status != "All":
        params["status"] = selected_status

    resp = requests.get(BOOKINGS_URL, params=params)
    if resp.status_code != 200:
        st.error("Failed to fetch booking data from the API.")
        st.stop()

    bookings = resp.json()

    # Build club id -> name lookup
    clubs_resp = requests.get(CLUBS_URL)
    club_names = (
        {c["club_id"]: c["club_name"] for c in clubs_resp.json()}
        if clubs_resp.status_code == 200 else {}
    )

    # --- Building filter ---
    building_names = sorted(set(b["building_name"] for b in bookings))
    with col2:
        selected_building = st.selectbox("Building", ["All"] + building_names)

    # --- Space filter scoped to selected building ---
    if selected_building != "All":
        space_names = sorted(
            set(b["room_name"] for b in bookings if b["building_name"] == selected_building)
        )
    else:
        space_names = sorted(set(b["room_name"] for b in bookings))
    with col1:
        selected_space = st.selectbox("Space", ["All"] + space_names)

    # --- Apply filters ---
    if selected_building != "All":
        bookings = [b for b in bookings if b["building_name"] == selected_building]

    if selected_space != "All":
        bookings = [b for b in bookings if b["room_name"] == selected_space]

    if search_query.strip():
        q = search_query.strip().lower()
        bookings = [
            b for b in bookings
            if q in b["room_name"].lower() or q == str(b["booking_id"])
        ]

    # --- Results ---
    st.write(f"Found **{len(bookings)}** booking(s)")

    for b in bookings:
        status_label = b["status"].replace("_", " ").title()
        header = (
            f"#{b['booking_id']}  ·  {b['room_name']} — {b['building_name']}"
            f"  ·  {status_label}  ·  {b['time_start']} – {b['time_end']}"
        )

        with st.expander(header):
            detail_resp = requests.get(f"{BOOKINGS_URL}/{b['booking_id']}")
            detail = detail_resp.json() if detail_resp.status_code == 200 else {}
            participants = detail.get("participants", [])
            manager = next((p for p in participants if p.get("managing")), None)
            non_managers = [p for p in participants if not p.get("managing")]

            left_col, right_col = st.columns(2)

            with left_col:
                st.write("**Booking Details**")
                st.write(f"**Booking ID:** {b['booking_id']}")
                st.write(f"**Space:** {b['room_name']} ({b['space_type'].replace('_', ' ').title()})")
                st.write(f"**Building:** {b['building_name']}")
                st.write(f"**Status:** {status_label}")
                st.write(f"**Start:** {b['time_start']}")
                st.write(f"**End:** {b['time_end']}")

                if b.get("club_id"):
                    st.write("")
                    st.write("**Associated Club**")
                    st.write(club_names.get(b["club_id"], f"Club {b['club_id']}"))

            with right_col:
                st.write("**Managing User**")
                if manager:
                    st.write(f"**Name:** {manager['f_name']} {manager['l_name']}")
                    st.write(f"**Email:** {manager.get('email', 'N/A')}")
                else:
                    st.write("No managing user on record.")

                st.write("")
                st.write("**Participants**")
                if non_managers:
                    for p in non_managers:
                        st.write(f"- {p['f_name']} {p['l_name']}")
                else:
                    st.write("No additional participants.")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")
