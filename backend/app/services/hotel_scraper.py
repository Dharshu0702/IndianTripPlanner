"""
Hotel scraper using OpenStreetMap Nominatim search API.
Fetches real hotels near destination. Falls back to generic hotels if API is slow.
Results cached in MongoDB for 24 hours.
"""

import requests
import random
from datetime import datetime, timezone
from flask import current_app

from app import get_db
from app.utils.constants import get_destination_coords

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
UNSPLASH_BASE = "https://images.unsplash.com"

TIER_IMAGES = {
    "Budget": [
        "photo-1631049307264-da0ec9d70304",
        "photo-1566073771259-6a8506099945",
        "photo-1522771739844-6a9f6d5f14af",
    ],
    "Balanced": [
        "photo-1542314831-068cd1dbfeeb",
        "photo-1520250497591-112f2f40a3f4",
        "photo-1571003123894-1f0594d2b5d9",
    ],
    "Luxury": [
        "photo-1551882547-ff40c63fe2f5",
        "photo-1445019980597-93fa8acb246c",
        "photo-1609944213536-80ee16b0c8d5",
    ],
}

TIER_PRICE_RANGE = {
    "Budget": (600, 1800),
    "Balanced": (2500, 6000),
    "Luxury": (8000, 28000),
}

# Generic hotel chain names by tier (used when API has too few results)
GENERIC_NAMES = {
    "Budget": ["Zostel", "FabHotel Express", "OYO Flagship", "Treebo Trend", "GoStops"],
    "Balanced": ["Lemon Tree Hotel", "Sarovar Portico", "Fortune Select", "Ginger Hotel", "Keys Prima"],
    "Luxury": ["Taj Hotel", "ITC Grand", "Radisson Blu", "JW Marriott", "Hyatt Regency"],
}


def _search_hotels_nominatim(destination, lat, lng):
    """Use Nominatim to search for hotels near destination."""
    try:
        resp = requests.get(
            NOMINATIM_URL,
            params={
                "q": f"hotel near {destination} India",
                "format": "json",
                "limit": 20,
                "viewbox": f"{lng-0.3},{lat+0.3},{lng+0.3},{lat-0.3}",
                "bounded": 1,
                "addressdetails": 1,
            },
            headers={"User-Agent": "IndiaSmartTripPlanner/1.0"},
            timeout=8,
        )
        resp.raise_for_status()
        results = resp.json()
        # Filter for actual hotels/lodging
        hotels = []
        for r in results:
            name = r.get("display_name", "").split(",")[0].strip()
            if not name or len(name) < 3:
                continue
            addr = r.get("address", {})
            location = ", ".join(filter(None, [
                addr.get("road", ""),
                addr.get("suburb") or addr.get("city_district", ""),
                addr.get("city") or addr.get("town") or addr.get("village", ""),
            ]))
            if not location:
                location = destination
            hotels.append({
                "osm_id": r.get("osm_id", random.randint(100000, 999999)),
                "name": name,
                "location": location,
            })
        return hotels
    except Exception as e:
        current_app.logger.warning(f"Nominatim hotel search error: {e}")
        return []


def _make_hotel(hotel_data, tier, idx, destination):
    """Create a hotel dict with price, rating, image, website."""
    price_min, price_max = TIER_PRICE_RANGE[tier]
    price = random.randint(price_min, price_max) // 100 * 100

    base_ratings = {"Budget": 3.7, "Balanced": 4.2, "Luxury": 4.7}
    rating = round(base_ratings[tier] + random.uniform(-0.2, 0.2), 1)
    rating = min(5.0, max(3.0, rating))

    img_id = TIER_IMAGES[tier][idx % 3]
    name = hotel_data.get("name", "Hotel")
    location = hotel_data.get("location", destination)
    if destination not in location:
        location = f"{location}, {destination}"

    search_name = name.replace(" ", "+")
    website = f"https://www.google.com/search?q={search_name}+{destination.replace(' ', '+')}"

    return {
        "id": f"osm-{hotel_data.get('osm_id', idx)}",
        "name": name,
        "location": location,
        "price_per_night": price,
        "rating": rating,
        "image": f"{UNSPLASH_BASE}/{img_id}?w=400&q=80",
        "website": website,
        "source": "openstreetmap",
    }


def _make_generic(tier, destination, idx):
    """Make a generic hotel when not enough real data."""
    price_min, price_max = TIER_PRICE_RANGE[tier]
    price = random.randint(price_min, price_max) // 100 * 100
    base_ratings = {"Budget": 3.7, "Balanced": 4.2, "Luxury": 4.7}
    img_id = TIER_IMAGES[tier][idx % 3]
    name = GENERIC_NAMES[tier][idx % len(GENERIC_NAMES[tier])]
    return {
        "id": f"gen-{tier[:3].lower()}-{idx}",
        "name": f"{name}, {destination}",
        "location": f"City Centre, {destination}",
        "price_per_night": price,
        "rating": round(base_ratings[tier] + random.uniform(-0.15, 0.15), 1),
        "image": f"{UNSPLASH_BASE}/{img_id}?w=400&q=80",
        "website": f"https://www.google.com/search?q={name.replace(' ', '+')}+{destination.replace(' ', '+')}",
        "source": "generated",
    }


def _distribute_to_tiers(raw_hotels, destination):
    """Distribute scraped hotels across 3 tiers, padding to 3 each."""
    tiers = {"Budget": [], "Balanced": [], "Luxury": []}
    tier_keys = list(tiers.keys())

    for i, h in enumerate(raw_hotels):
        tier = tier_keys[i % 3]
        hotel = _make_hotel(h, tier, len(tiers[tier]), destination)
        if len(tiers[tier]) < 3:
            tiers[tier].append(hotel)

    # Pad each tier to exactly 3
    for tier in tier_keys:
        while len(tiers[tier]) < 3:
            tiers[tier].append(_make_generic(tier, destination, len(tiers[tier])))

    return tiers


def get_hotels_for_destination(destination, plan_name):
    """
    Main entry point.
    1. Check MongoDB cache
    2. Search Nominatim for real hotels near destination
    3. Distribute to tiers, cache, return requested tier
    """
    db = get_db()
    tier = plan_name.replace(" Plan", "")
    if tier not in TIER_PRICE_RANGE:
        tier = "Balanced"

    cache_key = f"hotels:{destination}"
    cached = db.hotel_cache.find_one({"cache_key": cache_key})
    if cached:
        current_app.logger.info(f"Hotel cache hit: {destination}")
        return cached["tiers"].get(tier, [])

    # Get coordinates
    coords = get_destination_coords(destination)
    if not coords:
        current_app.logger.warning(f"No coords for {destination}, generating generic hotels")
        tiers = {t: [_make_generic(t, destination, i) for i in range(3)]
                 for t in ["Budget", "Balanced", "Luxury"]}
    else:
        lat, lng = coords
        current_app.logger.info(f"Searching hotels near {destination} ({lat},{lng})")
        raw = _search_hotels_nominatim(destination, lat, lng)
        current_app.logger.info(f"Nominatim returned {len(raw)} hotels for {destination}")
        tiers = _distribute_to_tiers(raw, destination)

    # Cache in MongoDB
    db.hotel_cache.update_one(
        {"cache_key": cache_key},
        {"$set": {
            "cache_key": cache_key,
            "destination": destination,
            "tiers": tiers,
            "created_at": datetime.now(timezone.utc),
        }},
        upsert=True,
    )

    return tiers.get(tier, [])
