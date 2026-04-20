import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Initialize sidebar
SideBarLinks()

st.title("Space Directory")

# API endpoints
SPACES_URL = "http://web-api:4000/spaces"

try:
    response = requests.get(SPACES_URL)
    if response.status_code == 200:
        spaces = response.json()

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
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            selected_type = st.selectbox("Space Type", ["All"] + space_types)
        with col2:
            selected_building = st.selectbox("Building", ["All"] + buildings)
        with col3:
            selected_size = st.selectbox("Size", ["All"] + [s.replace("_", " ").title() for s in sizes])
        with col4:
            selected_permissions = st.selectbox("Permissions", ["All"] + [p.replace("_", " ").title() for p in permissions])

        # --- Search and action row ---
        search_col, col5 = st.columns([3, 1])
        with search_col:
            search_query = st.text_input("Search by Name or Space ID", placeholder="e.g. Study Room or 42")
        with col5:
            selected_amenities = st.multiselect("Accommodations", options=list(amenity_labels.values()))

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

        for space in filtered_spaces:
            content_col, __ = st.columns([0.905, 0.095])
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

    else:
        st.error("Failed to fetch space data from the API")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")
