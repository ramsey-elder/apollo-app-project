from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

spaces = Blueprint("spaces", __name__)


# Get all spaces with optional filtering
# Supports query params: size, building_id, space_type, permissions
# Example: /spaces?space_type=room&size=large
@spaces.route("", methods=["GET"])
def get_all_spaces():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /spaces")

        size = request.args.get("size")
        building_id = request.args.get("building_id")
        space_type = request.args.get("space_type")
        permissions = request.args.get("permissions")

        query = """
            SELECT s.*, b.building_name, a.whiteboard, a.screen, a.desks,
                   a.sound_system, a.tables_avail, a.camera
            FROM spaces s
            JOIN buildings b ON s.building_id = b.building_id
            LEFT JOIN accommodations a ON s.space_id = a.space_id
            WHERE 1=1
        """
        params = []

        if size:
            query += " AND s.size = %s"
            params.append(size)
        if building_id:
            query += " AND s.building_id = %s"
            params.append(building_id)
        if space_type:
            query += " AND s.space_type = %s"
            params.append(space_type)
        if permissions:
            query += " AND s.permissions = %s"
            params.append(permissions)

        cursor.execute(query, params)
        space_list = cursor.fetchall()

        current_app.logger.info(f"Retrieved {len(space_list)} spaces")
        return jsonify(space_list), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_all_spaces: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Get a single space by ID, including its accommodations
# Example: GET /spaces/1
@spaces.route("/<int:space_id>", methods=["GET"])
def get_space(space_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /spaces/{space_id}")

        cursor.execute("""
            SELECT s.*, b.building_name
            FROM spaces s
            JOIN buildings b ON s.building_id = b.building_id
            WHERE s.space_id = %s
        """, (space_id,))
        space = cursor.fetchone()

        if not space:
            return jsonify({"error": "Space not found"}), 404

        cursor.execute("SELECT * FROM accommodations WHERE space_id = %s", (space_id,))
        space["accommodations"] = cursor.fetchone()

        return jsonify(space), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_space: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Create a new bookable space
# Required fields: permissions, availability_start, availability_end, space_type,
#                  room_name, creator_id, building_id
# Optional fields: size
# Example: POST /spaces with JSON body
@spaces.route("", methods=["POST"])
def create_space():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("POST /spaces")
        data = request.get_json()

        required_fields = [
            "permissions", "availability_start", "availability_end",
            "space_type", "room_name", "creator_id", "building_id",
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor.execute("SELECT building_id FROM buildings WHERE building_id = %s", (data["building_id"],))
        if not cursor.fetchone():
            return jsonify({"error": "Building not found"}), 404

        cursor.execute("""
            INSERT INTO spaces (permissions, availability_start, availability_end,
                                space_type, room_name, size, creator_id, building_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data["permissions"],
            data["availability_start"],
            data["availability_end"],
            data["space_type"],
            data["room_name"],
            data.get("size"),
            data["creator_id"],
            data["building_id"],
        ))
        get_db().commit()

        return jsonify({"message": "Space created successfully", "space_id": cursor.lastrowid}), 201
    except Error as e:
        current_app.logger.error(f"Database error in create_space: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Update space details
# Can update: permissions, availability_start, availability_end, space_type, room_name, size
# Example: PUT /spaces/1 with JSON body
@spaces.route("/<int:space_id>", methods=["PUT"])
def update_space(space_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"PUT /spaces/{space_id}")
        data = request.get_json()

        cursor.execute("SELECT space_id FROM spaces WHERE space_id = %s", (space_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Space not found"}), 404

        allowed_fields = [
            "permissions", "availability_start", "availability_end",
            "space_type", "room_name", "size",
        ]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(space_id)
        query = f"UPDATE spaces SET {', '.join(update_fields)} WHERE space_id = %s"
        cursor.execute(query, params)
        get_db().commit()

        return jsonify({"message": "Space updated successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in update_space: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Remove a space by ID
# Example: DELETE /spaces/1
@spaces.route("/<int:space_id>", methods=["DELETE"])
def delete_space(space_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"DELETE /spaces/{space_id}")

        cursor.execute("SELECT space_id FROM spaces WHERE space_id = %s", (space_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Space not found"}), 404

        cursor.execute("DELETE FROM accommodations WHERE space_id = %s", (space_id,))
        cursor.execute("DELETE FROM spaces WHERE space_id = %s", (space_id,))
        get_db().commit()

        return jsonify({"message": "Space deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in delete_space: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
