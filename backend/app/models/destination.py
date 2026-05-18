"""Destination model helpers for MongoDB."""

from app import get_db


def find_destinations_by_state(state):
    """Find all destinations for a given state."""
    db = get_db()
    return list(db.destinations.find({"state": state}, {"_id": 0}))


def find_destination(state, name):
    """Find a specific destination by state and name."""
    db = get_db()
    return db.destinations.find_one({"state": state, "name": name}, {"_id": 0})


def upsert_destination(state, name, data):
    """Insert or update a destination document."""
    db = get_db()
    db.destinations.update_one(
        {"state": state, "name": name},
        {"$set": data},
        upsert=True,
    )


def get_all_destinations_grouped():
    """Get all destinations grouped by state."""
    db = get_db()
    destinations = list(db.destinations.find({}, {"_id": 0}).sort([("state", 1), ("name", 1)]))

    grouped = {}
    for dest in destinations:
        state = dest["state"]
        if state not in grouped:
            grouped[state] = []
        grouped[state].append(dest)

    return grouped
