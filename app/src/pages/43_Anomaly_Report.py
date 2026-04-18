import io
import csv
from collections import Counter
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Anomaly Report")
st.write("Identify irregular booking patterns such as repeated no-shows and high cancellation rates.")

BOOKINGS_URL = "http://web-api:4000/bookings"
USERS_URL = "http://web-api:4000/users"

try:
    bookings_resp = requests.get(BOOKINGS_URL)
    users_resp = requests.get(USERS_URL)

    if bookings_resp.status_code != 200:
        st.error("Failed to fetch booking data.")
        st.stop()

    bookings = bookings_resp.json()
    users = users_resp.json() if users_resp.status_code == 200 else []
    user_lookup = {u["user_id"]: f"{u['f_name']} {u['l_name']}" for u in users}

    noshow_counts = Counter()
    cancel_counts = Counter()
    total_counts = Counter()

    for b in bookings:
        cid = b.get("creator_id")
        if cid:
            total_counts[cid] += 1
            if b["status"] == "no_show":
                noshow_counts[cid] += 1
            elif b["status"] == "cancelled":
                cancel_counts[cid] += 1

    col1, col2 = st.columns(2)
    with col1:
        noshow_threshold = st.slider(
            "Flag users with at least this many no-shows", min_value=1, max_value=10, value=2
        )
    with col2:
        cancel_threshold = st.slider(
            "Flag users with at least this many cancellations", min_value=1, max_value=20, value=5
        )

    flagged = []
    all_creator_ids = set(list(noshow_counts.keys()) + list(cancel_counts.keys()))
    for cid in all_creator_ids:
        ns = noshow_counts.get(cid, 0)
        cc = cancel_counts.get(cid, 0)
        tot = total_counts.get(cid, 0)
        if ns >= noshow_threshold or cc >= cancel_threshold:
            flagged.append({
                "user_id": cid,
                "name": user_lookup.get(cid, f"User {cid}"),
                "total_bookings": tot,
                "no_shows": ns,
                "cancellations": cc,
                "no_show_rate": f"{ns / tot * 100:.1f}%" if tot > 0 else "N/A",
                "cancel_rate": f"{cc / tot * 100:.1f}%" if tot > 0 else "N/A",
            })

    flagged.sort(key=lambda x: x["no_shows"], reverse=True)

    st.divider()
    st.subheader(f"Flagged Users ({len(flagged)})")

    if not flagged:
        st.success("No users meet the current flagging thresholds.")
    else:
        for f in flagged:
            reasons = []
            if f["no_shows"] >= noshow_threshold:
                reasons.append(f"{f['no_shows']} no-show(s)")
            if f["cancellations"] >= cancel_threshold:
                reasons.append(f"{f['cancellations']} cancellation(s)")
            label = f"⚠️ {f['name']} (User #{f['user_id']}) — {', '.join(reasons)}"
            with st.expander(label):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Total Bookings:** {f['total_bookings']}")
                    st.write(f"**No-Shows:** {f['no_shows']} ({f['no_show_rate']})")
                with c2:
                    st.write(f"**Cancellations:** {f['cancellations']} ({f['cancel_rate']})")
                st.caption("Consider escalating to a system admin for review.")

    st.divider()
    st.subheader("Export Full Booking Report")

    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["booking_id", "room_name", "building_name", "status", "time_start", "time_end", "creator_id"],
    )
    writer.writeheader()
    for b in bookings:
        writer.writerow({
            "booking_id": b.get("booking_id"),
            "room_name": b.get("room_name"),
            "building_name": b.get("building_name"),
            "status": b.get("status"),
            "time_start": b.get("time_start"),
            "time_end": b.get("time_end"),
            "creator_id": b.get("creator_id"),
        })

    st.download_button(
        label="Download Booking Report (CSV)",
        data=output.getvalue(),
        file_name="booking_report.csv",
        mime="text/csv",
        type="primary",
    )

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")
