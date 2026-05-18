"""Booking model helpers for MongoDB."""

from datetime import datetime, timezone
from bson import ObjectId

from app import get_db


def create_booking(trip_id, user_id, selected_plan, customizations=None):
    """Create a new booking document."""
    db = get_db()

    booking_doc = {
        "trip_id": ObjectId(trip_id),
        "user_id": ObjectId(user_id),
        "selected_plan": selected_plan,
        "customizations": customizations or {},
        "status": "pending",
        "admin_notes": "",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    result = db.bookings.insert_one(booking_doc)
    booking_doc["_id"] = result.inserted_id
    return booking_doc


def find_booking_by_id(booking_id):
    """Find a booking by ID."""
    db = get_db()
    return db.bookings.find_one({"_id": ObjectId(booking_id)})


def find_bookings_by_user(user_id):
    """Find all bookings for a user."""
    db = get_db()
    return list(
        db.bookings.find({"user_id": ObjectId(user_id)}).sort("created_at", -1)
    )


def find_all_bookings():
    """Find all bookings (admin)."""
    db = get_db()
    return list(db.bookings.find().sort("created_at", -1))


def update_booking_status(booking_id, status, admin_notes=""):
    """Update booking status (approve/reject)."""
    db = get_db()
    result = db.bookings.update_one(
        {"_id": ObjectId(booking_id)},
        {
            "$set": {
                "status": status,
                "admin_notes": admin_notes,
                "updated_at": datetime.now(timezone.utc),
            }
        },
    )
    return result.modified_count > 0


def update_booking_customizations(booking_id, customizations, updated_plan):
    """Update booking customizations and recalculated plan."""
    db = get_db()
    result = db.bookings.update_one(
        {"_id": ObjectId(booking_id)},
        {
            "$set": {
                "customizations": customizations,
                "selected_plan": updated_plan,
                "updated_at": datetime.now(timezone.utc),
            }
        },
    )
    return result.modified_count > 0


def serialize_booking(booking):
    """Convert booking document to JSON-serializable dict."""
    if not booking:
        return None
    return {
        "id": str(booking["_id"]),
        "trip_id": str(booking["trip_id"]),
        "user_id": str(booking["user_id"]),
        "selected_plan": booking.get("selected_plan", {}),
        "customizations": booking.get("customizations", {}),
        "status": booking["status"],
        "admin_notes": booking.get("admin_notes", ""),
        "created_at": booking["created_at"].isoformat(),
        "updated_at": booking["updated_at"].isoformat(),
    }
