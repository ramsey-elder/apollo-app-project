from flask import Blueprint, jsonify, current_app
from backend.db_connection import get_db
from mysql.connector import Error

clubs = Blueprint("clubs", __name__)

# Get all clubs
# Example: GET /clubs
@clubs.route("", methods=["GET"])
def get_all_clubs():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /clubs")

        cursor.execute("SELECT club_id, club_name, description, email, suspended FROM clubs")
        club_list = cursor.fetchall()

        current_app.logger.info(f"Retrieved {len(club_list)} clubs")
        return jsonify(club_list), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_all_clubs: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
