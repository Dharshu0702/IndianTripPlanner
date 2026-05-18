"""Ollama AI service for generating trip plans."""

import json
import hashlib
import re
import requests
from datetime import datetime, timezone
from flask import current_app

from app import get_db
from app.services.cost_engine import generate_cost_variants, suggest_transport
from app.utils.constants import HOTEL_RATES, FOOD_RATES, TRANSPORT_RATES


# ── Realistic hotel names by tier and destination ──
BUDGET_HOTELS = [
    "OYO Rooms", "FabHotel", "Treebo Trend", "Hotel Sai Palace",
    "Zostel Hostel", "GoStops", "Hotel Rahi", "Lodge Comfort",
]
BALANCED_HOTELS = [
    "Hotel Lemon Tree", "Ginger Hotel", "Country Inn & Suites",
    "Fortune Hotel", "Keys Select Hotel", "Clarks Inn", "Sarovar Portico",
]
LUXURY_HOTELS = [
    "Taj Hotel & Resort", "ITC Grand", "The Oberoi", "Radisson Blu",
    "JW Marriott", "Hyatt Regency", "The Lalit", "Vivanta by Taj",
]

# ── Curated places to visit by destination ──
DESTINATION_PLACES = {
    "Tirupati": ["Tirumala Temple", "Sri Padmavathi Temple", "Talakona Waterfalls", "Chandragiri Fort", "Sri Venkateswara National Park"],
    "Araku Valley": ["Borra Caves", "Katiki Waterfalls", "Tribal Museum", "Coffee Plantations", "Galikonda View Point"],
    "Visakhapatnam": ["RK Beach", "Submarine Museum", "Kailasagiri", "Simhachalam Temple", "Dolphin's Nose"],
    "Shimla": ["Mall Road", "Jakhu Temple", "The Ridge", "Kufri", "Christ Church", "Scandal Point"],
    "Manali": ["Hadimba Temple", "Solang Valley", "Rohtang Pass", "Old Manali", "Manu Temple", "Vashisht Hot Springs"],
    "Dharamshala": ["McLeod Ganj", "Bhagsu Waterfall", "Namgyal Monastery", "Dal Lake", "Triund Trek"],
    "Jaipur": ["Amber Fort", "Hawa Mahal", "City Palace", "Jantar Mantar", "Nahargarh Fort", "Jal Mahal"],
    "Udaipur": ["City Palace", "Lake Pichola", "Jag Mandir", "Saheliyon ki Bari", "Fateh Sagar Lake"],
    "Jaisalmer": ["Jaisalmer Fort", "Sam Sand Dunes", "Patwon Ki Haveli", "Gadisar Lake", "Desert Safari"],
    "Baga Beach": ["Baga Beach", "Fort Aguada", "Chapora Fort", "Anjuna Flea Market", "Saturday Night Market", "Calangute Beach"],
    "Palolem Beach": ["Palolem Beach", "Butterfly Beach", "Cabo de Rama Fort", "Cola Beach", "Canacona Island"],
    "Basilica of Bom Jesus": ["Basilica of Bom Jesus", "Se Cathedral", "Fort Aguada", "Dona Paula", "Miramar Beach"],
    "Munnar": ["Tea Gardens", "Eravikulam National Park", "Mattupetty Dam", "Top Station", "Echo Point", "Attukal Waterfalls"],
    "Alleppey": ["Houseboat Cruise", "Alleppey Beach", "Marari Beach", "Krishnapuram Palace", "Revi Karunakaran Museum"],
    "Fort Kochi": ["Chinese Fishing Nets", "Fort Kochi Beach", "Jew Town", "Mattancherry Palace", "Santa Cruz Cathedral"],
    "Taj Mahal": ["Taj Mahal", "Agra Fort", "Fatehpur Sikri", "Mehtab Bagh", "Itimad-ud-Daulah"],
    "Varanasi": ["Kashi Vishwanath Temple", "Dashashwamedh Ghat", "Sarnath", "Assi Ghat", "Manikarnika Ghat"],
    "Rishikesh": ["Laxman Jhula", "Ram Jhula", "Triveni Ghat", "Beatles Ashram", "River Rafting", "Neer Garh Waterfall"],
    "Nainital": ["Naini Lake", "Mall Road", "Snow View Point", "Naina Devi Temple", "Tiffin Top"],
    "Kolkata": ["Victoria Memorial", "Howrah Bridge", "Indian Museum", "Dakshineswar Kali Temple", "Park Street"],
    "Darjeeling": ["Tiger Hill", "Batasia Loop", "Tea Gardens", "Darjeeling Himalayan Railway", "Peace Pagoda"],
    "Golden Temple": ["Golden Temple", "Jallianwala Bagh", "Partition Museum", "Wagah Border", "Gobindgarh Fort"],
    "Gangtok": ["MG Marg", "Rumtek Monastery", "Tsomgo Lake", "Hanuman Tok", "Enchey Monastery"],
    "Ooty": ["Botanical Gardens", "Ooty Lake", "Doddabetta Peak", "Rose Garden", "Tea Factory"],
    "Madurai": ["Meenakshi Temple", "Thirumalai Nayakkar Mahal", "Gandhi Memorial Museum", "Alagar Kovil"],
    "Kanyakumari": ["Vivekananda Rock Memorial", "Thiruvalluvar Statue", "Sunrise Point", "Padmanabhapuram Palace"],
    "Hampi": ["Virupaksha Temple", "Vittala Temple", "Elephant Stables", "Lotus Mahal", "Hemakuta Hill"],
    "Coorg": ["Abbey Falls", "Raja's Seat", "Dubare Elephant Camp", "Talakaveri", "Namdroling Monastery"],
    "Charminar": ["Charminar", "Golconda Fort", "Mecca Masjid", "Laad Bazaar", "Salar Jung Museum"],
    "Puri Beach": ["Puri Beach", "Jagannath Temple", "Konark Sun Temple", "Chilika Lake", "Raghurajpur Artist Village"],
    "Kaziranga National Park": ["Elephant Safari", "Jeep Safari", "Central Range", "Western Range", "Orchid Garden"],
    "Bodh Gaya": ["Mahabodhi Temple", "Great Buddha Statue", "Thai Monastery", "Bodhi Tree", "Royal Bhutan Monastery"],
    "Shillong": ["Elephant Falls", "Ward's Lake", "Don Bosco Museum", "Shillong Peak", "Umiam Lake"],
}


def _get_hotel_name(destination, tier):
    """Get a realistic hotel name matching the price tier."""
    import random
    if tier == "Budget Plan":
        base = random.choice(BUDGET_HOTELS)
    elif tier == "Balanced Plan":
        base = random.choice(BALANCED_HOTELS)
    else:
        base = random.choice(LUXURY_HOTELS)

    # Add destination context for some
    if "OYO" in base or "Zostel" in base or "GoStops" in base or "Ginger" in base:
        return f"{base}, {destination}"
    return f"{base}, {destination}"


def _get_places(destination):
    """Get curated places list for destination."""
    places = DESTINATION_PLACES.get(destination)
    if places:
        return places

    # Fallback: generate generic but realistic places
    return [
        f"{destination} Main Temple/Monument",
        f"Local Market, {destination}",
        f"{destination} View Point",
        f"Heritage Walk, {destination}",
        f"Nature Trail near {destination}",
    ]


def _estimate_flight_time(distance_km):
    """Estimate realistic flight travel time including transfers."""
    flight_hours = distance_km / 700  # ~700 km/h cruise speed
    # Add 3h for: airport transit (1h), boarding (0.5h), arrival (0.5h), buffer (1h)
    total_hours = flight_hours + 3
    h = int(total_hours)
    m = int((total_hours - h) * 60)
    return f"{h}h {m}m"


def _estimate_travel_time(distance_km, transport_mode):
    """Estimate realistic travel time based on mode."""
    if transport_mode in ("flight",):
        return _estimate_flight_time(distance_km)
    elif transport_mode in ("train", "train_ac"):
        hours = distance_km / 55  # Indian trains avg ~55 km/h including stops
        h = int(hours)
        m = int((hours - h) * 60)
        return f"{h}h {m}m"
    else:  # bus, cab
        hours = distance_km / 45  # Indian roads avg ~45 km/h
        h = int(hours)
        m = int((hours - h) * 60)
        return f"{h}h {m}m"


def _build_prompt(user_location, destination, state, distance_km, travelers, days, budget, trip_type):
    """Build the LLM prompt for trip generation."""
    cab_note = ""
    if travelers > 4:
        num_cabs = max(1, -(-travelers // 4))
        cab_note = f"\nIMPORTANT: Since there are {travelers} travelers (more than 4), suggest {num_cabs} cabs for local transport."

    prompt = f"""You are an expert Indian travel planner. Generate exactly 3 travel plans as a valid JSON array.

CONTEXT:
- Origin: {user_location}
- Destination: {destination}, {state}, India
- Distance: {distance_km:.0f} km
- Travelers: {travelers}
- Days: {days}
- Budget: ₹{budget:,} INR
- Trip Type: {trip_type}{cab_note}

RULES:
- Day 1 MUST be "Travel to {destination}" (departure from origin)
- Final day MUST be "Return journey" (departure from {destination})
- Itinerary MUST have EXACTLY {days} days (Day 1 to Day {days})
- Budget Plan hotels: OYO, FabHotel, Zostel (₹500-1500/night)
- Balanced Plan hotels: Lemon Tree, Ginger, Fortune (₹1500-4000/night)
- Luxury Plan hotels: Taj, Oberoi, Marriott (₹5000-25000/night)
- Hotel cost MUST be realistic for the hotel named
- All costs in Indian Rupees (₹)

Return ONLY a JSON array of 3 objects. Each object has keys:
plan_name, travel_mode, travel_cost, hotel_name, hotel_cost_per_night,
food_cost_per_day, local_transport_per_day, places_to_visit (array),
day_wise_itinerary (array of {{day, title, activities[]}}), total_cost

JSON ONLY, no explanation:"""

    return prompt


def _generate_cache_key(destination, state, travelers, days, budget, trip_type, distance_km):
    """Generate a deterministic cache key from inputs."""
    key_str = f"{destination}|{state}|{travelers}|{days}|{budget}|{trip_type}|{round(distance_km, -1)}"
    return hashlib.sha256(key_str.encode()).hexdigest()


def _parse_ai_response(response_text):
    """Extract and parse JSON from LLM response."""
    # Try direct parse first
    try:
        plans = json.loads(response_text)
        if isinstance(plans, list) and len(plans) == 3:
            return plans
    except json.JSONDecodeError:
        pass

    # Try to find JSON array in the response
    json_match = re.search(r'\[[\s\S]*\]', response_text)
    if json_match:
        try:
            plans = json.loads(json_match.group())
            if isinstance(plans, list) and len(plans) >= 3:
                return plans[:3]
        except json.JSONDecodeError:
            pass

    # Try to find individual JSON objects
    objects = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text)
    if len(objects) >= 3:
        plans = []
        for obj_str in objects[:3]:
            try:
                plans.append(json.loads(obj_str))
            except json.JSONDecodeError:
                continue
        if len(plans) == 3:
            return plans

    return None


def _generate_fallback_plans(destination, state, distance_km, travelers, days, trip_type, user_location):
    """Generate template-based plans when LLM fails. Fully validated."""
    cost_variants = generate_cost_variants(distance_km, days, travelers)
    places = _get_places(destination)

    plan_tiers = ["Budget Plan", "Balanced Plan", "Luxury Plan"]
    plans = []

    for i, variant in enumerate(cost_variants):
        plan_name = plan_tiers[i] if i < 3 else variant["plan_name"]
        hotel_name = _get_hotel_name(destination, plan_name)

        # Generate day-wise itinerary (EXACTLY `days` entries)
        itinerary = []
        for d in range(1, days + 1):
            if d == 1:
                title = f"Travel to {destination}"
                activities = [
                    f"Depart from {user_location} via {variant['transport_mode']}",
                    f"Arrive at {destination}, {state}",
                    f"Check into {hotel_name}",
                    "Freshen up and evening leisure",
                ]
            elif d == days:
                title = f"Return from {destination}"
                activities = [
                    "Breakfast and hotel checkout",
                    "Last-minute local sightseeing or shopping",
                    f"Depart {destination} via {variant['transport_mode']}",
                    f"Arrive back at origin",
                ]
            else:
                # Exploration days — cycle through places
                place_idx = (d - 2) % len(places)
                next_place_idx = (d - 1) % len(places)
                title = f"Explore {places[place_idx]}"
                activities = [
                    "Breakfast at hotel",
                    f"Visit {places[place_idx]}",
                    "Lunch at local restaurant",
                    f"Visit {places[next_place_idx]}",
                    "Evening leisure or shopping",
                    "Dinner",
                ]

            itinerary.append({
                "day": d,
                "title": title,
                "activities": activities,
            })

        plans.append({
            "plan_name": plan_name,
            "travel_mode": variant["transport_mode"],
            "travel_cost": variant["travel_cost"],
            "hotel_name": hotel_name,
            "hotel_cost_per_night": variant["hotel_cost_per_night"],
            "food_cost_per_day": variant["food_per_person_per_day"] * travelers,
            "local_transport_per_day": variant["local_transport_per_day"],
            "places_to_visit": places,
            "day_wise_itinerary": itinerary,
            "total_cost": variant["total_cost"],
        })

    return plans


def _validate_and_fix_plan(plan, cost_data, destination, state, days, travelers, user_location):
    """
    Post-process an AI-generated plan to fix common issues:
    - Hotel name must match price tier
    - Costs must be realistic (override with cost engine if wildly off)
    - Itinerary must have exactly `days` entries
    - Day 1 must reference destination (not origin)
    """
    plan_name = plan.get("plan_name", "Balanced Plan")

    # ── Fix 1: Ensure hotel name matches price tier ──
    hotel_cost = plan.get("hotel_cost_per_night", 0)
    hotel_name = plan.get("hotel_name", "")

    # Check for tier mismatch (luxury hotel with budget price or vice versa)
    luxury_keywords = ["leela", "taj", "oberoi", "marriott", "hyatt", "itc grand", "ritz", "four seasons"]
    budget_keywords = ["oyo", "fabhotel", "zostel", "gostops", "lodge", "dormitory"]

    name_lower = hotel_name.lower()
    is_luxury_name = any(k in name_lower for k in luxury_keywords)
    is_budget_name = any(k in name_lower for k in budget_keywords)

    if plan_name == "Budget Plan" and (is_luxury_name or hotel_cost > 2000):
        plan["hotel_name"] = _get_hotel_name(destination, "Budget Plan")
        plan["hotel_cost_per_night"] = cost_data["hotel_cost_per_night"]
    elif plan_name == "Balanced Plan" and (is_luxury_name and hotel_cost < 3000):
        plan["hotel_name"] = _get_hotel_name(destination, "Balanced Plan")
        plan["hotel_cost_per_night"] = cost_data["hotel_cost_per_night"]
    elif plan_name == "Luxury Plan" and (is_budget_name or hotel_cost < 4000):
        plan["hotel_name"] = _get_hotel_name(destination, "Luxury Plan")
        plan["hotel_cost_per_night"] = cost_data["hotel_cost_per_night"]

    # ── Fix 2: Override costs with cost engine values (always accurate) ──
    plan["travel_cost"] = cost_data["travel_cost"]
    plan["travel_mode"] = cost_data["transport_mode"]
    plan["hotel_cost_per_night"] = cost_data["hotel_cost_per_night"]
    plan["food_cost_per_day"] = cost_data["food_per_person_per_day"] * travelers
    plan["local_transport_per_day"] = cost_data["local_transport_per_day"]
    plan["total_cost"] = cost_data["total_cost"]

    # ── Fix 3: Ensure places_to_visit exists and is reasonable ──
    if not plan.get("places_to_visit") or len(plan.get("places_to_visit", [])) < 3:
        plan["places_to_visit"] = _get_places(destination)

    # ── Fix 4: Validate itinerary day count ──
    itinerary = plan.get("day_wise_itinerary", [])
    if len(itinerary) != days:
        # Regenerate itinerary with correct day count
        places = plan["places_to_visit"]
        new_itinerary = []
        for d in range(1, days + 1):
            if d == 1:
                new_itinerary.append({
                    "day": d,
                    "title": f"Travel to {destination}",
                    "activities": [
                        f"Depart from {user_location} via {plan['travel_mode']}",
                        f"Arrive at {destination}, {state}",
                        f"Check into {plan.get('hotel_name', 'hotel')}",
                        "Freshen up and evening leisure",
                    ],
                })
            elif d == days:
                new_itinerary.append({
                    "day": d,
                    "title": f"Return from {destination}",
                    "activities": [
                        "Breakfast and hotel checkout",
                        "Last-minute local sightseeing",
                        f"Depart via {plan['travel_mode']}",
                        "Arrive back at origin",
                    ],
                })
            else:
                pi = (d - 2) % len(places)
                new_itinerary.append({
                    "day": d,
                    "title": f"Explore {places[pi]}",
                    "activities": [
                        "Breakfast at hotel",
                        f"Visit {places[pi]}",
                        "Lunch at local restaurant",
                        f"Visit {places[(pi + 1) % len(places)]}",
                        "Evening leisure",
                        "Dinner",
                    ],
                })
        plan["day_wise_itinerary"] = new_itinerary
    else:
        # Fix Day 1 if it references origin instead of destination
        if itinerary and itinerary[0].get("title", ""):
            title = itinerary[0]["title"]
            # If Day 1 title contains origin location or says "Arrival in" origin
            if destination.lower() not in title.lower() or "arrival" in title.lower():
                itinerary[0]["title"] = f"Travel to {destination}"
                itinerary[0]["activities"] = [
                    f"Depart from {user_location} via {plan['travel_mode']}",
                    f"Arrive at {destination}, {state}",
                    f"Check into {plan.get('hotel_name', 'hotel')}",
                    "Freshen up and evening leisure",
                ]

        # Ensure day numbers are sequential and correct
        for idx, day in enumerate(itinerary):
            day["day"] = idx + 1

    return plan


def generate_trip_plans(user_location, destination, state, distance_km,
                        travelers, days, budget, trip_type):
    """
    Generate 3 AI-based trip plans using Ollama.
    Falls back to template plans if AI fails.
    All plans are post-processed for accuracy.
    Caches results in MongoDB.
    """
    db = get_db()

    # Check cache
    cache_key = _generate_cache_key(destination, state, travelers, days, budget, trip_type, distance_km)
    cached = db.ai_cache.find_one({"cache_key": cache_key})
    if cached:
        current_app.logger.info(f"AI cache hit for {destination}")
        return cached["response"], "cache"

    # Build prompt
    prompt = _build_prompt(
        user_location, destination, state, distance_km,
        travelers, days, budget, trip_type
    )

    # Call Ollama
    ollama_url = current_app.config["OLLAMA_BASE_URL"]
    model = current_app.config["OLLAMA_MODEL"]

    plans = None
    source = "ai"

    try:
        current_app.logger.info(f"Calling Ollama ({model}) for {destination} plans...")
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 4096,
                },
            },
            timeout=120,
        )
        response.raise_for_status()

        data = response.json()
        response_text = data.get("response", "")
        current_app.logger.info(f"Ollama response received ({len(response_text)} chars)")

        plans = _parse_ai_response(response_text)

        if not plans:
            current_app.logger.warning("Failed to parse AI response, using fallback")

    except requests.exceptions.ConnectionError:
        current_app.logger.warning("Ollama not available, using fallback plans")
    except requests.exceptions.Timeout:
        current_app.logger.warning("Ollama request timed out, using fallback plans")
    except Exception as e:
        current_app.logger.warning(f"Ollama error: {e}, using fallback plans")

    # Fallback to template-based plans
    if not plans:
        plans = _generate_fallback_plans(destination, state, distance_km, travelers, days, trip_type, user_location)
        source = "fallback"

    # ── POST-PROCESSING: Validate & fix ALL plans (AI or fallback) ──
    cost_variants = generate_cost_variants(distance_km, days, travelers)
    for i, plan in enumerate(plans):
        if i < len(cost_variants):
            plan = _validate_and_fix_plan(
                plan, cost_variants[i], destination, state, days, travelers, user_location
            )
            plan["cost_breakdown"] = cost_variants[i]
            if cost_variants[i].get("cab_info"):
                plan["cab_info"] = cost_variants[i]["cab_info"]

            # Add realistic travel time per mode
            mode_key = cost_variants[i].get("transport_mode_key", "bus")
            plan["travel_time"] = _estimate_travel_time(distance_km, mode_key)

            plans[i] = plan

    # Cache the result
    db.ai_cache.update_one(
        {"cache_key": cache_key},
        {
            "$set": {
                "cache_key": cache_key,
                "response": plans,
                "source": source,
                "created_at": datetime.now(timezone.utc),
            }
        },
        upsert=True,
    )

    return plans, source
