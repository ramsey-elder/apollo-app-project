from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

users = Blueprint("users", __name__)


# Get all registered users
# Example: GET /users
@users.route("", methods=["GET"])
def get_all_users():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /users")

        cursor.execute("SELECT * FROM users")
        user_list = cursor.fetchall()

        current_app.logger.info(f"Retrieved {len(user_list)} users")
        return jsonify(user_list), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_all_users: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get a single user by ID
# Example: GET /users/1
@users.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /users/{user_id}")

        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(user), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_user: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Delete a user by ID
# Example: DELETE /users/1
@users.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"DELETE /users/{user_id}")

        cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            return jsonify({"error": "User not found"}), 404

        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        get_db().commit()

        return jsonify({"message": "User deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in delete_user: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get all clubs a user represents
# Example: GET /users/club_reps/1
@users.route("/club_reps/<int:user_id>", methods=["GET"])
def get_user_clubs(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /users/club_reps/{user_id}")

        cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            return jsonify({"error": "User not found"}), 404

        cursor.execute("""
            SELECT c.club_id, c.club_name, c.description, c.email, c.suspended
            FROM club_reps cr
            JOIN clubs c ON cr.club_id = c.club_id
            WHERE cr.user_id = %s
        """, (user_id,))
        clubs = cursor.fetchall()

        return jsonify(clubs), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_user_clubs: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get facility manager contact info (facility_managers is a separate table from users)
# Supports query param: building_id
# Example: GET /users/facility_managers?building_id=2
@users.route("/facility_managers", methods=["GET"])
def get_facility_managers():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /users/facility_managers")

        building_id = request.args.get("building_id")

        query = """
            SELECT fm.manager_id, fm.f_name, fm.l_name, fm.email, fm.phone,
                   fm.building_id, b.building_name
            FROM facility_managers fm
            JOIN buildings b ON fm.building_id = b.building_id
            WHERE 1=1
        """
        params = []

        if building_id:
            query += " AND fm.building_id = %s"
            params.append(building_id)

        cursor.execute(query, params)
        managers = cursor.fetchall()

        current_app.logger.info(f"Retrieved {len(managers)} facility managers")
        return jsonify(managers), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_facility_managers: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# List buildings with booking counts for underuse analysis
# Example: GET /users/buildings
@users.route("/buildings", methods=["GET"])
def get_buildings():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /users/buildings")

        cursor.execute("""
            SELECT b.building_id, b.building_name, b.street, b.city, b.state, b.zip,
                   COUNT(bk.booking_id) AS booking_count
            FROM buildings b
            LEFT JOIN spaces s ON b.building_id = s.building_id
            LEFT JOIN bookings bk ON s.space_id = bk.space_id
            GROUP BY b.building_id, b.building_name, b.street, b.city, b.state, b.zip
            ORDER BY booking_count ASC
        """)
        building_list = cursor.fetchall()

        current_app.logger.info(f"Retrieved {len(building_list)} buildings")
        return jsonify(building_list), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_buildings: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
