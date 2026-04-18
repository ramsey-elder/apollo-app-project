import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Initialize sidebar
SideBarLinks()

st.title("Space Directory")

# API endpoints
SPACES_URL = "http://web-api:4000/spaces"
MANAGERS_URL = "http://web-api:4000/facility_managers"

try:
    response = requests.get(SPACES_URL)
    if response.status_code == 200:
        spaces = response.json()

        managers_by_building = {}
        mgr_resp = requests.get(MANAGERS_URL)
        if mgr_resp.status_code == 200:
            for m in mgr_resp.json():
                managers_by_building[m["building_id"]] = m

        # Extract unique values for filter options
        space_types = sorted(set(s["space_type"] for s in spaces))
        buildings   = sorted(set(s["building_name"] for s in spaces if s.get("building_name")))
        sizes       = sorted(set(s["size"] for s in spaces if s.get("size")))
        permissions = sorted(set(s["permissions"] for s in spaces if s.get("permissions")))
        amenity_keys = ["whiteboard", "screen", "desks", "sound_system", "tables_avail", "camera"]
        amenity_labels = {
            "whiteboard": "Whiteboard",
            "screen": "Screen",
            "desks": "Desks",
            "sound_system": "Sound System",
            "tables_avail": "Tables",
            "camera": "Camera",
        }

        # --- Filter row ---
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            selected_type = st.selectbox("Space Type", ["All"] + space_types)
        with col2:
            selected_building = st.selectbox("Building", ["All"] + buildings)
        with col3:
            selected_size = st.selectbox("Size", ["All"] + [s.replace("_", " ").title() for s in sizes])
        with col4:
            selected_permissions = st.selectbox("Permissions", ["All"] + [p.replace("_", " ").title() for p in permissions])
        with col5:
            selected_amenities = st.multiselect("Accommodations", options=list(amenity_labels.values()))

        # --- Search and action row ---
        search_col, button_col = st.columns([3, 1])
        with search_col:
            search_query = st.text_input("Search by Name or Space ID", placeholder="e.g. Study Room or 42")
        with button_col:
            st.markdown('<div style="height:27px"></div>', unsafe_allow_html=True)
            confirm_removal = st.button("Confirm Removal", type="primary", use_container_width=True)

        # Handle removal when button is clicked
        if confirm_removal:
            selected_ids = [
                s["space_id"] for s in spaces
                if st.session_state.get(f"select_{s['space_id']}", False)
            ]
            if selected_ids:
                errors = []
                for uid in selected_ids:
                    del_resp = requests.delete(f"{SPACES_URL}/{uid}")
                    if del_resp.status_code != 200:
                        errors.append(uid)
                if errors:
                    st.error(f"Failed to remove space(s) with ID(s): {errors}")
                else:
                    st.success(f"Successfully removed {len(selected_ids)} space(s).")
                st.rerun()
            else:
                st.warning("No spaces selected for removal.")

        # --- Apply filters ---
        filtered_spaces = spaces

        if selected_type != "All":
            filtered_spaces = [s for s in filtered_spaces if s["space_type"] == selected_type]

        if selected_building != "All":
            filtered_spaces = [s for s in filtered_spaces if s.get("building_name") == selected_building]

        if selected_size != "All":
            filtered_spaces = [
                s for s in filtered_spaces
                if s.get("size", "").replace("_", " ").title() == selected_size
            ]

        if selected_permissions != "All":
            filtered_spaces = [
                s for s in filtered_spaces
                if s.get("permissions", "").replace("_", " ").title() == selected_permissions
            ]

        if selected_amenities:
            label_to_key = {v: k for k, v in amenity_labels.items()}
            required_keys = [label_to_key[label] for label in selected_amenities]
            filtered_spaces = [
                s for s in filtered_spaces
                if all(s.get(k) for k in required_keys)
            ]

        if search_query.strip():
            q = search_query.strip().lower()
            filtered_spaces = [
                s for s in filtered_spaces
                if q in s["room_name"].lower()
                or q == str(s["space_id"])
            ]

        # --- Results ---
        st.write(f"Found {len(filtered_spaces)} Spaces")

        _, header_check_col = st.columns([0.85, 0.15])
        with header_check_col:
            st.markdown("**Remove Space**")

        for space in filtered_spaces:
            content_col, check_col = st.columns([0.905, 0.095])
            with content_col:
                with st.expander(f"{space['room_name']} ({space['space_type'].replace('_', ' ').title()})"):
                    info_col, accommodations_col = st.columns(2)

                    with info_col:
                        st.write("**Basic Information**")
                        st.write(f"**Space ID:** {space['space_id']}")
                        st.write(f"**Type:** {space['space_type'].replace('_', ' ').title()}")
                        st.write(f"**Building:** {space.get('building_name', 'N/A')}")
                        st.write(f"**Size:** {space['size'].replace('_', ' ').title() if space.get('size') else 'N/A'}")
                        st.write(f"**Permissions:** {space.get('permissions', 'N/A').replace('_', ' ').title()}")
                        avail_start = space.get('availability_start', 'N/A')
                        avail_end = space.get('availability_end', 'N/A')
                        st.write(f"**Available:** {avail_start} – {avail_end}")
                        st.write("")
                        st.write("**Facility Manager**")
                        manager = managers_by_building.get(space["building_id"])
                        if manager:
                            st.write(f"**Name:** {manager['f_name']} {manager['l_name']}")
                            st.write(f"**Email:** {manager.get('email', 'N/A')}")
                            st.write(f"**Phone:** {manager.get('phone') or 'N/A'}")
                        else:
                            st.write("No facility manager on record.")

                    with accommodations_col:
                        st.write("**Accommodations**")
                        amenities = {
                            "Whiteboard": space.get("whiteboard"),
                            "Screen": space.get("screen"),
                            "Desks": space.get("desks"),
                            "Sound System": space.get("sound_system"),
                            "Tables": space.get("tables_avail"),
                            "Camera": space.get("camera"),
                        }
                        has_any = False
                        for name, val in amenities.items():
                            if val is not None:
                                has_any = True
                                icon = "✓" if val else "✗"
                                st.write(f"{icon} {name}")
                        if not has_any:
                            st.write("No accommodation data available.")

            with check_col:
                st.checkbox(
                    "",
                    key=f"select_{space['space_id']}",
                    label_visibility="collapsed",
                )

    else:
        st.error("Failed to fetch space data from the API")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")
