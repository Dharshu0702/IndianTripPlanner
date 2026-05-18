"""Admin routes — manage bookings, view stats, users."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.utils.decorators import admin_required
from app.models.booking import (
    find_all_bookings, find_booking_by_id, update_booking_status, serialize_booking,
)
from app.models.trip import find_trip_by_id
from app.models.user import find_user_by_id, serialize_user
from app.services.email_service import send_booking_status_update
from app import get_db

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/stats", methods=["GET"])
@jwt_required()
@admin_required
def get_stats():
    """Get dashboard statistics."""
    db = get_db()
    total_users = db.users.count_documents({})
    total_trips = db.trips.count_documents({})
    total_bookings = db.bookings.count_documents({})
    pending = db.bookings.count_documents({"status": "pending"})
    approved = db.bookings.count_documents({"status": "approved"})
    rejected = db.bookings.count_documents({"status": "rejected"})

    return jsonify({
        "stats": {
            "total_users": total_users,
            "total_trips": total_trips,
            "total_bookings": total_bookings,
            "pending_bookings": pending,
            "approved_bookings": approved,
            "rejected_bookings": rejected,
        }
    }), 200


@admin_bp.route("/bookings", methods=["GET"])
@jwt_required()
@admin_required
def get_all_bookings_admin():
    """Get all bookings with trip and user details."""
    bookings = find_all_bookings()
    result = []
    for b in bookings:
        booking_data = serialize_booking(b)
        trip = find_trip_by_id(str(b["trip_id"]))
        user = find_user_by_id(str(b["user_id"]))
        if trip:
            booking_data["trip"] = {
                "destination": trip["destination"],
                "inputs": trip["inputs"],
                "distance_km": trip.get("distance_km", 0),
                "origin_location": trip.get("origin_location", {}),
            }
        if user:
            booking_data["user"] = serialize_user(user)
        result.append(booking_data)

    return jsonify({"bookings": result}), 200


@admin_bp.route("/bookings/<booking_id>/status", methods=["PATCH"])
@jwt_required()
@admin_required
def update_status(booking_id):
    """Approve or reject a booking."""
    data = request.get_json()
    status = data.get("status")
    admin_notes = data.get("admin_notes", "")

    if status not in ("approved", "rejected"):
        return jsonify({"error": "Status must be 'approved' or 'rejected'"}), 400

    booking = find_booking_by_id(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    updated = update_booking_status(booking_id, status, admin_notes)
    if not updated:
        return jsonify({"error": "Failed to update booking"}), 500

    # Send email to user
    user = find_user_by_id(str(booking["user_id"]))
    trip = find_trip_by_id(str(booking["trip_id"]))
    if user and trip:
        booking["status"] = status
        booking["admin_notes"] = admin_notes
        send_booking_status_update(user["email"], user["name"], booking, trip, status)

    return jsonify({"message": f"Booking {status}", "status": status}), 200


@admin_bp.route("/users", methods=["GET"])
@jwt_required()
@admin_required
def get_all_users():
    """Get all users."""
    db = get_db()
    users = list(db.users.find().sort("created_at", -1))
    return jsonify({"users": [serialize_user(u) for u in users]}), 200


@admin_bp.route("/cache/clear", methods=["DELETE"])
@jwt_required()
@admin_required
def clear_ai_cache():
    """Clear AI plan cache so next generation uses updated logic."""
    db = get_db()
    ai_result = db.ai_cache.delete_many({})
    dist_result = db.distance_cache.delete_many({})
    hotel_result = db.hotel_cache.delete_many({})
    return jsonify({
        "message": "Cache cleared successfully",
        "ai_cache_cleared": ai_result.deleted_count,
        "distance_cache_cleared": dist_result.deleted_count,
        "hotel_cache_cleared": hotel_result.deleted_count,
    }), 200

