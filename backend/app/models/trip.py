"""Trip model helpers for MongoDB."""

from datetime import datetime, timezone
from bson import ObjectId

from app import get_db


def create_trip(user_id, location, state, destination, inputs, distance_data, generated_plans):
    """Create a new trip document."""
    db = get_db()

    trip_doc = {
        "user_id": ObjectId(user_id),
        "origin_location": {
            "lat": location["lat"],
            "lng": location["lng"],
            "address": location.get("address", ""),
        },
        "destination": {
            "state": state,
            "place": destination,
        },
        "inputs": {
            "travelers": inputs["travelers"],
            "days": inputs["days"],
            "budget": inputs["budget"],
            "trip_type": inputs["trip_type"],
        },
        "distance_km": distance_data.get("distance_km", 0),
        "travel_time": distance_data.get("duration", ""),
        "generated_plans": generated_plans,
        "created_at": datetime.now(timezone.utc),
    }

    result = db.trips.insert_one(trip_doc)
    trip_doc["_id"] = result.inserted_id
    return trip_doc


def find_trip_by_id(trip_id):
    """Find a trip by ID."""
    db = get_db()
    return db.trips.find_one({"_id": ObjectId(trip_id)})


def find_trips_by_user(user_id):
    """Find all trips for a user."""
    db = get_db()
    return list(
        db.trips.find({"user_id": ObjectId(user_id)}).sort("created_at", -1)
    )


def serialize_trip(trip):
    """Convert trip document to JSON-serializable dict."""
    if not trip:
        return None
    return {
        "id": str(trip["_id"]),
        "user_id": str(trip["user_id"]),
        "origin_location": trip["origin_location"],
        "destination": trip["destination"],
        "inputs": trip["inputs"],
        "distance_km": trip.get("distance_km", 0),
        "travel_time": trip.get("travel_time", ""),
        "generated_plans": trip.get("generated_plans", []),
        "created_at": trip["created_at"].isoformat(),
    }
