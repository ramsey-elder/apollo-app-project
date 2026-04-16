import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Initialize sidebar
SideBarLinks()

st.title("User Directory")

# API endpoint
API_URL = "http://web-api:4000/users"

try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        users = response.json()

        # Extract unique values for user type filter
        user_types = sorted(list(set(user["user_type"] for user in users)))

        # Controls row
        filter_col, search_col, button_col = st.columns([1, 2, 1])

        with filter_col:
            selected_type = st.selectbox("Filter by User Type", ["All"] + user_types)

        with search_col:
            search_query = st.text_input("Search by Name or User ID", placeholder="e.g. Joshua or 42")

        with button_col:
            st.markdown('<div style="height:27px"></div>', unsafe_allow_html=True)
            confirm_removal = st.button("Confirm Removal", type="primary", use_container_width=True)

        # Handle removal when button is clicked
        if confirm_removal:
            selected_ids = [
                u["user_id"] for u in users
                if st.session_state.get(f"select_{u['user_id']}", False)
            ]
            if selected_ids:
                errors = []
                for uid in selected_ids:
                    del_resp = requests.delete(f"{API_URL}/{uid}")
                    if del_resp.status_code != 200:
                        errors.append(uid)
                if errors:
                    st.error(f"Failed to remove user(s) with ID(s): {errors}")
                else:
                    st.success(f"Successfully removed {len(selected_ids)} user(s).")
                st.rerun()
            else:
                st.warning("No users selected for removal.")

        # Apply filters
        filtered_users = users
        if selected_type != "All":
            filtered_users = [u for u in filtered_users if u["user_type"] == selected_type]
        if search_query.strip():
            q = search_query.strip().lower()
            filtered_users = [
                u for u in filtered_users
                if q in u["f_name"].lower()
                or q in u["l_name"].lower()
                or q in f"{u['f_name']} {u['l_name']}".lower()
                or q == str(u["user_id"])
            ]

        # Display results count
        st.write(f"Found {len(filtered_users)} Users")

        # Header row for the checkbox column
        _, header_check_col = st.columns([0.88, 0.12])
        with header_check_col:
            st.markdown("**Remove User**")

        # Render each user with a checkbox and expandable details
        for user in filtered_users:
            content_col, check_col = st.columns([0.93, 0.07])
            with content_col:
                with st.expander(f"{user['f_name']} {user['l_name']} ({user['user_type'].replace('_', ' ').title()})"):
                    info_col, contact_col = st.columns(2)

                    with info_col:
                        st.write("**Basic Information**")
                        st.write(f"**User ID:** {user['user_id']}")
                        st.write(f"**Role:** {user['user_type'].replace('_', ' ').title()}")

                    with contact_col:
                        st.write("**Contact Information**")
                        st.write(f"**Email:** {user['email']}")

            with check_col:
                st.checkbox(
                    "",
                    key=f"select_{user['user_id']}",
                    label_visibility="collapsed",
                )

    else:
        st.error("Failed to fetch user data from the API")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")
