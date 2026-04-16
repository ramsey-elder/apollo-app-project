from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

buildings = Blueprint("buildings", __name__)

# Get all buildings in db
# Example: GET /buildings
@buildings.route("", methods=["GET"])
def get_all_buildings():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /buildings")

        cursor.execute("SELECT * FROM buildings")
        building_list = cursor.fetchall()

        current_app.logger.info(f"Retrieved {len(building_list)} buildings")
        return jsonify(building_list), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_all_buildings: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# List buildings with booking counts for underuse analysis
# Example: GET /buildings
@buildings.route("/buildings", methods=["GET"])
def get_buildings():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /buildings")

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