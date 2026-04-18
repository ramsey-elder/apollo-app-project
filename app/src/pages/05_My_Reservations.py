import datetime
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("My Reservations")

BOOKINGS_URL = "http://web-api:4000/bookings"

creator_id = st.session_state.get("user_id", 1)

try:
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_status = st.selectbox("Status", ["All", "active", "cancelled", "completed", "no_show"])
    with col2:
        search_query = st.text_input("Search by Space or Booking ID", placeholder="e.g. Study Room or 42")

    params = {"creator_id": creator_id}
    if selected_status != "All":
        params["status"] = selected_status

    resp = requests.get(BOOKINGS_URL, params=params)
    if resp.status_code != 200:
        st.error("Failed to fetch your reservations.")
        st.stop()

    bookings = resp.json()

    if search_query.strip():
        q = search_query.strip().lower()
        bookings = [b for b in bookings if q in b["room_name"].lower() or q == str(b["booking_id"])]

    st.write(f"Found **{len(bookings)}** reservation(s)")

    for b in bookings:
        status_label = b["status"].replace("_", " ").title()
        header = (
            f"#{b['booking_id']}  ·  {b['room_name']} — {b['building_name']}"
            f"  ·  {status_label}  ·  {b['time_start']} – {b['time_end']}"
        )

        with st.expander(header):
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
                if b["status"] == "active":
                    st.write("**Actions**")

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
                    st.write("**Reschedule**")
                    with st.form(key=f"reschedule_{b['booking_id']}"):
                        new_start_date = st.date_input("New Start Date", value=datetime.date.today())
                        new_start_time = st.time_input("New Start Time", value=datetime.time(9, 0))
                        new_end_date = st.date_input("New End Date", value=datetime.date.today())
                        new_end_time = st.time_input("New End Time", value=datetime.time(10, 0))
                        update_submitted = st.form_submit_button("Update Time")

                        if update_submitted:
                            ts = datetime.datetime.combine(new_start_date, new_start_time)
                            te = datetime.datetime.combine(new_end_date, new_end_time)
                            if te <= ts:
                                st.error("End time must be after start time.")
                            else:
                                upd_resp = requests.put(
                                    f"{BOOKINGS_URL}/{b['booking_id']}",
                                    json={
                                        "time_start": ts.strftime("%Y-%m-%d %H:%M:%S"),
                                        "time_end": te.strftime("%Y-%m-%d %H:%M:%S"),
                                    },
                                )
                                if upd_resp.status_code == 200:
                                    st.success("Booking time updated.")
                                    st.rerun()
                                else:
                                    st.error("Failed to update booking time.")
                else:
                    st.write(f"*This booking is {status_label.lower()} and cannot be modified.*")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")
