from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

bookings = Blueprint("bookings", __name__)


# Get all bookings with optional filtering
# Supports query params: status, building, space_type, user_type, creator_id, club_id
# Example: /bookings?status=active&creator_id=1
@bookings.route("", methods=["GET"])
def get_all_bookings():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /bookings")

        status = request.args.get("status")
        building = request.args.get("building")
        space_type = request.args.get("space_type")
        creator_id = request.args.get("creator_id")
        club_id = request.args.get("club_id")

        query = """
            SELECT b.*, s.space_type, s.room_name, bg.building_name
            FROM bookings b
            JOIN spaces s ON b.space_id = s.space_id
            JOIN buildings bg ON s.building_id = bg.building_id
            WHERE 1=1
        """
        params = []

        if status:
            query += " AND b.status = %s"
            params.append(status)
        if building:
            query += " AND bg.building_name LIKE %s"
            params.append(f"%{building}%")
        if space_type:
            query += " AND s.space_type = %s"
            params.append(space_type)
        if creator_id:
            query += " AND b.creator_id = %s"
            params.append(creator_id)
        if club_id:
            query += " AND b.club_id = %s"
            params.append(club_id)

        cursor.execute(query, params)
        booking_list = cursor.fetchall()

        current_app.logger.info(f"Retrieved {len(booking_list)} bookings")
        return jsonify(booking_list), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_all_bookings: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get a single booking by ID
# Example: GET /bookings/1
@bookings.route("/<int:booking_id>", methods=["GET"])
def get_booking(booking_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /bookings/{booking_id}")

        cursor.execute("""
            SELECT b.*, s.space_type, s.room_name, bg.building_name
            FROM bookings b
            JOIN spaces s ON b.space_id = s.space_id
            JOIN buildings bg ON s.building_id = bg.building_id
            WHERE b.booking_id = %s
        """, (booking_id,))
        booking = cursor.fetchone()

        if not booking:
            return jsonify({"error": "Booking not found"}), 404

        # Fetch participants for this booking
        cursor.execute("""
            SELECT u.user_id, u.f_name, u.l_name, u.email, bp.managing
            FROM booking_participants bp
            JOIN users u ON bp.user_id = u.user_id
            WHERE bp.booking_id = %s
        """, (booking_id,))
        booking["participants"] = cursor.fetchall()

        return jsonify(booking), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_booking: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Create a new booking
# Required fields: time_start, time_end, space_id, creator_id
# Optional fields: club_id
# Example: POST /bookings with JSON body
@bookings.route("", methods=["POST"])
def create_booking():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("POST /bookings")
        data = request.get_json()

        required_fields = ["time_start", "time_end", "space_id", "creator_id"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor.execute("SELECT space_id FROM spaces WHERE space_id = %s", (data["space_id"],))
        if not cursor.fetchone():
            return jsonify({"error": "Space not found"}), 404

        cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (data["creator_id"],))
        if not cursor.fetchone():
            return jsonify({"error": "Creator user not found"}), 404

        cursor.execute("""
            INSERT INTO bookings (time_start, time_end, space_id, creator_id, club_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data["time_start"],
            data["time_end"],
            data["space_id"],
            data["creator_id"],
            data.get("club_id"),
        ))
        get_db().commit()

        return jsonify({"message": "Booking created successfully", "booking_id": cursor.lastrowid}), 201
    except Error as e:
        current_app.logger.error(f"Database error in create_booking: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Update a booking (change time, status, approve, cancel)
# Can update: time_start, time_end, status, approved
# Example: PUT /bookings/1 with JSON body
@bookings.route("/<int:booking_id>", methods=["PUT"])
def update_booking(booking_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"PUT /bookings/{booking_id}")
        data = request.get_json()

        cursor.execute("SELECT booking_id FROM bookings WHERE booking_id = %s", (booking_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Booking not found"}), 404

        allowed_fields = ["time_start", "time_end", "status", "approved"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(booking_id)
        query = f"UPDATE bookings SET {', '.join(update_fields)} WHERE booking_id = %s"
        cursor.execute(query, params)
        get_db().commit()

        return jsonify({"message": "Booking updated successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in update_booking: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Hard delete a booking by ID
# Example: DELETE /bookings/1
@bookings.route("/<int:booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"DELETE /bookings/{booking_id}")

        cursor.execute("SELECT booking_id FROM bookings WHERE booking_id = %s", (booking_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Booking not found"}), 404

        cursor.execute("DELETE FROM booking_participants WHERE booking_id = %s", (booking_id,))
        cursor.execute("DELETE FROM bookings WHERE booking_id = %s", (booking_id,))
        get_db().commit()

        return jsonify({"message": "Booking deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in delete_booking: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
