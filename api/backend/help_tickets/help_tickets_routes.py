from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

help_tickets = Blueprint("help_tickets", __name__)

# Get all help tickets
# Example: GET /help_tickets
@help_tickets.route("", methods=["GET"])
def get_all_help_tickets():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /help_tickets")

        cursor.execute("SELECT ticket_id, ticket_type, title, description, created_at, closed_at, admin_id, creator_id FROM help_tickets")
        ticket_list = cursor.fetchall()

        current_app.logger.info(f"Retrieved {len(ticket_list)} help tickets")
        return jsonify(ticket_list), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_all_help_tickets: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()



# Create a new help ticket
# Required fields: ticket_type, title, description, creator_id (auto-populated from session on frontend)
# created_at is auto-populated; closed_at defaults to NULL
# Example: POST /help_tickets with JSON body
@help_tickets.route("", methods=["POST"])
def create_help_ticket():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("POST /help_tickets")
        data = request.get_json()

        required_fields = ["ticket_type", "title", "description", "creator_id"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor.execute("""
            INSERT INTO help_tickets (ticket_type, title, description, creator_id, created_at)
            VALUES (%s, %s, %s, %s, NOW())
        """, (
            data["ticket_type"],
            data["title"],
            data["description"],
            data["creator_id"],
        ))
        get_db().commit()

        return jsonify({"message": "Help ticket created successfully", "ticket_id": cursor.lastrowid}), 201
    except Error as e:
        current_app.logger.error(f"Database error in create_help_ticket: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
