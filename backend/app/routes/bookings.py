"""Booking routes — create, view, and manage bookings."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.booking import (
    create_booking, find_booking_by_id, find_bookings_by_user, serialize_booking,
)
from app.models.trip import find_trip_by_id
from app.models.user import find_user_by_id
from app.services.email_service import send_booking_notification_to_admin

bookings_bp = Blueprint("bookings", __name__)


@bookings_bp.route("", methods=["POST"])
@jwt_required()
def create_new_booking():
    """Create a new booking from a selected plan."""
    user_id = get_jwt_identity()
    data = request.get_json()

    trip_id = data.get("trip_id")
    selected_plan = data.get("selected_plan")
    customizations = data.get("customizations", {})

    if not trip_id or not selected_plan:
        return jsonify({"error": "trip_id and selected_plan are required"}), 400

    # Verify trip exists
    trip = find_trip_by_id(trip_id)
    if not trip:
        return jsonify({"error": "Trip not found"}), 404

    # Create booking
    booking = create_booking(trip_id, user_id, selected_plan, customizations)

    # Send email notification to admin
    user = find_user_by_id(user_id)
    send_booking_notification_to_admin(
        serialize_booking(booking), trip, user
    )

    return jsonify({
        "message": "Booking request submitted successfully",
        "booking": serialize_booking(booking),
    }), 201


@bookings_bp.route("/my-bookings", methods=["GET"])
@jwt_required()
def get_my_bookings():
    """Get all bookings for the current user."""
    user_id = get_jwt_identity()
    bookings = find_bookings_by_user(user_id)

    # Enrich with trip data
    result = []
    for b in bookings:
        booking_data = serialize_booking(b)
        trip = find_trip_by_id(str(b["trip_id"]))
        if trip:
            booking_data["trip"] = {
                "destination": trip["destination"],
                "inputs": trip["inputs"],
                "distance_km": trip.get("distance_km", 0),
            }
        result.append(booking_data)

    return jsonify({"bookings": result}), 200


@bookings_bp.route("/<booking_id>", methods=["GET"])
@jwt_required()
def get_booking(booking_id):
    """Get a specific booking."""
    booking = find_booking_by_id(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    booking_data = serialize_booking(booking)
    trip = find_trip_by_id(str(booking["trip_id"]))
    if trip:
        from app.models.trip import serialize_trip
        booking_data["trip"] = serialize_trip(trip)

    return jsonify({"booking": booking_data}), 200
