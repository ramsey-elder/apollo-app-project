import datetime
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Bookings Directory")

BOOKINGS_URL = "http://web-api:4000/bookings"
CLUBS_URL = "http://web-api:4000/clubs"


try:
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

    params = {}
    if selected_status != "All":
        params["status"] = selected_status

    resp = requests.get(BOOKINGS_URL, params=params)
    if resp.status_code != 200:
        st.error("Failed to fetch booking data from the API.")
        st.stop()

    bookings = resp.json()

    clubs_resp = requests.get(CLUBS_URL)
    club_names = (
        {c["club_id"]: c["club_name"] for c in clubs_resp.json()}
        if clubs_resp.status_code == 200 else {}
    )

    building_names = sorted(set(b["building_name"] for b in bookings))
    with col2:
        selected_building = st.selectbox("Building", ["All"] + building_names)

    if selected_building != "All":
        space_names = sorted(
            set(b["room_name"] for b in bookings if b["building_name"] == selected_building)
        )
    else:
        space_names = sorted(set(b["room_name"] for b in bookings))
    with col1:
        selected_space = st.selectbox("Space", ["All"] + space_names)

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

            info_col, people_col, action_col = st.columns(3)

            with info_col:
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

            with people_col:
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

            with action_col:
                st.write("**Admin Actions**")

                if b["status"] == "active":
                    if st.button("Cancel Booking", key=f"cancel_{b['booking_id']}", type="secondary"):
                        cancel_resp = requests.put(
                            f"{BOOKINGS_URL}/{b['booking_id']}",
                            json={"status": "cancelled"},
                        )
                        if cancel_resp.status_code == 200:
                            st.success("Booking cancelled.")
                            st.rerun()
                        else:
                            st.error("Failed to cancel booking.")

                    st.write("")
                    with st.form(key=f"reschedule_{b['booking_id']}"):
                        st.write("**Reschedule**")
                        new_start_date = st.date_input("New Start Date", value=datetime.date.today())
                        new_start_time = st.time_input("New Start Time", value=datetime.time(9, 0))
                        new_end_date = st.date_input("New End Date", value=datetime.date.today())
                        new_end_time = st.time_input("New End Time", value=datetime.time(10, 0))
                        if st.form_submit_button("Update Time"):
                            ts = datetime.datetime.combine(new_start_date, new_start_time)
                            te = datetime.datetime.combine(new_end_date, new_end_time)
                            if te <= ts:
                                st.error("End time must be after start time.")
                            else:
                                upd = requests.put(
                                    f"{BOOKINGS_URL}/{b['booking_id']}",
                                    json={
                                        "time_start": ts.strftime("%Y-%m-%d %H:%M:%S"),
                                        "time_end": te.strftime("%Y-%m-%d %H:%M:%S"),
                                    },
                                )
                                if upd.status_code == 200:
                                    st.success("Time updated.")
                                    st.rerun()
                                else:
                                    st.error("Failed to update.")

                st.write("")
                if st.button("Delete Booking", key=f"delete_{b['booking_id']}", type="primary"):
                    del_resp = requests.delete(f"{BOOKINGS_URL}/{b['booking_id']}")
                    if del_resp.status_code == 200:
                        st.success("Booking deleted.")
                        st.rerun()
                    else:
                        st.error("Failed to delete booking.")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")
