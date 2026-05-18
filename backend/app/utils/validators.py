"""Input validation utilities."""

import re
from .constants import DESTINATIONS, TRIP_TYPES


def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_signup(data):
    """Validate signup data. Returns (is_valid, error_message)."""
    if not data:
        return False, "Request body is required"

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not name or len(name) < 2:
        return False, "Name must be at least 2 characters"

    if not email or not validate_email(email):
        return False, "Valid email is required"

    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters"

    return True, None


def validate_login(data):
    """Validate login data. Returns (is_valid, error_message)."""
    if not data:
        return False, "Request body is required"

    if not data.get("email"):
        return False, "Email is required"

    if not data.get("password"):
        return False, "Password is required"

    return True, None


def validate_trip_input(data):
    """Validate trip generation input. Returns (is_valid, error_message)."""
    if not data:
        return False, "Request body is required"

    # Location validation
    location = data.get("location")
    if not location or not location.get("lat") or not location.get("lng"):
        return False, "Current location (lat, lng) is required"

    # State validation
    state = data.get("state", "").strip()
    if not state or state not in DESTINATIONS:
        return False, f"Invalid state. Must be one of: {', '.join(sorted(DESTINATIONS.keys()))}"

    # Destination validation
    destination = data.get("destination", "").strip()
    if not destination or destination not in DESTINATIONS.get(state, []):
        valid = ", ".join(DESTINATIONS.get(state, []))
        return False, f"Invalid destination for {state}. Must be one of: {valid}"

    # Travelers
    travelers = data.get("travelers")
    if not travelers or not isinstance(travelers, int) or travelers < 1 or travelers > 50:
        return False, "Number of travelers must be between 1 and 50"

    # Days
    days = data.get("days")
    if not days or not isinstance(days, int) or days < 1 or days > 30:
        return False, "Number of days must be between 1 and 30"

    # Budget
    budget = data.get("budget")
    if not budget or budget < 1000:
        return False, "Budget must be at least ₹1,000"

    # Trip type
    trip_type = data.get("trip_type", "").strip()
    if not trip_type or trip_type not in TRIP_TYPES:
        return False, f"Trip type must be one of: {', '.join(TRIP_TYPES)}"

    return True, None
