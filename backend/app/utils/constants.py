"""
Strictly defined destination data for India Smart Trip Planner.
Only these destinations are allowed — no additions permitted.
"""

DESTINATIONS = {
    "Andhra Pradesh": ["Tirupati", "Araku Valley", "Visakhapatnam"],
    "Arunachal Pradesh": ["Tawang Monastery", "Namdapha National Park"],
    "Assam": ["Kaziranga National Park", "Majuli Island"],
    "Bihar": ["Bodh Gaya", "Nalanda"],
    "Chhattisgarh": ["Chitrakote Falls", "Tirathgarh Waterfalls"],
    "Goa": ["Baga Beach", "Palolem Beach", "Basilica of Bom Jesus"],
    "Gujarat": ["Rann of Kutch", "Gir National Park", "Sabarmati Ashram"],
    "Haryana": ["Sultanpur National Park", "Surajkund Crafts Mela"],
    "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala"],
    "Jharkhand": ["Betla National Park", "Baidyanath Dham"],
    "Karnataka": ["Hampi", "Coorg", "Mysore Palace"],
    "Kerala": ["Munnar", "Alleppey", "Fort Kochi"],
    "Madhya Pradesh": ["Khajuraho Temples", "Mandu", "Kanha National Park"],
    "Maharashtra": ["Ajanta Ellora Caves", "Mumbai", "Lonavala"],
    "Manipur": ["Loktak Lake", "Imphal War Cemetery"],
    "Meghalaya": ["Shillong", "Cherrapunji", "Dawki"],
    "Mizoram": ["Aizawl", "Reiek Tlang"],
    "Nagaland": ["Kohima", "Dzukou Valley"],
    "Odisha": ["Puri Beach", "Konark Sun Temple", "Chilika Lake"],
    "Punjab": ["Golden Temple", "Wagah Border"],
    "Rajasthan": ["Jaipur", "Udaipur", "Jaisalmer"],
    "Sikkim": ["Gangtok", "Nathu La Pass", "Tsomgo Lake"],
    "Tamil Nadu": ["Madurai", "Ooty", "Kanyakumari"],
    "Telangana": ["Charminar", "Golconda Fort"],
    "Tripura": ["Ujjayanta Palace", "Neermahal"],
    "Uttar Pradesh": ["Taj Mahal", "Varanasi", "Ayodhya"],
    "Uttarakhand": ["Rishikesh", "Nainital", "Mussoorie", "Auli"],
    "West Bengal": ["Kolkata", "Darjeeling", "Sundarbans"],
}

# Approximate coordinates for destinations (lat, lng) for distance calculation
DESTINATION_COORDS = {
    "Tirupati": (13.6288, 79.4192),
    "Araku Valley": (18.3273, 82.8756),
    "Visakhapatnam": (17.6868, 83.2185),
    "Tawang Monastery": (27.5860, 91.8594),
    "Namdapha National Park": (27.4833, 96.3833),
    "Kaziranga National Park": (26.5775, 93.1711),
    "Majuli Island": (26.9500, 94.1667),
    "Bodh Gaya": (24.6961, 84.9869),
    "Nalanda": (25.1357, 85.4461),
    "Chitrakote Falls": (19.2036, 81.7014),
    "Tirathgarh Waterfalls": (19.0136, 81.7528),
    "Baga Beach": (15.5550, 73.7514),
    "Palolem Beach": (15.0100, 74.0231),
    "Basilica of Bom Jesus": (15.5009, 73.9116),
    "Rann of Kutch": (23.7337, 69.8597),
    "Gir National Park": (21.1243, 70.7933),
    "Sabarmati Ashram": (23.0607, 72.5809),
    "Sultanpur National Park": (28.4689, 76.8897),
    "Surajkund Crafts Mela": (28.4744, 77.2690),
    "Shimla": (31.1048, 77.1734),
    "Manali": (32.2396, 77.1887),
    "Dharamshala": (32.2190, 76.3234),
    "Betla National Park": (23.8707, 84.0581),
    "Baidyanath Dham": (24.4920, 86.7000),
    "Hampi": (15.3350, 76.4600),
    "Coorg": (12.3375, 75.8069),
    "Mysore Palace": (12.3051, 76.6551),
    "Munnar": (10.0889, 77.0595),
    "Alleppey": (9.4981, 76.3388),
    "Fort Kochi": (9.9658, 76.2421),
    "Khajuraho Temples": (24.8318, 79.9199),
    "Mandu": (22.3694, 75.3920),
    "Kanha National Park": (22.3345, 80.6115),
    "Ajanta Ellora Caves": (20.5519, 75.7033),
    "Mumbai": (19.0760, 72.8777),
    "Lonavala": (18.7546, 73.4062),
    "Loktak Lake": (24.5500, 93.8000),
    "Imphal War Cemetery": (24.7951, 93.9360),
    "Shillong": (25.5788, 91.8933),
    "Cherrapunji": (25.2800, 91.7200),
    "Dawki": (25.1863, 92.0215),
    "Aizawl": (23.7271, 92.7176),
    "Reiek Tlang": (23.6833, 92.5833),
    "Kohima": (25.6751, 94.1086),
    "Dzukou Valley": (25.5500, 94.0800),
    "Puri Beach": (19.7983, 85.8315),
    "Konark Sun Temple": (19.8876, 86.0945),
    "Chilika Lake": (19.7260, 85.3199),
    "Golden Temple": (31.6200, 74.8765),
    "Wagah Border": (31.6047, 74.5731),
    "Jaipur": (26.9124, 75.7873),
    "Udaipur": (24.5854, 73.7125),
    "Jaisalmer": (26.9157, 70.9083),
    "Gangtok": (27.3389, 88.6065),
    "Nathu La Pass": (27.3870, 88.8300),
    "Tsomgo Lake": (27.3753, 88.7653),
    "Madurai": (9.9252, 78.1198),
    "Ooty": (11.4102, 76.6950),
    "Kanyakumari": (8.0883, 77.5385),
    "Charminar": (17.3616, 78.4747),
    "Golconda Fort": (17.3833, 78.4011),
    "Ujjayanta Palace": (23.8315, 91.2868),
    "Neermahal": (23.4417, 91.2500),
    "Taj Mahal": (27.1751, 78.0421),
    "Varanasi": (25.3176, 83.0064),
    "Ayodhya": (26.7922, 82.1998),
    "Rishikesh": (30.0869, 78.2676),
    "Nainital": (29.3803, 79.4636),
    "Mussoorie": (30.4598, 78.0644),
    "Auli": (30.5280, 79.5671),
    "Kolkata": (22.5726, 88.3639),
    "Darjeeling": (27.0360, 88.2627),
    "Sundarbans": (21.9497, 88.8990),
}

# Trip types
TRIP_TYPES = ["Budget", "Family", "Adventure", "Luxury"]

# Transport cost rates (INR)
TRANSPORT_RATES = {
    "bus": {"cost_per_km": 2.0, "label": "Bus"},
    "cab": {"cost_per_km": 12.0, "label": "Cab"},
    "train": {"cost_per_km": 1.5, "label": "Train (Sleeper)"},
    "train_ac": {"cost_per_km": 2.5, "label": "Train (AC)"},
    "flight": {"base_cost": 4500, "label": "Flight"},
}

# Hotel cost ranges per night (INR) by trip type
HOTEL_RATES = {
    "Budget": {"min": 500, "max": 1500, "avg": 800},
    "Family": {"min": 1500, "max": 4000, "avg": 2500},
    "Adventure": {"min": 1000, "max": 3000, "avg": 1800},
    "Luxury": {"min": 5000, "max": 25000, "avg": 10000},
}

# Food cost per person per day (INR) by trip type
FOOD_RATES = {
    "Budget": 400,
    "Family": 800,
    "Adventure": 600,
    "Luxury": 2000,
}

# Local transport per day (INR)
LOCAL_TRANSPORT_RATES = {
    "Budget": 300,
    "Family": 800,
    "Adventure": 500,
    "Luxury": 2500,
}

# Activity/entry fee per place per person (INR)
ACTIVITY_COST_PER_PLACE = {
    "Budget": 150,
    "Family": 300,
    "Adventure": 400,
    "Luxury": 800,
}


def get_all_states():
    """Return list of all states."""
    return sorted(DESTINATIONS.keys())


def get_destinations_for_state(state):
    """Return destinations for a given state, or None if invalid."""
    return DESTINATIONS.get(state)


def is_valid_destination(state, destination):
    """Check if a destination belongs to the given state."""
    places = DESTINATIONS.get(state, [])
    return destination in places


def get_destination_coords(destination):
    """Return (lat, lng) for a destination, or None if not found."""
    return DESTINATION_COORDS.get(destination)
