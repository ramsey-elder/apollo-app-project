from collections import Counter
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Booking Analytics")

BOOKINGS_URL = "http://web-api:4000/bookings"

try:
    resp = requests.get(BOOKINGS_URL)
    if resp.status_code != 200:
        st.error("Failed to fetch booking data.")
        st.stop()

    all_bookings = resp.json()

    buildings = sorted(set(b["building_name"] for b in all_bookings))
    space_types = sorted(set(b["space_type"] for b in all_bookings))

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_building = st.selectbox("Building", ["All"] + buildings)
    with col2:
        selected_space_type = st.selectbox(
            "Space Type",
            ["All"] + [s.replace("_", " ").title() for s in space_types],
        )
    with col3:
        selected_status = st.selectbox(
            "Status", ["All", "active", "completed", "cancelled", "no_show"]
        )

    filtered = all_bookings
    if selected_building != "All":
        filtered = [b for b in filtered if b["building_name"] == selected_building]
    if selected_space_type != "All":
        filtered = [b for b in filtered if b["space_type"].replace("_", " ").title() == selected_space_type]
    if selected_status != "All":
        filtered = [b for b in filtered if b["status"] == selected_status]

    st.divider()
    st.subheader("Summary")
    status_counts = Counter(b["status"] for b in filtered)
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Bookings", len(filtered))
    m2.metric("Active", status_counts.get("active", 0))
    m3.metric("Completed", status_counts.get("completed", 0))
    m4.metric("Cancelled", status_counts.get("cancelled", 0))
    m5.metric("No-Show", status_counts.get("no_show", 0))

    st.divider()
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Bookings by Building")
        building_counts = Counter(b["building_name"] for b in filtered)
        if building_counts:
            st.bar_chart(building_counts)
        else:
            st.write("No data to display.")

    with col_right:
        st.subheader("Bookings by Space Type")
        type_counts = Counter(b["space_type"].replace("_", " ").title() for b in filtered)
        if type_counts:
            st.bar_chart(type_counts)
        else:
            st.write("No data to display.")

    st.divider()
    st.subheader("Cancellation & No-Show Rates")
    total = len(filtered)
    if total > 0:
        cancel_rate = status_counts.get("cancelled", 0) / total * 100
        noshow_rate = status_counts.get("no_show", 0) / total * 100
        r1, r2, r3 = st.columns(3)
        r1.metric("Cancellation Rate", f"{cancel_rate:.1f}%")
        r2.metric("No-Show Rate", f"{noshow_rate:.1f}%")
        r3.metric("Completion Rate", f"{status_counts.get('completed', 0) / total * 100:.1f}%")
    else:
        st.write("No bookings match the selected filters.")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")
