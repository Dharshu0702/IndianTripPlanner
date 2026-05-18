"""Authentication routes — signup, login, JWT tokens."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity,
)

from app.models.user import (
    create_user, find_user_by_email, find_user_by_id,
    verify_password, serialize_user,
)
from app.utils.validators import validate_signup, validate_login

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():
    """Register a new user."""
    data = request.get_json()
    valid, error = validate_signup(data)
    if not valid:
        return jsonify({"error": error}), 400

    # Check if email exists
    if find_user_by_email(data["email"]):
        return jsonify({"error": "Email already registered"}), 409

    # Create user
    user = create_user(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        role=data.get("role", "user"),
    )

    # Generate tokens
    user_id = str(user["_id"])
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)

    return jsonify({
        "message": "Account created successfully",
        "user": serialize_user(user),
        "access_token": access_token,
        "refresh_token": refresh_token,
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Login and get JWT tokens."""
    data = request.get_json()
    valid, error = validate_login(data)
    if not valid:
        return jsonify({"error": error}), 400

    user = find_user_by_email(data["email"])
    if not user or not verify_password(user["password"], data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    user_id = str(user["_id"])
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)

    return jsonify({
        "message": "Login successful",
        "user": serialize_user(user),
        "access_token": access_token,
        "refresh_token": refresh_token,
    }), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Refresh the access token."""
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return jsonify({"access_token": access_token}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    """Get current user profile."""
    user_id = get_jwt_identity()
    user = find_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user": serialize_user(user)}), 200
