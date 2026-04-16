from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error
from datetime import timedelta

facility_managers = Blueprint("facility_managers", __name__)

# Get facility manager contact info (facility_managers is a separate table from users)
# Supports query param: building_id
# Example: GET /facility_managers?building_id=2
@facility_managers.route("", methods=["GET"])
def get_facility_managers():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /facility_managers")

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
