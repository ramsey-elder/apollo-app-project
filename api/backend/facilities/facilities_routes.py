from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

facilities = Blueprint("facilities", __name__)


# List all buildings with booking counts for underuse analysis [Michael-3]
# Example: GET /facilities/buildings
@facilities.route("/buildings", methods=["GET"])
def get_all_buildings():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /facilities/buildings")

        cursor.execute("""
            SELECT b.building_id, b.building_name, b.street, b.city, b.state, b.zip,
                   COUNT(DISTINCT s.space_id)    AS space_count,
                   COUNT(bk.booking_id)          AS booking_count,
                   ROUND(
                       COUNT(bk.booking_id) /
                       NULLIF(COUNT(DISTINCT s.space_id), 0),
                   2)                            AS bookings_per_space
            FROM buildings b
            LEFT JOIN spaces s   ON b.building_id = s.building_id
            LEFT JOIN bookings bk ON s.space_id  = bk.space_id
            GROUP BY b.building_id, b.building_name, b.street, b.city, b.state, b.zip
            ORDER BY bookings_per_space ASC
        """)
        building_list = cursor.fetchall()

        current_app.logger.info(f"Retrieved {len(building_list)} buildings")
        return jsonify(building_list), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_all_buildings: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get a single building by ID
# Example: GET /facilities/buildings/1
@facilities.route("/buildings/<int:building_id>", methods=["GET"])
def get_building(building_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /facilities/buildings/{building_id}")

        cursor.execute("""
            SELECT b.*,
                   COUNT(DISTINCT s.space_id) AS space_count,
                   COUNT(bk.booking_id)       AS booking_count
            FROM buildings b
            LEFT JOIN spaces s   ON b.building_id = s.building_id
            LEFT JOIN bookings bk ON s.space_id  = bk.space_id
            WHERE b.building_id = %s
            GROUP BY b.building_id
        """, (building_id,))
        building = cursor.fetchone()

        if not building:
            return jsonify({"error": "Building not found"}), 404

        return jsonify(building), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_building: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# List all facility managers, optionally filtered by building [Adam-5]
# Supports query param: building_id
# Example: GET /facilities/facility_managers?building_id=2
@facilities.route("/facility_managers", methods=["GET"])
def get_all_facility_managers():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /facilities/facility_managers")

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
        current_app.logger.error(f"Database error in get_all_facility_managers: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get a single facility manager by ID [Adam-5]
# Returns f_name, l_name, email, and phone in one response
# Example: GET /facilities/facility_managers/1
@facilities.route("/facility_managers/<int:manager_id>", methods=["GET"])
def get_facility_manager(manager_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /facilities/facility_managers/{manager_id}")

        cursor.execute("""
            SELECT fm.manager_id, fm.f_name, fm.l_name, fm.email, fm.phone,
                   fm.building_id, b.building_name
            FROM facility_managers fm
            JOIN buildings b ON fm.building_id = b.building_id
            WHERE fm.manager_id = %s
        """, (manager_id,))
        manager = cursor.fetchone()

        if not manager:
            return jsonify({"error": "Facility manager not found"}), 404

        return jsonify(manager), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_facility_manager: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get the facility manager for a specific building [Adam-5]
# Useful for admins looking up who to contact about a space issue
# Example: GET /facilities/buildings/1/facility_manager
@facilities.route("/buildings/<int:building_id>/facility_manager", methods=["GET"])
def get_building_facility_manager(building_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /facilities/buildings/{building_id}/facility_manager")

        cursor.execute("SELECT building_id FROM buildings WHERE building_id = %s", (building_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Building not found"}), 404

        cursor.execute("""
            SELECT fm.manager_id, fm.f_name, fm.l_name, fm.email, fm.phone,
                   fm.building_id, b.building_name
            FROM facility_managers fm
            JOIN buildings b ON fm.building_id = b.building_id
            WHERE fm.building_id = %s
        """, (building_id,))
        manager = cursor.fetchone()

        if not manager:
            return jsonify({"error": "No facility manager found for this building"}), 404

        return jsonify(manager), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_building_facility_manager: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
