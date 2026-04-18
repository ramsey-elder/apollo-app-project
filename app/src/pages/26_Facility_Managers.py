import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Facility Managers")

MANAGERS_URL = "http://web-api:4000/facility_managers"
BUILDINGS_URL = "http://web-api:4000/buildings"

try:
    buildings_resp = requests.get(BUILDINGS_URL)
    buildings = buildings_resp.json() if buildings_resp.status_code == 200 else []
    building_options = {b["building_id"]: b["building_name"] for b in buildings}

    col1, col2 = st.columns([1, 2])
    with col1:
        selected_building_name = st.selectbox(
            "Filter by Building",
            ["All"] + list(building_options.values()),
        )
    with col2:
        search_query = st.text_input(
            "Search by Name or Email",
            placeholder="e.g. Smith or smith@neu.edu",
        )

    params = {}
    if selected_building_name != "All":
        bid = next(k for k, v in building_options.items() if v == selected_building_name)
        params["building_id"] = bid

    resp = requests.get(MANAGERS_URL, params=params)
    if resp.status_code != 200:
        st.error("Failed to fetch facility manager data.")
        st.stop()

    managers = resp.json()

    if search_query.strip():
        q = search_query.strip().lower()
        managers = [
            m for m in managers
            if q in m["f_name"].lower()
            or q in m["l_name"].lower()
            or q in f"{m['f_name']} {m['l_name']}".lower()
            or q in (m.get("email") or "").lower()
        ]

    st.write(f"Found **{len(managers)}** facility manager(s)")

    for m in managers:
        with st.expander(f"{m['f_name']} {m['l_name']} — {m['building_name']}"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.write("**Contact Information**")
                st.write(f"**Name:** {m['f_name']} {m['l_name']}")
                st.write(f"**Email:** {m.get('email', 'N/A')}")
                st.write(f"**Phone:** {m.get('phone') or 'N/A'}")
            with col_b:
                st.write("**Assignment**")
                st.write(f"**Building:** {m['building_name']}")
                st.write(f"**Manager ID:** {m['manager_id']}")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")
