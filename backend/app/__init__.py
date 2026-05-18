from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from pymongo import MongoClient

from .config import Config

# Global extensions
jwt = JWTManager()
mail = Mail()
mongo_client = None
db = None


def create_app(config_class=Config):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])
    jwt.init_app(app)
    mail.init_app(app)

    # MongoDB connection
    global mongo_client, db
    mongo_client = MongoClient(app.config["MONGO_URI"])
    db_name = app.config["MONGO_URI"].rsplit("/", 1)[-1].split("?")[0]
    db = mongo_client[db_name]

    # Create indexes
    _create_indexes(db)

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.trips import trips_bp
    from .routes.bookings import bookings_bp
    from .routes.destinations import destinations_bp
    from .routes.admin import admin_bp
    from .routes.pdf import pdf_bp
    from .routes.hotels import hotels_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(trips_bp, url_prefix="/api/trips")
    app.register_blueprint(bookings_bp, url_prefix="/api/bookings")
    app.register_blueprint(destinations_bp, url_prefix="/api/destinations")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(pdf_bp, url_prefix="/api/pdf")
    app.register_blueprint(hotels_bp, url_prefix="/api/hotels")

    # Health check
    @app.route("/api/health")
    def health():
        return {"status": "healthy", "app": "India Smart Trip Planner"}

    return app


def _create_indexes(database):
    """Create MongoDB indexes for performance."""
    database.users.create_index("email", unique=True)
    database.trips.create_index("user_id")
    database.bookings.create_index("user_id")
    database.bookings.create_index("trip_id")
    database.ai_cache.create_index("cache_key", unique=True)
    database.ai_cache.create_index("created_at", expireAfterSeconds=86400)
    database.hotel_cache.create_index("cache_key", unique=True)
    database.hotel_cache.create_index("created_at", expireAfterSeconds=86400)
    database.destinations.create_index([("state", 1), ("name", 1)], unique=True)


def get_db():
    """Get the database instance."""
    return db
