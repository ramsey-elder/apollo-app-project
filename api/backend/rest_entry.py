from flask import Flask
from dotenv import load_dotenv
import os
import logging

from backend.db_connection import init_app as init_db
from backend.simple.simple_routes import simple_routes
from backend.users.users_routes import users
from backend.bookings.bookings_routes import bookings
from backend.spaces.spaces_routes import spaces
from backend.buildings.buildings_routes import buildings
from backend.facility_managers.facility_managers_routes import facility_managers
from backend.clubs.club_routes import clubs
from backend.facilities.facilities_routes import facilities
from backend.help_tickets.help_tickets_routes import help_tickets



def create_app():
    app = Flask(__name__)

    app.logger.setLevel(logging.DEBUG)
    app.logger.info('API startup')

    # Load environment variables from the .env file so they are
    # accessible via os.getenv() below.
    load_dotenv()

    # Secret key used by Flask for securely signing session cookies.
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Database connection settings — values come from the .env file.
    app.config["MYSQL_DATABASE_USER"] = os.getenv("DB_USER").strip()
    app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("MYSQL_ROOT_PASSWORD").strip()
    app.config["MYSQL_DATABASE_HOST"] = os.getenv("DB_HOST").strip()
    app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("DB_PORT").strip())
    app.config["MYSQL_DATABASE_DB"] = os.getenv("DB_NAME").strip()

    # Register the cleanup hook for the database connection.
    app.logger.info("create_apkp(): initializing database connection")
    init_db(app)

    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each.
    app.logger.info("create_app(): registering blueprints")
    app.register_blueprint(simple_routes)
    app.register_blueprint(users, url_prefix="/users")
    app.register_blueprint(bookings, url_prefix="/bookings")
    app.register_blueprint(spaces, url_prefix="/spaces")
    app.register_blueprint(buildings, url_prefix="/buildings")
    app.register_blueprint(facility_managers, url_prefix="/facility_managers")
    app.register_blueprint(clubs, url_prefix="/clubs")
    app.register_blueprint(facilities, url_prefix="/facilities")
    app.register_blueprint(help_tickets, url_prefix="/help_tickets")
    
    return app
