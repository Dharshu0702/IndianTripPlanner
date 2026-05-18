"""PDF download routes."""

from flask import Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required

from app.models.trip import find_trip_by_id
from app.models.booking import find_booking_by_id
from app.services.pdf_service import generate_trip_pdf

pdf_bp = Blueprint("pdf", __name__)


@pdf_bp.route("/trip/<trip_id>/<int:plan_index>", methods=["GET"])
@jwt_required()
def download_trip_pdf(trip_id, plan_index):
    """Download PDF for a specific trip plan."""
    trip = find_trip_by_id(trip_id)
    if not trip:
        return jsonify({"error": "Trip not found"}), 404

    plans = trip.get("generated_plans", [])
    if plan_index < 0 or plan_index >= len(plans):
        return jsonify({"error": "Invalid plan index"}), 400

    plan = plans[plan_index]
    buffer = generate_trip_pdf(trip, plan)

    dest = trip["destination"]["place"].replace(" ", "_")
    filename = f"TripPlan_{dest}_{plan['plan_name'].replace(' ', '_')}.pdf"

    response = make_response(buffer.getvalue())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response


@pdf_bp.route("/booking/<booking_id>", methods=["GET"])
@jwt_required()
def download_booking_pdf(booking_id):
    """Download PDF for an approved booking."""
    booking = find_booking_by_id(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    trip = find_trip_by_id(str(booking["trip_id"]))
    if not trip:
        return jsonify({"error": "Trip not found"}), 404

    plan = booking.get("selected_plan", {})
    buffer = generate_trip_pdf(trip, plan, booking)

    dest = trip["destination"]["place"].replace(" ", "_")
    filename = f"Booking_{dest}.pdf"

    response = make_response(buffer.getvalue())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response
