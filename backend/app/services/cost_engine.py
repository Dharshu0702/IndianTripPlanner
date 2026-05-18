"""Travel cost calculation engine. All costs in INR (₹)."""

from app.utils.constants import (
    TRANSPORT_RATES,
    HOTEL_RATES,
    FOOD_RATES,
    LOCAL_TRANSPORT_RATES,
    ACTIVITY_COST_PER_PLACE,
)


def suggest_transport(distance_km, trip_type="Budget"):
    """
    Suggest transport mode based on distance.
    <300 km → Bus/Cab
    300-800 km → Train
    >800 km → Flight
    """
    if distance_km < 300:
        if trip_type == "Luxury":
            mode = "cab"
        elif trip_type == "Budget":
            mode = "bus"
        else:
            mode = "cab"
    elif distance_km <= 800:
        if trip_type == "Luxury":
            mode = "train_ac"
        else:
            mode = "train"
    else:
        mode = "flight"

    return mode


def calculate_travel_cost(distance_km, mode, travelers):
    """Calculate one-way travel cost for all travelers."""
    rate = TRANSPORT_RATES.get(mode, TRANSPORT_RATES["bus"])

    if mode == "flight":
        base = rate["base_cost"]
        # Rough flight cost scaling: base + distance factor
        cost_per_person = base + (distance_km * 0.5)
        total = cost_per_person * travelers
    else:
        cost_per_km = rate["cost_per_km"]
        if mode in ("bus", "train", "train_ac"):
            # Per person cost
            total = cost_per_km * distance_km * travelers
        else:
            # Cab: shared cost, need multiple cabs if >4 travelers
            num_cabs = max(1, -(-travelers // 4))  # ceiling division
            total = cost_per_km * distance_km * num_cabs

    return round(total, 2)


def calculate_hotel_cost(days, travelers, trip_type):
    """Calculate total hotel cost."""
    rate = HOTEL_RATES.get(trip_type, HOTEL_RATES["Budget"])
    rooms = max(1, -(-travelers // 2))  # ceiling division, 2 per room
    cost_per_night = rate["avg"]
    total = cost_per_night * rooms * days
    return round(total, 2), cost_per_night, rooms


def calculate_food_cost(days, travelers, trip_type):
    """Calculate total food cost."""
    daily_per_person = FOOD_RATES.get(trip_type, FOOD_RATES["Budget"])
    total = daily_per_person * travelers * days
    return round(total, 2), daily_per_person


def calculate_local_transport(days, travelers, trip_type):
    """Calculate local transport cost."""
    daily = LOCAL_TRANSPORT_RATES.get(trip_type, LOCAL_TRANSPORT_RATES["Budget"])
    # Local transport is typically shared (cab/auto)
    num_vehicles = max(1, -(-travelers // 4))
    total = daily * num_vehicles * days
    return round(total, 2), daily


def calculate_activity_cost(num_places, travelers, trip_type):
    """Calculate total activity/entry fees for all places."""
    per_place_per_person = ACTIVITY_COST_PER_PLACE.get(trip_type, ACTIVITY_COST_PER_PLACE["Budget"])
    total = per_place_per_person * num_places * travelers
    return round(total, 2), per_place_per_person


def calculate_total_cost(distance_km, days, travelers, trip_type, transport_mode=None, num_places=0):
    """
    Calculate complete trip cost breakdown.
    Returns a dict with all cost components.
    """
    if not transport_mode:
        transport_mode = suggest_transport(distance_km, trip_type)

    # Travel cost (round trip)
    one_way = calculate_travel_cost(distance_km, transport_mode, travelers)
    travel_cost = round(one_way * 2, 2)

    # Hotel
    hotel_total, hotel_per_night, rooms = calculate_hotel_cost(days, travelers, trip_type)

    # Food
    food_total, food_per_person_day = calculate_food_cost(days, travelers, trip_type)

    # Local transport
    local_total, local_per_day = calculate_local_transport(days, travelers, trip_type)

    # Activity/entry fees
    activity_total, activity_per_place = calculate_activity_cost(num_places, travelers, trip_type)

    # Grand total
    total = round(travel_cost + hotel_total + food_total + local_total + activity_total, 2)

    # Cab info for >4 travelers
    cab_info = None
    if travelers > 4 and transport_mode == "cab":
        num_cabs = max(1, -(-travelers // 4))
        cab_info = {
            "num_cabs": num_cabs,
            "travelers_per_cab": min(4, travelers),
            "note": f"Recommending {num_cabs} cabs for {travelers} travelers (max 4 per cab)",
        }

    return {
        "transport_mode": TRANSPORT_RATES[transport_mode]["label"],
        "transport_mode_key": transport_mode,
        "distance_km": distance_km,
        "travel_cost": travel_cost,
        "travel_cost_one_way": one_way,
        "hotel_cost_per_night": hotel_per_night,
        "hotel_rooms": rooms,
        "hotel_total": hotel_total,
        "food_per_person_per_day": food_per_person_day,
        "food_total": food_total,
        "local_transport_per_day": local_per_day,
        "local_transport_total": local_total,
        "activity_cost_per_place": activity_per_place,
        "activity_total": activity_total,
        "num_places": num_places,
        "total_cost": total,
        "currency": "INR",
        "cab_info": cab_info,
    }


def generate_cost_variants(distance_km, days, travelers, num_places=0):
    """Generate cost breakdowns for Budget, Balanced, and Luxury plans."""
    budget_mode = suggest_transport(distance_km, "Budget")
    balanced_mode = suggest_transport(distance_km, "Family")
    luxury_mode = suggest_transport(distance_km, "Luxury")

    # For luxury over 300km, consider flight even if distance <800
    if distance_km > 300 and luxury_mode != "flight":
        luxury_mode = "flight" if distance_km > 500 else "train_ac"

    budget = calculate_total_cost(distance_km, days, travelers, "Budget", budget_mode, num_places)
    budget["plan_name"] = "Budget Plan"

    balanced = calculate_total_cost(distance_km, days, travelers, "Family", balanced_mode, num_places)
    balanced["plan_name"] = "Balanced Plan"

    luxury = calculate_total_cost(distance_km, days, travelers, "Luxury", luxury_mode, num_places)
    luxury["plan_name"] = "Luxury Plan"

    return [budget, balanced, luxury]
