"""Destination listing routes."""

from flask import Blueprint, jsonify

from app.utils.constants import DESTINATIONS, get_all_states, get_destinations_for_state
from app.models.destination import find_destinations_by_state, get_all_destinations_grouped

destinations_bp = Blueprint("destinations", __name__)


@destinations_bp.route("/states", methods=["GET"])
def list_states():
    """Get all Indian states."""
    return jsonify({"states": get_all_states()}), 200


@destinations_bp.route("/by-state/<state>", methods=["GET"])
def list_by_state(state):
    """Get destinations for a specific state."""
    places = get_destinations_for_state(state)
    if places is None:
        return jsonify({"error": f"Invalid state: {state}"}), 404

    # Try to get enriched data from DB
    db_data = find_destinations_by_state(state)
    db_map = {d["name"]: d for d in db_data}

    result = []
    for place in places:
        info = db_map.get(place, {})
        result.append({
            "name": place,
            "state": state,
            "description": info.get("description", f"{place} is a popular destination in {state}, India."),
            "attractions": info.get("attractions", []),
            "avg_hotel_price": info.get("avg_hotel_price", 0),
            "best_time_to_visit": info.get("best_time_to_visit", ""),
        })

    return jsonify({"state": state, "destinations": result}), 200


@destinations_bp.route("/all", methods=["GET"])
def list_all():
    """Get all destinations grouped by state."""
    return jsonify({"destinations": DESTINATIONS}), 200
