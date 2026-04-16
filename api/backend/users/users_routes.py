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