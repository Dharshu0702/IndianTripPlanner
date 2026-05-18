"""User model helpers for MongoDB."""

from datetime import datetime, timezone
import bcrypt
from bson import ObjectId

from app import get_db


def create_user(name, email, password, role="user"):
    """Create a new user document in MongoDB."""
    db = get_db()
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    user_doc = {
        "name": name.strip(),
        "email": email.strip().lower(),
        "password": hashed,  # stored as bytes
        "role": role,
        "created_at": datetime.now(timezone.utc),
    }

    result = db.users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    return user_doc


def find_user_by_email(email):
    """Find a user by email."""
    db = get_db()
    return db.users.find_one({"email": email.strip().lower()})


def find_user_by_id(user_id):
    """Find a user by ObjectId."""
    db = get_db()
    return db.users.find_one({"_id": ObjectId(user_id)})


def verify_password(stored_hash, password):
    """Verify password against stored bcrypt hash.
    Handles both bytes (normal signup) and str (reset via script).
    """
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode("utf-8")
    return bcrypt.checkpw(password.encode("utf-8"), stored_hash)


def serialize_user(user):
    """Convert user document to JSON-serializable dict."""
    if not user:
        return None
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "created_at": user["created_at"].isoformat(),
    }
