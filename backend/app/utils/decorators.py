"""Custom decorators for route protection."""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from app import get_db


def admin_required(fn):
    """Decorator to restrict access to admin users only."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        db = get_db()
        current_user_id = get_jwt_identity()
        from bson import ObjectId
        user = db.users.find_one({"_id": ObjectId(current_user_id)})

        if not user or user.get("role") != "admin":
            return jsonify({"error": "Admin access required"}), 403

        return fn(*args, **kwargs)
    return wrapper
