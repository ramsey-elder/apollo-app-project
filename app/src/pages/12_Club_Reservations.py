import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Club Reservations")

BOOKINGS_URL = "http://web-api:4000/bookings"
CLUBS_URL = "http://web-api:4000/clubs"

try:
    clubs_resp = requests.get(CLUBS_URL)
    if clubs_resp.status_code != 200:
        st.error("Failed to load clubs from the API.")
        st.stop()

    clubs = clubs_resp.json()
    club_options = {c["club_id"]: c["club_name"] for c in clubs}

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_club_name = st.selectbox(
            "Club",
            options=["— Select a club —"] + list(club_options.values()),
        )

    with col2:
        selected_status = st.selectbox(
            "Status",
            ["All", "active", "cancelled", "completed", "no_show"],
        )

    with col3:
        search_query = st.text_input(
            "Search by Space or Booking ID",
            placeholder="e.g. Study Room or 42",
        )

    if selected_club_name == "— Select a club —":
        st.info("Select a club above to view its reservations.")
        st.stop()

    selected_club_id = next(k for k, v in club_options.items() if v == selected_club_name)

    params = {"club_id": selected_club_id}
    if selected_status != "All":
        params["status"] = selected_status

    resp = requests.get(BOOKINGS_URL, params=params)
    if resp.status_code != 200:
        st.error("Failed to fetch reservations from the API.")
        st.stop()

    bookings = resp.json()

    if search_query.strip():
        q = search_query.strip().lower()
        bookings = [
            b for b in bookings
            if q in b["room_name"].lower() or q == str(b["booking_id"])
        ]

    st.write(f"Found **{len(bookings)}** reservation(s) for **{selected_club_name}**")

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

    st.divider()
    if st.button("Create New Booking", type="primary"):
        st.switch_page("pages/04_New_Booking.py")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")
