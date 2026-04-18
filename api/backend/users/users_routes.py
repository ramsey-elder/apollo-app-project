from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

users = Blueprint("users", __name__)

VALID_USER_TYPES = {"student", "club_rep", "admin", "data_analyst"}


# List all registered users [Adam-6]
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


# Create a new user
# Required fields: f_name, l_name, email, user_type
# Example: POST /users with JSON body
@users.route("", methods=["POST"])
def create_user():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("POST /users")
        data = request.get_json()

        required_fields = ["f_name", "l_name", "email", "user_type"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        if data["user_type"] not in VALID_USER_TYPES:
            return jsonify({"error": f"Invalid user_type. Must be one of: {', '.join(sorted(VALID_USER_TYPES))}"}), 400

        cursor.execute("""
            INSERT INTO users (f_name, l_name, email, user_type)
            VALUES (%s, %s, %s, %s)
        """, (data["f_name"], data["l_name"], data["email"], data["user_type"]))
        get_db().commit()

        new_id = cursor.lastrowid
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (new_id,))
        return jsonify(cursor.fetchone()), 201
    except Error as e:
        if e.errno == 1062:
            return jsonify({"error": "A user with that email already exists"}), 409
        current_app.logger.error(f"Database error in create_user: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Partial update of a user — only fields present in the body are changed
# Updatable fields: f_name, l_name, email, user_type
# Example: PUT /users/1 with JSON body
@users.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"PUT /users/{user_id}")
        data = request.get_json()

        cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            return jsonify({"error": "User not found"}), 404

        if "user_type" in data and data["user_type"] not in VALID_USER_TYPES:
            return jsonify({"error": f"Invalid user_type. Must be one of: {', '.join(sorted(VALID_USER_TYPES))}"}), 400

        allowed_fields = ["f_name", "l_name", "email", "user_type"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(user_id)
        cursor.execute(
            f"UPDATE users SET {', '.join(update_fields)} WHERE user_id = %s",
            params,
        )
        get_db().commit()

        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        return jsonify(cursor.fetchone()), 200
    except Error as e:
        if e.errno == 1062:
            return jsonify({"error": "A user with that email already exists"}), 409
        current_app.logger.error(f"Database error in update_user: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Delete a user [Adam-6]
# Returns 409 if the user owns bookings, buildings, or help tickets (NOT NULL FKs).
# Cleans up booking_participants, club_reps, and nullable help_tickets.admin_id first.
# Wrapped in a transaction — rolls back on any failure.
# Example: DELETE /users/1
@users.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        current_app.logger.info(f"DELETE /users/{user_id}")

        cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            return jsonify({"error": "User not found"}), 404

        # Check NOT NULL FK references that would block deletion
        blocking = []

        cursor.execute("SELECT COUNT(*) AS cnt FROM bookings WHERE creator_id = %s", (user_id,))
        if cursor.fetchone()["cnt"] > 0:
            blocking.append("bookings (creator_id)")

        cursor.execute("SELECT COUNT(*) AS cnt FROM buildings WHERE creator_id = %s", (user_id,))
        if cursor.fetchone()["cnt"] > 0:
            blocking.append("buildings (creator_id)")

        cursor.execute("SELECT COUNT(*) AS cnt FROM help_tickets WHERE creator_id = %s", (user_id,))
        if cursor.fetchone()["cnt"] > 0:
            blocking.append("help_tickets (creator_id)")

        if blocking:
            return jsonify({
                "error": "Cannot delete user: they own records in " + ", ".join(blocking)
            }), 409

        # Clean up nullable/junction FKs, then delete the user
        cursor.execute("DELETE FROM booking_participants WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM club_reps WHERE user_id = %s", (user_id,))
        cursor.execute("UPDATE help_tickets SET admin_id = NULL WHERE admin_id = %s", (user_id,))
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        db.commit()

        return jsonify({"message": "User deleted successfully"}), 200
    except Error as e:
        db.rollback()
        current_app.logger.error(f"Database error in delete_user: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
