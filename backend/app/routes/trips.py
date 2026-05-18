"""Trip routes — generate AI plans, get trips."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.trip import create_trip, find_trip_by_id, find_trips_by_user, serialize_trip
from app.services.maps_service import get_distance_data, generate_maps_link
from app.services.ai_service import generate_trip_plans
from app.services.cost_engine import calculate_total_cost, suggest_transport
from app.utils.validators import validate_trip_input

trips_bp = Blueprint("trips", __name__)


@trips_bp.route("/generate", methods=["POST"])
@jwt_required()
def generate_plans():
    """Generate 3 AI-based travel plans."""
    user_id = get_jwt_identity()
    data = request.get_json()

    valid, error = validate_trip_input(data)
    if not valid:
        return jsonify({"error": error}), 400

    location = data["location"]
    state = data["state"]
    destination = data["destination"]
    travelers = data["travelers"]
    days = data["days"]
    budget = data["budget"]
    trip_type = data["trip_type"]

    # Calculate distance (OSRM road distance)
    distance_data = get_distance_data(location["lat"], location["lng"], destination)

    # Label the OSRM duration as road travel time
    distance_data["road_duration"] = distance_data.get("duration", "")

    # Generate maps link
    maps_link = generate_maps_link(location["lat"], location["lng"], destination)

    # Generate AI plans (each plan will have its own travel_time based on mode)
    plans, source = generate_trip_plans(
        user_location=location.get("address", f"{location['lat']}, {location['lng']}"),
        destination=destination,
        state=state,
        distance_km=distance_data["distance_km"],
        travelers=travelers,
        days=days,
        budget=budget,
        trip_type=trip_type,
    )

    # Add maps link to each plan
    for plan in plans:
        plan["maps_link"] = maps_link

    # Use the first plan's travel time as the trip-level display
    # (each plan has its own travel_time already set by ai_service)
    if plans and plans[0].get("travel_time"):
        distance_data["duration"] = plans[0]["travel_time"]

    # Save trip to database
    trip = create_trip(
        user_id=user_id,
        location=location,
        state=state,
        destination=destination,
        inputs={"travelers": travelers, "days": days, "budget": budget, "trip_type": trip_type},
        distance_data=distance_data,
        generated_plans=plans,
    )

    return jsonify({
        "message": "Plans generated successfully",
        "trip": serialize_trip(trip),
        "distance": distance_data,
        "maps_link": maps_link,
        "ai_source": source,
    }), 201


@trips_bp.route("/my-trips", methods=["GET"])
@jwt_required()
def get_my_trips():
    """Get all trips for the current user."""
    user_id = get_jwt_identity()
    trips = find_trips_by_user(user_id)
    return jsonify({"trips": [serialize_trip(t) for t in trips]}), 200


@trips_bp.route("/<trip_id>", methods=["GET"])
@jwt_required()
def get_trip(trip_id):
    """Get a specific trip by ID."""
    trip = find_trip_by_id(trip_id)
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    return jsonify({"trip": serialize_trip(trip)}), 200


@trips_bp.route("/recalculate", methods=["POST"])
@jwt_required()
def recalculate_cost():
    """Recalculate cost with customized parameters."""
    data = request.get_json()
    distance_km = data.get("distance_km", 0)
    days = data.get("days", 1)
    travelers = data.get("travelers", 1)
    trip_type = data.get("trip_type", "Budget")
    transport_mode = data.get("transport_mode")
    num_places = data.get("num_places", 0)

    if not transport_mode:
        transport_mode = suggest_transport(distance_km, trip_type)

    cost = calculate_total_cost(distance_km, days, travelers, trip_type, transport_mode, num_places)

    return jsonify({"cost_breakdown": cost}), 200

