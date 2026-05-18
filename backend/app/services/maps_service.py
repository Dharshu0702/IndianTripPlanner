"""Distance & routing service using OSRM (open-source) with Haversine fallback."""

import math
import requests
from flask import current_app

from app import get_db
from app.utils.constants import get_destination_coords

# Public OSRM demo server (free, no API key needed)
OSRM_BASE_URL = "https://router.project-osrm.org"


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points using Haversine formula."""
    R = 6371  # Earth's radius in km

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return round(R * c, 2)


def estimate_duration(distance_km):
    """Estimate travel duration based on distance."""
    if distance_km < 300:
        hours = distance_km / 50  # Avg road speed ~50 km/h
    elif distance_km <= 800:
        hours = distance_km / 60  # Train avg ~60 km/h
    else:
        hours = (distance_km / 700) + 3  # Flight + airport overhead

    h = int(hours)
    m = int((hours - h) * 60)
    return f"{h}h {m}m"


def _query_osrm(origin_lat, origin_lng, dest_lat, dest_lng):
    """
    Query the OSRM routing API for driving distance and duration.
    OSRM uses (lng, lat) order in the URL.
    Returns (distance_km, duration_text) or None on failure.
    """
    try:
        url = (
            f"{OSRM_BASE_URL}/route/v1/driving/"
            f"{origin_lng},{origin_lat};{dest_lng},{dest_lat}"
            f"?overview=false&alternatives=false"
        )
        resp = requests.get(url, timeout=10, headers={"User-Agent": "IndiaSmartTripPlanner/1.0"})
        resp.raise_for_status()
        data = resp.json()

        if data.get("code") == "Ok" and data.get("routes"):
            route = data["routes"][0]
            distance_km = round(route["distance"] / 1000, 2)
            duration_secs = route["duration"]
            h = int(duration_secs // 3600)
            m = int((duration_secs % 3600) // 60)
            duration_text = f"{h}h {m}m"
            return distance_km, duration_text

    except Exception as e:
        current_app.logger.warning(f"OSRM routing error: {e}")

    return None


def get_distance_data(origin_lat, origin_lng, destination_name):
    """
    Get distance and duration between origin and destination.
    Uses OSRM routing API first, falls back to Haversine.
    Results are cached in MongoDB.
    """
    db = get_db()

    # Check cache first
    cache_key = f"{round(origin_lat, 4)}_{round(origin_lng, 4)}_{destination_name}"
    cached = db.distance_cache.find_one({"cache_key": cache_key})
    if cached:
        return {
            "distance_km": cached["distance_km"],
            "duration": cached["duration"],
            "source": cached.get("source", "cache"),
        }

    # Get destination coordinates
    dest_coords = get_destination_coords(destination_name)
    if not dest_coords:
        return {"distance_km": 0, "duration": "Unknown", "source": "error"}

    dest_lat, dest_lng = dest_coords
    result = None

    # Try OSRM for real road distance
    osrm_result = _query_osrm(origin_lat, origin_lng, dest_lat, dest_lng)
    if osrm_result:
        distance_km, duration = osrm_result
        result = {
            "distance_km": distance_km,
            "duration": duration,
            "source": "osrm",
        }

    # Fallback to Haversine
    if not result:
        distance_km = haversine_distance(origin_lat, origin_lng, dest_lat, dest_lng)
        # Road distance is typically 1.3x straight-line distance
        road_distance = round(distance_km * 1.3, 2)
        duration = estimate_duration(road_distance)
        result = {
            "distance_km": road_distance,
            "duration": duration,
            "source": "haversine",
        }

    # Cache the result
    from datetime import datetime, timezone
    db.distance_cache.update_one(
        {"cache_key": cache_key},
        {
            "$set": {
                "cache_key": cache_key,
                "distance_km": result["distance_km"],
                "duration": result["duration"],
                "source": result["source"],
                "created_at": datetime.now(timezone.utc),
            }
        },
        upsert=True,
    )

    return result


def generate_maps_link(origin_lat, origin_lng, destination_name):
    """Generate an OpenStreetMap directions link."""
    dest_coords = get_destination_coords(destination_name)
    if not dest_coords:
        return f"https://www.openstreetmap.org/search?query={destination_name},+India"

    dest_lat, dest_lng = dest_coords
    return (
        f"https://www.openstreetmap.org/directions?"
        f"engine=fossgis_osrm_car&route={origin_lat},{origin_lng};{dest_lat},{dest_lng}"
    )


def get_route_coords(origin_lat, origin_lng, destination_name):
    """
    Get route geometry (polyline coordinates) from OSRM for Leaflet map display.
    Returns list of [lat, lng] pairs or None.
    """
    dest_coords = get_destination_coords(destination_name)
    if not dest_coords:
        return None

    dest_lat, dest_lng = dest_coords

    try:
        url = (
            f"{OSRM_BASE_URL}/route/v1/driving/"
            f"{origin_lng},{origin_lat};{dest_lng},{dest_lat}"
            f"?overview=full&geometries=geojson"
        )
        resp = requests.get(url, timeout=10, headers={"User-Agent": "IndiaSmartTripPlanner/1.0"})
        resp.raise_for_status()
        data = resp.json()

        if data.get("code") == "Ok" and data.get("routes"):
            # GeoJSON coordinates are [lng, lat] — flip to [lat, lng] for Leaflet
            coords = data["routes"][0]["geometry"]["coordinates"]
            return [[c[1], c[0]] for c in coords]

    except Exception as e:
        current_app.logger.warning(f"OSRM geometry error: {e}")

    # Fallback: straight line
    return [[origin_lat, origin_lng], [dest_lat, dest_lng]]
