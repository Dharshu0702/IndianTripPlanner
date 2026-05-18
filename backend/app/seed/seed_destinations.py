"""Seed script to populate the destinations collection in MongoDB."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from app import create_app, get_db
from app.utils.constants import DESTINATIONS, DESTINATION_COORDS

# Default destination metadata
DEFAULT_DATA = {
    "Tirupati": {"description": "Tirupati is a famous pilgrimage city in Andhra Pradesh, home to the Sri Venkateswara Temple on Tirumala Hills.", "best_time": "Sep-Mar", "avg_hotel": 1500},
    "Araku Valley": {"description": "Araku Valley is a hill station in Visakhapatnam district known for its coffee plantations and tribal culture.", "best_time": "Oct-Mar", "avg_hotel": 1200},
    "Visakhapatnam": {"description": "Vizag is a port city with beautiful beaches, submarine museum, and Kailasagiri hill park.", "best_time": "Oct-Mar", "avg_hotel": 2000},
    "Tawang Monastery": {"description": "Tawang Monastery is the largest monastery in India, situated at 10,000 ft in Arunachal Pradesh.", "best_time": "Mar-Jun, Sep-Oct", "avg_hotel": 1500},
    "Kaziranga National Park": {"description": "Kaziranga is a UNESCO World Heritage Site famous for the Indian one-horned rhinoceros.", "best_time": "Nov-Apr", "avg_hotel": 2500},
    "Bodh Gaya": {"description": "Bodh Gaya is where Gautama Buddha attained enlightenment under the Bodhi Tree.", "best_time": "Oct-Mar", "avg_hotel": 1000},
    "Baga Beach": {"description": "Baga Beach in North Goa is famous for nightlife, water sports, and beachside shacks.", "best_time": "Nov-Feb", "avg_hotel": 2500},
    "Rann of Kutch": {"description": "The Great Rann of Kutch is a vast salt marsh known for the Rann Utsav festival.", "best_time": "Nov-Feb", "avg_hotel": 3000},
    "Shimla": {"description": "Shimla is the capital of Himachal Pradesh, a popular hill station with colonial architecture.", "best_time": "Mar-Jun, Dec-Jan", "avg_hotel": 2000},
    "Manali": {"description": "Manali is an adventure hub with snow-capped peaks, temples, and trekking routes.", "best_time": "Oct-Jun", "avg_hotel": 2000},
    "Hampi": {"description": "Hampi is a UNESCO World Heritage Site with ruins of the Vijayanagara Empire.", "best_time": "Oct-Mar", "avg_hotel": 1500},
    "Munnar": {"description": "Munnar is a hill station in Kerala famous for tea plantations and misty mountains.", "best_time": "Sep-May", "avg_hotel": 2500},
    "Alleppey": {"description": "Alleppey (Alappuzha) is known as the Venice of the East for its houseboat cruises on backwaters.", "best_time": "Sep-Mar", "avg_hotel": 3000},
    "Jaipur": {"description": "Jaipur, the Pink City, is Rajasthan's capital known for Amber Fort, Hawa Mahal, and palaces.", "best_time": "Oct-Mar", "avg_hotel": 2500},
    "Udaipur": {"description": "Udaipur, the City of Lakes, features stunning palaces, temples, and Pichola Lake.", "best_time": "Sep-Mar", "avg_hotel": 3000},
    "Taj Mahal": {"description": "The Taj Mahal in Agra is a UNESCO World Heritage Site and one of the Seven Wonders of the World.", "best_time": "Oct-Mar", "avg_hotel": 2000},
    "Varanasi": {"description": "Varanasi is one of the oldest cities in the world, sacred for Hindu pilgrimage along the Ganges.", "best_time": "Oct-Mar", "avg_hotel": 1500},
    "Rishikesh": {"description": "Rishikesh is the Yoga Capital of the World, known for adventure sports and ashrams.", "best_time": "Sep-Jun", "avg_hotel": 1500},
    "Darjeeling": {"description": "Darjeeling is famous for tea gardens, the toy train, and views of Kanchenjunga.", "best_time": "Mar-May, Oct-Nov", "avg_hotel": 2000},
    "Kolkata": {"description": "Kolkata is the cultural capital of India, known for Howrah Bridge, Victoria Memorial, and cuisine.", "best_time": "Oct-Mar", "avg_hotel": 2500},
    "Golden Temple": {"description": "The Golden Temple (Harmandir Sahib) in Amritsar is the holiest Sikh shrine.", "best_time": "Oct-Mar", "avg_hotel": 1500},
    "Ooty": {"description": "Ooty (Udhagamandalam) is a popular hill station in Tamil Nadu with botanical gardens and lakes.", "best_time": "Oct-Jun", "avg_hotel": 2000},
    "Gangtok": {"description": "Gangtok, the capital of Sikkim, offers views of Kanchenjunga and Buddhist monasteries.", "best_time": "Mar-Jun, Sep-Dec", "avg_hotel": 2000},
    "Shillong": {"description": "Shillong, the Scotland of the East, is known for waterfalls, living root bridges, and music.", "best_time": "Sep-May", "avg_hotel": 1800},
    "Charminar": {"description": "Charminar is an iconic monument in Hyderabad, surrounded by bustling bazaars.", "best_time": "Oct-Mar", "avg_hotel": 2000},
    "Puri Beach": {"description": "Puri is famous for the Jagannath Temple and its beautiful golden beach.", "best_time": "Oct-Mar", "avg_hotel": 1500},
}


def seed_destinations():
    """Seed the destinations collection with initial data."""
    app = create_app()
    with app.app_context():
        db = get_db()
        count = 0

        for state, places in DESTINATIONS.items():
            for place in places:
                defaults = DEFAULT_DATA.get(place, {})
                coords = DESTINATION_COORDS.get(place, (0, 0))

                doc = {
                    "state": state,
                    "name": place,
                    "description": defaults.get("description", f"{place} is a popular tourist destination in {state}, India."),
                    "attractions": [],
                    "avg_hotel_price": defaults.get("avg_hotel", 1500),
                    "best_time_to_visit": defaults.get("best_time", "Oct-Mar"),
                    "lat": coords[0],
                    "lng": coords[1],
                }

                db.destinations.update_one(
                    {"state": state, "name": place},
                    {"$setOnInsert": doc},
                    upsert=True,
                )
                count += 1

        print(f"Seeded {count} destinations across {len(DESTINATIONS)} states.")


if __name__ == "__main__":
    seed_destinations()
