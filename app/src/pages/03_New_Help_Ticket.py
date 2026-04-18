import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Submit Help Ticket")

# Reset form whenever navigating to this page from another page
if st.session_state.get("_last_page") != "03_help_ticket":
    st.session_state["_last_page"] = "03_help_ticket"
    st.session_state["ht_form_key_counter"] = st.session_state.get("ht_form_key_counter", -1) + 1

if "ht_show_success_modal" not in st.session_state:
    st.session_state.ht_show_success_modal = False
if "ht_success_ticket_id" not in st.session_state:
    st.session_state.ht_success_ticket_id = None
if "ht_reset_form" not in st.session_state:
    st.session_state.ht_reset_form = False

TICKET_TYPES = ["booking_issue", "access", "space", "account", "report", "other"]

HELP_TICKETS_API_URL = "http://web-api:4000/help_tickets"


@st.dialog("Success")
def show_success_dialog(ticket_id):
    st.markdown(f"### Help ticket #{ticket_id} has been successfully submitted!")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Return to Home", type="primary", use_container_width=True):
            st.session_state.ht_show_success_modal = False
            st.session_state.ht_success_ticket_id = None
            st.switch_page("pages/00_Student_Home.py")

    with col2:
        if st.button("Submit Another Ticket", type="primary", use_container_width=True):
            st.session_state.ht_show_success_modal = False
            st.session_state.ht_success_ticket_id = None
            st.session_state.ht_reset_form = True
            st.rerun()


if st.session_state.ht_reset_form:
    st.session_state.ht_form_key_counter += 1
    st.session_state.ht_reset_form = False

with st.form(f"help_ticket_form_{st.session_state.ht_form_key_counter}"):
    st.subheader("Ticket Details")

    title = st.text_input("Title *")

    ticket_type = st.selectbox(
        "Ticket Type *",
        options=TICKET_TYPES,
        format_func=lambda x: x.replace("_", " ").title(),
    )

    description = st.text_area("Description *", height=150)

    submitted = st.form_submit_button("Submit Ticket", type="primary")

    if submitted:
        if not title.strip():
            st.error("Please enter a title.")
        elif not description.strip():
            st.error("Please enter a description.")
        else:
            ticket_data = {
                "title": title.strip(),
                "ticket_type": ticket_type,
                "description": description.strip(),
                "creator_id": st.session_state.get("user_id", 1),
            }

            try:
                response = requests.post(HELP_TICKETS_API_URL, json=ticket_data)

                if response.status_code == 201:
                    st.session_state.ht_show_success_modal = True
                    st.session_state.ht_success_ticket_id = response.json().get("ticket_id")
                    st.rerun()
                else:
                    st.error(
                        f"Failed to submit ticket: {response.json().get('error', 'Unknown error')}"
                    )

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {str(e)}")
                st.info("Please ensure the API server is running.")

if st.session_state.ht_show_success_modal:
    st.session_state.ht_show_success_modal = False
    show_success_dialog(st.session_state.ht_success_ticket_id)
