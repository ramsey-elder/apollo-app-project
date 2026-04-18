import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Building Usage")
st.write("Buildings ranked by total booking count. Low counts may indicate underused locations worth recommending.")

BUILDINGS_URL = "http://web-api:4000/buildings/buildings"

try:
    resp = requests.get(BUILDINGS_URL)
    if resp.status_code != 200:
        st.error("Failed to fetch building usage data.")
        st.stop()

    buildings = resp.json()

    counts = [b["booking_count"] for b in buildings]
    median_count = sorted(counts)[len(counts) // 2] if counts else 0
    underused_threshold = max(median_count // 2, 1)

    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("Search by building name", placeholder="e.g. Snell Library")
    with col2:
        show_underused_only = st.checkbox("Show underused buildings only")

    filtered = buildings
    if search.strip():
        q = search.strip().lower()
        filtered = [b for b in filtered if q in b["building_name"].lower()]
    if show_underused_only:
        filtered = [b for b in filtered if b["booking_count"] <= underused_threshold]

    st.write(f"Showing **{len(filtered)}** building(s) — sorted ascending by booking count")

    for b in filtered:
        is_underused = b["booking_count"] <= underused_threshold
        label = f"{'⚠️ ' if is_underused else ''}{b['building_name']} — {b['booking_count']} booking(s)"
        with st.expander(label):
            col_a, col_b = st.columns(2)
            with col_a:
                st.write("**Location**")
                st.write(f"**Building:** {b['building_name']}")
                address_parts = [b.get('street', ''), b.get('city', ''), b.get('state', ''), str(b.get('zip', ''))]
                st.write(f"**Address:** {', '.join(p for p in address_parts if p)}")
            with col_b:
                st.write("**Usage**")
                st.write(f"**Total Bookings:** {b['booking_count']}")
                if is_underused:
                    st.warning("Underused — consider recommending as an alternative to high-demand spaces.")

    st.divider()
    st.subheader("Booking Count by Building")
    chart_data = {b["building_name"]: b["booking_count"] for b in buildings}
    if chart_data:
        st.bar_chart(chart_data)

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")
