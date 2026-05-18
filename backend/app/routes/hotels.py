"""Hotels route — scrape and return real hotel options from OpenStreetMap."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.hotel_scraper import get_hotels_for_destination

hotels_bp = Blueprint("hotels", __name__)


@hotels_bp.route("", methods=["GET"])
@hotels_bp.route("/", methods=["GET"])
@jwt_required()
def fetch_hotels():
    """
    GET /api/hotels?destination=Alleppey&plan=Balanced Plan
    Scrapes real hotels from OpenStreetMap Overpass API.
    Returns 3 hotel options matching the plan tier.
    Results are cached for 24 hours.
    """
    destination = request.args.get("destination", "").strip()
    plan_name = request.args.get("plan", "Balanced Plan").strip()

    if not destination:
        return jsonify({"error": "destination is required"}), 400

    hotels = get_hotels_for_destination(destination, plan_name)
    return jsonify({
        "hotels": hotels,
        "destination": destination,
        "plan": plan_name,
        "source": "openstreetmap",
    }), 200
