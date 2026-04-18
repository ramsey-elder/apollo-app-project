import datetime
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Create New Booking")

# Reset form whenever navigating to this page from another page
if st.session_state.get("_last_page") != "17_club_booking":
    st.session_state["_last_page"] = "17_club_booking"
    st.session_state["cb_form_key"] = st.session_state.get("cb_form_key", -1) + 1

if "cb_show_success_modal" not in st.session_state:
    st.session_state.cb_show_success_modal = False
if "cb_success_booking_count" not in st.session_state:
    st.session_state.cb_success_booking_count = 0

k = st.session_state["cb_form_key"]

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def add_months(dt, months):
    """Advance a datetime by a number of months, clamping to the last day of the month."""
    month = dt.month - 1 + months
    year = dt.year + month // 12
    month = month % 12 + 1
    is_leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    days_in_month = [31, 29 if is_leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]
    day = min(dt.day, days_in_month)
    return dt.replace(year=year, month=month, day=day)


def generate_occurrences(time_start, time_end, frequency, recur_until,
                         custom_every_n=1, custom_every_unit="days", custom_weekdays=None):
    """Return a list of (time_start, time_end) pairs for all occurrences up to recur_until."""
    occurrences = []
    duration = time_end - time_start

    if frequency == "Custom" and custom_weekdays:
        current = time_start
        while current.date() <= recur_until:
            if current.strftime("%A") in custom_weekdays:
                occurrences.append((current, current + duration))
            current += datetime.timedelta(days=1)

    elif frequency == "Custom":
        current_start = time_start
        current_end = time_end
        while current_start.date() <= recur_until:
            occurrences.append((current_start, current_end))
            if custom_every_unit == "days":
                current_start += datetime.timedelta(days=custom_every_n)
                current_end += datetime.timedelta(days=custom_every_n)
            elif custom_every_unit == "weeks":
                current_start += datetime.timedelta(weeks=custom_every_n)
                current_end += datetime.timedelta(weeks=custom_every_n)
            elif custom_every_unit == "months":
                current_start = add_months(current_start, custom_every_n)
                current_end = add_months(current_end, custom_every_n)

    else:
        current_start = time_start
        current_end = time_end
        while current_start.date() <= recur_until:
            occurrences.append((current_start, current_end))
            if frequency == "Daily":
                current_start += datetime.timedelta(days=1)
                current_end += datetime.timedelta(days=1)
            elif frequency == "Weekly":
                current_start += datetime.timedelta(weeks=1)
                current_end += datetime.timedelta(weeks=1)
            elif frequency == "Monthly":
                current_start = add_months(current_start, 1)
                current_end = add_months(current_end, 1)

    return occurrences


@st.dialog("Success")
def show_success_dialog(count):
    if count == 1:
        st.markdown("### Your booking has been successfully created!")
    else:
        st.markdown(f"### {count} recurring bookings have been successfully created!")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Return to Home", type="primary", use_container_width=True):
            st.session_state.cb_show_success_modal = False
            st.session_state.cb_success_booking_count = 0
            st.switch_page("pages/10_Club_Rep_Home.py")
    with col2:
        if st.button("Create Another Booking", type="primary", use_container_width=True):
            st.session_state.cb_show_success_modal = False
            st.session_state.cb_success_booking_count = 0
            st.session_state["cb_form_key"] += 1
            st.rerun()


# Fetch spaces from API
try:
    spaces_response = requests.get("http://web-api:4000/spaces")
    if spaces_response.status_code == 200:
        spaces_data = spaces_response.json()
        space_options = {
            s["space_id"]: f"{s['room_name']} ({s['space_type'].replace('_', ' ').title()})"
            for s in spaces_data
        }
    else:
        space_options = {}
        st.warning("Could not load spaces from the server.")
except requests.exceptions.RequestException:
    space_options = {}
    st.warning("Could not connect to the API to load spaces.")

# Fetch clubs from API
try:
    clubs_response = requests.get("http://web-api:4000/clubs")
    if clubs_response.status_code == 200:
        clubs_data = clubs_response.json()
        club_options = {c["club_id"]: c["club_name"] for c in clubs_data}
    else:
        club_options = {}
        st.warning("Could not load clubs from the server.")
except requests.exceptions.RequestException:
    club_options = {}
    st.warning("Could not connect to the API to load clubs.")

BOOKINGS_API_URL = "http://web-api:4000/bookings"

# ── Booking Details ────────────────────────────────────────────────────────────
st.subheader("Booking Details")

if space_options:
    selected_space_name = st.selectbox(
        "Space *", options=list(space_options.values()), key=f"cb_space_{k}"
    )
else:
    selected_space_name = st.selectbox("Space *", options=[], key=f"cb_space_{k}")
    st.caption("No spaces available.")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date *", value=datetime.date.today(), key=f"cb_start_date_{k}")
    start_time = st.time_input("Start Time *", value=datetime.time(9, 0), key=f"cb_start_time_{k}")
with col2:
    end_date = st.date_input("End Date *", value=datetime.date.today(), key=f"cb_end_date_{k}")
    end_time = st.time_input("End Time *", value=datetime.time(10, 0), key=f"cb_end_time_{k}")

if club_options:
    selected_club_name = st.selectbox(
        "Club *", options=list(club_options.values()), key=f"cb_club_{k}"
    )
else:
    selected_club_name = st.selectbox("Club *", options=[], key=f"cb_club_{k}")
    st.caption("No clubs available.")

# ── Recurring Booking ──────────────────────────────────────────────────────────
st.divider()
st.subheader("Recurring Booking")

is_recurring = st.checkbox("Make this a recurring booking", key=f"cb_recurring_{k}")

custom_every_n = 1
custom_every_unit = "days"
custom_weekdays = []
recur_until = datetime.date.today()

if is_recurring:
    recurrence_frequency = st.selectbox(
        "Repeat",
        options=["Daily", "Weekly", "Monthly", "Custom"],
        key=f"cb_frequency_{k}",
    )

    if recurrence_frequency == "Custom":
        st.caption("Choose one: repeat by interval OR repeat on specific days of the week.")
        interval_col, unit_col = st.columns([1, 2])
        with interval_col:
            custom_every_n = st.number_input(
                "Repeat every",
                min_value=1,
                max_value=365,
                value=1,
                step=1,
                key=f"cb_every_n_{k}",
            )
        with unit_col:
            custom_every_unit = st.selectbox(
                "Unit",
                options=["days", "weeks", "months"],
                label_visibility="hidden",
                key=f"cb_every_unit_{k}",
            )
        custom_weekdays = st.multiselect(
            "Repeat on (days of the week)",
            options=WEEKDAYS,
            key=f"cb_weekdays_{k}",
        )
        st.caption("If days of the week are selected, the interval above is ignored.")

    recur_until = st.date_input(
        "Recurrence End Date",
        value=datetime.date.today() + datetime.timedelta(weeks=4),
        key=f"cb_recur_until_{k}",
    )
else:
    recurrence_frequency = "Daily"

# ── Submit ─────────────────────────────────────────────────────────────────────
st.divider()
submitted = st.button("Create Booking", type="primary")

if submitted:
    if not space_options:
        st.error("No spaces are available. Please try again later.")
    elif not club_options:
        st.error("No clubs are available. Please try again later.")
    else:
        time_start = datetime.datetime.combine(start_date, start_time)
        time_end = datetime.datetime.combine(end_date, end_time)

        if time_end <= time_start:
            st.error("End time must be after start time.")
        elif is_recurring and recur_until <= start_date:
            st.error("Recurrence end date must be after the start date.")
        else:
            space_id = next(k for k, v in space_options.items() if v == selected_space_name)
            club_id = next(k for k, v in club_options.items() if v == selected_club_name)
            creator_id = st.session_state.get("user_id", 1)

            if is_recurring:
                occurrences = generate_occurrences(
                    time_start, time_end,
                    recurrence_frequency, recur_until,
                    custom_every_n=custom_every_n,
                    custom_every_unit=custom_every_unit,
                    custom_weekdays=custom_weekdays,
                )
            else:
                occurrences = [(time_start, time_end)]

            created = 0
            failed = 0

            for occ_start, occ_end in occurrences:
                booking_data = {
                    "time_start": occ_start.strftime("%Y-%m-%d %H:%M:%S"),
                    "time_end": occ_end.strftime("%Y-%m-%d %H:%M:%S"),
                    "space_id": space_id,
                    "club_id": club_id,
                    "creator_id": creator_id,
                }
                try:
                    response = requests.post(BOOKINGS_API_URL, json=booking_data)
                    if response.status_code == 201:
                        created += 1
                    else:
                        failed += 1
                except requests.exceptions.RequestException:
                    failed += 1

            if created > 0:
                st.session_state.cb_show_success_modal = True
                st.session_state.cb_success_booking_count = created
                if failed > 0:
                    st.warning(f"{failed} occurrence(s) could not be created.")
                st.rerun()
            else:
                st.error("Failed to create any bookings. Please try again.")

if st.session_state.cb_show_success_modal:
    st.session_state.cb_show_success_modal = False
    show_success_dialog(st.session_state.cb_success_booking_count)
