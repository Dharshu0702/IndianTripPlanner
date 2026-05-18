"""Curated hotel data for Indian destinations."""

_B = "Budget"
_M = "Balanced"
_L = "Luxury"

def _h(id, name, loc, price, rating, img_id, website):
    return {
        "id": id, "name": name, "location": loc,
        "price_per_night": price, "rating": rating,
        "image": f"https://images.unsplash.com/photo-{img_id}?w=400&q=80",
        "website": website,
    }

HOTELS = {
    "Baga Beach": {
        "Budget": [
            {"id": "bg-b1", "name": "Zostel Goa", "location": "Baga, North Goa", "price_per_night": 800, "rating": 4.2, "image": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&q=80", "website": "https://www.zostel.com/zostel/goa/"},
            {"id": "bg-b2", "name": "FabHotel Calangute", "location": "Calangute, Goa", "price_per_night": 1200, "rating": 3.8, "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&q=80", "website": "https://www.fabhotels.com"},
            {"id": "bg-b3", "name": "OYO Rooms Baga", "location": "Baga Beach Road, Goa", "price_per_night": 950, "rating": 3.6, "image": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400&q=80", "website": "https://www.oyorooms.com"},
        ],
        "Balanced": [
            {"id": "bg-m1", "name": "Lemon Tree Amarante Beach", "location": "Candolim, Goa", "price_per_night": 3500, "rating": 4.3, "image": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&q=80", "website": "https://www.lemontreehotels.com"},
            {"id": "bg-m2", "name": "Country Club Goa", "location": "Anjuna, Goa", "price_per_night": 2800, "rating": 4.1, "image": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400&q=80", "website": "https://www.countryclubindia.net"},
            {"id": "bg-m3", "name": "Acron Waterfront Resort", "location": "Baga River, Goa", "price_per_night": 4200, "rating": 4.4, "image": "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400&q=80", "website": "https://www.acronresort.com"},
        ],
        "Luxury": [
            {"id": "bg-l1", "name": "The Leela Goa", "location": "Mobor, Cavelossim, Goa", "price_per_night": 18000, "rating": 4.8, "image": "https://images.unsplash.com/photo-1551882547-ff40c63fe2f5?w=400&q=80", "website": "https://www.theleela.com/goa"},
            {"id": "bg-l2", "name": "Taj Fort Aguada Resort", "location": "Fort Aguada Road, Goa", "price_per_night": 22000, "rating": 4.9, "image": "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=400&q=80", "website": "https://www.tajhotels.com/goa"},
            {"id": "bg-l3", "name": "W Goa", "location": "Vagator Beach, Goa", "price_per_night": 25000, "rating": 4.7, "image": "https://images.unsplash.com/photo-1540541338537-41b8f72dfbb3?w=400&q=80", "website": "https://www.marriott.com/w-goa"},
        ],
    },
    "Shimla": {
        "Budget": [
            {"id": "sh-b1", "name": "Zostel Shimla", "location": "Mall Road, Shimla", "price_per_night": 700, "rating": 4.3, "image": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=400&q=80", "website": "https://www.zostel.com/zostel/shimla/"},
            {"id": "sh-b2", "name": "Hotel White", "location": "The Ridge, Shimla", "price_per_night": 1100, "rating": 3.7, "image": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&q=80", "website": "https://www.hotelwhiteshimla.com"},
            {"id": "sh-b3", "name": "Hotel Dreamland", "location": "Cart Road, Shimla", "price_per_night": 900, "rating": 3.5, "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&q=80", "website": "https://www.hoteldreamlandshimla.com"},
        ],
        "Balanced": [
            {"id": "sh-m1", "name": "Clarkes Hotel", "location": "The Mall, Shimla", "price_per_night": 3200, "rating": 4.2, "image": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400&q=80", "website": "https://www.clarkeshotel.com"},
            {"id": "sh-m2", "name": "Hotel Combermere", "location": "Mall Road, Shimla", "price_per_night": 2800, "rating": 4.0, "image": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&q=80", "website": "https://www.hotelcombermere.com"},
            {"id": "sh-m3", "name": "Honeymoon Inn Shimla", "location": "Chaura Maidan, Shimla", "price_per_night": 3500, "rating": 4.1, "image": "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400&q=80", "website": "https://www.honeymooninnshimla.com"},
        ],
        "Luxury": [
            {"id": "sh-l1", "name": "Wildflower Hall", "location": "Mashobra, Shimla", "price_per_night": 22000, "rating": 4.9, "image": "https://images.unsplash.com/photo-1551882547-ff40c63fe2f5?w=400&q=80", "website": "https://www.oberoihotels.com/wildflower-hall"},
            {"id": "sh-l2", "name": "The Cecil Hotel", "location": "Chaura Maidan, Shimla", "price_per_night": 12000, "rating": 4.7, "image": "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=400&q=80", "website": "https://www.oberoihotels.com/the-cecil"},
            {"id": "sh-l3", "name": "Chapslee Estate", "location": "Lakkar Bazaar, Shimla", "price_per_night": 15000, "rating": 4.8, "image": "https://images.unsplash.com/photo-1540541338537-41b8f72dfbb3?w=400&q=80", "website": "https://www.chapslee.com"},
        ],
    },
    "Manali": {
        "Budget": [
            {"id": "mn-b1", "name": "Zostel Manali", "location": "Old Manali Road", "price_per_night": 750, "rating": 4.4, "image": "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=400&q=80", "website": "https://www.zostel.com/zostel/manali/"},
            {"id": "mn-b2", "name": "Hotel Snow View", "location": "The Mall, Manali", "price_per_night": 1000, "rating": 3.8, "image": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400&q=80", "website": "https://www.hotelsnowviewmanali.com"},
            {"id": "mn-b3", "name": "Backpacker Panda Manali", "location": "Old Manali", "price_per_night": 650, "rating": 4.1, "image": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&q=80", "website": "https://www.backpackerpanda.com"},
        ],
        "Balanced": [
            {"id": "mn-m1", "name": "Span Resort & Spa", "location": "Kullu-Manali Highway", "price_per_night": 5500, "rating": 4.5, "image": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400&q=80", "website": "https://www.spanresort.com"},
            {"id": "mn-m2", "name": "Snow Valley Resorts", "location": "Hadimba Road, Manali", "price_per_night": 3800, "rating": 4.2, "image": "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400&q=80", "website": "https://www.snowvalleyresorts.com"},
            {"id": "mn-m3", "name": "Hotel Rohtang View", "location": "Circuit House Road, Manali", "price_per_night": 3200, "rating": 4.0, "image": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&q=80", "website": "https://www.hotelrohtangview.com"},
        ],
        "Luxury": [
            {"id": "mn-l1", "name": "Solang Valley Resort", "location": "Solang Valley, Manali", "price_per_night": 12000, "rating": 4.7, "image": "https://images.unsplash.com/photo-1551882547-ff40c63fe2f5?w=400&q=80", "website": "https://www.solangvalleyresorts.com"},
            {"id": "mn-l2", "name": "The Himalayan Hotel", "location": "Log Huts Area, Manali", "price_per_night": 9500, "rating": 4.6, "image": "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=400&q=80", "website": "https://www.thehimalayanhotel.com"},
            {"id": "mn-l3", "name": "Manuallaya Resort", "location": "Duff Dunbar, Manali", "price_per_night": 15000, "rating": 4.8, "image": "https://images.unsplash.com/photo-1540541338537-41b8f72dfbb3?w=400&q=80", "website": "https://www.manuallaya.com"},
        ],
    },
    "Jaipur": {
        "Budget": [
            {"id": "jp-b1", "name": "Zostel Jaipur", "location": "Johari Bazaar, Jaipur", "price_per_night": 700, "rating": 4.3, "image": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&q=80", "website": "https://www.zostel.com/zostel/jaipur/"},
            {"id": "jp-b2", "name": "Hotel Pearl Palace", "location": "Hathroi Fort, Jaipur", "price_per_night": 1500, "rating": 4.5, "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&q=80", "website": "https://www.hotelpearlpalace.com"},
            {"id": "jp-b3", "name": "Moustache Hostel Jaipur", "location": "MI Road, Jaipur", "price_per_night": 800, "rating": 4.2, "image": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400&q=80", "website": "https://www.moustachehostel.com"},
        ],
        "Balanced": [
            {"id": "jp-m1", "name": "Sarovar Portico Jaipur", "location": "Civil Lines, Jaipur", "price_per_night": 2800, "rating": 4.2, "image": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400&q=80", "website": "https://www.sarovarhotels.com"},
            {"id": "jp-m2", "name": "Lemon Tree Premier Jaipur", "location": "Tonk Road, Jaipur", "price_per_night": 3200, "rating": 4.3, "image": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&q=80", "website": "https://www.lemontreehotels.com"},
            {"id": "jp-m3", "name": "Clarks Amer Jaipur", "location": "Jawaharlal Nehru Marg, Jaipur", "price_per_night": 3800, "rating": 4.1, "image": "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400&q=80", "website": "https://www.clarkshotels.com"},
        ],
        "Luxury": [
            {"id": "jp-l1", "name": "Rambagh Palace", "location": "Bhawani Singh Road, Jaipur", "price_per_night": 35000, "rating": 4.9, "image": "https://images.unsplash.com/photo-1609944213536-80ee16b0c8d5?w=400&q=80", "website": "https://www.tajhotels.com/rambagh-palace"},
            {"id": "jp-l2", "name": "ITC Rajputana", "location": "Palace Road, Jaipur", "price_per_night": 12000, "rating": 4.7, "image": "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=400&q=80", "website": "https://www.itchotels.com"},
            {"id": "jp-l3", "name": "Trident Jaipur", "location": "Amber Fort Road, Jaipur", "price_per_night": 10000, "rating": 4.6, "image": "https://images.unsplash.com/photo-1540541338537-41b8f72dfbb3?w=400&q=80", "website": "https://www.tridenthotels.com"},
        ],
    },
    "Munnar": {
        "Budget": [
            {"id": "mu-b1", "name": "Zostel Munnar", "location": "Town Centre, Munnar", "price_per_night": 800, "rating": 4.3, "image": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&q=80", "website": "https://www.zostel.com/zostel/munnar/"},
            {"id": "mu-b2", "name": "Tea Nest Munnar", "location": "Munnar Town", "price_per_night": 1200, "rating": 3.9, "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&q=80", "website": "https://www.teanestmunnar.com"},
            {"id": "mu-b3", "name": "Green View Munnar", "location": "Lockhart Gap, Munnar", "price_per_night": 950, "rating": 3.7, "image": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400&q=80", "website": "https://www.greenviewmunnar.com"},
        ],
        "Balanced": [
            {"id": "mu-m1", "name": "Windermere Estate", "location": "Pothamedu, Munnar", "price_per_night": 3500, "rating": 4.5, "image": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400&q=80", "website": "https://www.windermere-munnar.com"},
            {"id": "mu-m2", "name": "Chandy's Windy Woods", "location": "Devikulam, Munnar", "price_per_night": 2800, "rating": 4.2, "image": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&q=80", "website": "https://www.chandyswindywoods.com"},
            {"id": "mu-m3", "name": "Tall Trees Munnar", "location": "Bison Valley Road, Munnar", "price_per_night": 4200, "rating": 4.4, "image": "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400&q=80", "website": "https://www.talltreesmunnar.com"},
        ],
        "Luxury": [
            {"id": "mu-l1", "name": "The Spice Tree", "location": "Yellapatty, Munnar", "price_per_night": 12000, "rating": 4.8, "image": "https://images.unsplash.com/photo-1551882547-ff40c63fe2f5?w=400&q=80", "website": "https://www.thespicetree.com"},
            {"id": "mu-l2", "name": "Fragrant Nature Munnar", "location": "Bison Valley, Munnar", "price_per_night": 8500, "rating": 4.6, "image": "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=400&q=80", "website": "https://www.fragrantnature.com"},
            {"id": "mu-l3", "name": "Soft India Boutique Resort", "location": "Devikulam, Munnar", "price_per_night": 10000, "rating": 4.7, "image": "https://images.unsplash.com/photo-1540541338537-41b8f72dfbb3?w=400&q=80", "website": "https://www.softindia.com"},
        ],
    },
    "Udaipur": {
        "Budget": [
            {"id": "ud-b1", "name": "Zostel Udaipur", "location": "Lal Ghat, Udaipur", "price_per_night": 750, "rating": 4.4, "image": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&q=80", "website": "https://www.zostel.com/zostel/udaipur/"},
            {"id": "ud-b2", "name": "Nukkad Hostel Udaipur", "location": "Gangaur Ghat, Udaipur", "price_per_night": 900, "rating": 4.2, "image": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400&q=80", "website": "https://www.nukkad.com"},
            {"id": "ud-b3", "name": "Hotel Pratap Bhawan", "location": "Lake Pichola, Udaipur", "price_per_night": 1400, "rating": 3.8, "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&q=80", "website": "https://www.hotelpratapbhawan.com"},
        ],
        "Balanced": [
            {"id": "ud-m1", "name": "Raas Leela Udaipur", "location": "City Palace Road, Udaipur", "price_per_night": 5500, "rating": 4.5, "image": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400&q=80", "website": "https://www.raasleela.com"},
            {"id": "ud-m2", "name": "Hotel Mahendra Prakash", "location": "Chetak Circle, Udaipur", "price_per_night": 3200, "rating": 4.1, "image": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&q=80", "website": "https://www.hotelmahendraprakash.com"},
            {"id": "ud-m3", "name": "Amet Haveli", "location": "Hanuman Ghat, Udaipur", "price_per_night": 4500, "rating": 4.3, "image": "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400&q=80", "website": "https://www.amethaveli.com"},
        ],
        "Luxury": [
            {"id": "ud-l1", "name": "Taj Lake Palace", "location": "Lake Pichola, Udaipur", "price_per_night": 45000, "rating": 5.0, "image": "https://images.unsplash.com/photo-1609944213536-80ee16b0c8d5?w=400&q=80", "website": "https://www.tajhotels.com/lake-palace"},
            {"id": "ud-l2", "name": "The Oberoi Udaivilas", "location": "Haridasji Ki Magri, Udaipur", "price_per_night": 55000, "rating": 4.9, "image": "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=400&q=80", "website": "https://www.oberoihotels.com/udaivilas"},
            {"id": "ud-l3", "name": "Fateh Garh Heritage Resort", "location": "Fatehsagar Lake, Udaipur", "price_per_night": 18000, "rating": 4.7, "image": "https://images.unsplash.com/photo-1540541338537-41b8f72dfbb3?w=400&q=80", "website": "https://www.fatehgarh.in"},
        ],
    },
}

# ── Additional destinations ──
HOTELS["Alleppey"] = HOTELS["Alleppey Backwaters"] = {
    "Budget": [
        {"id":"al-b1","name":"Zostel Alleppey","location":"Beach Road, Alleppey","price_per_night":850,"rating":4.3,"image":"https://images.unsplash.com/photo-1571985755959-3f2ff7b5e1bc?w=400&q=80","website":"https://www.zostel.com/zostel/alleppey/"},
        {"id":"al-b2","name":"Tharavadu Heritage Home","location":"Ward 10, Alleppey","price_per_night":1200,"rating":4.0,"image":"https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&q=80","website":"https://www.tharavaduheritage.com"},
        {"id":"al-b3","name":"FabHotel Alleppey","location":"Mullakkal, Alleppey","price_per_night":1000,"rating":3.8,"image":"https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&q=80","website":"https://www.fabhotels.com"},
    ],
    "Balanced": [
        {"id":"al-m1","name":"Pagoda Resort","location":"Beach Road, Alleppey","price_per_night":3200,"rating":4.3,"image":"https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400&q=80","website":"https://www.pagondaresort.com"},
        {"id":"al-m2","name":"Raheem Residency","location":"Beach Road, Alleppey","price_per_night":4500,"rating":4.5,"image":"https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&q=80","website":"https://www.raheemresidency.com"},
        {"id":"al-m3","name":"Kerala Bamboo House","location":"Punnamada Lake, Alleppey","price_per_night":2800,"rating":4.2,"image":"https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400&q=80","website":"https://www.keralabamboohouse.com"},
    ],
    "Luxury": [
        {"id":"al-l1","name":"Marari Beach Resort (CGH)","location":"Mararikulam, Alleppey","price_per_night":14000,"rating":4.8,"image":"https://images.unsplash.com/photo-1551882547-ff40c63fe2f5?w=400&q=80","website":"https://www.cghearth.com/marari-beach"},
        {"id":"al-l2","name":"Coconut Lagoon CGH Earth","location":"Kumarakom, Alleppey","price_per_night":18000,"rating":4.9,"image":"https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=400&q=80","website":"https://www.cghearth.com/coconut-lagoon"},
        {"id":"al-l3","name":"Xandari Riverscapes","location":"Alappuzha Backwaters","price_per_night":12000,"rating":4.7,"image":"https://images.unsplash.com/photo-1540541338537-41b8f72dfbb3?w=400&q=80","website":"https://www.xandari.com"},
    ],
}

HOTELS["Fort Kochi"] = {
    "Budget": [
        {"id":"fk-b1","name":"Zostel Fort Kochi","location":"Fort Kochi, Kerala","price_per_night":750,"rating":4.4,"image":"https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&q=80","website":"https://www.zostel.com/zostel/fort-kochi/"},
        {"id":"fk-b2","name":"Old Harbour Hostel","location":"Tower Road, Fort Kochi","price_per_night":900,"rating":4.1,"image":"https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400&q=80","website":"https://www.oldharbourhostel.com"},
        {"id":"fk-b3","name":"Casa Linda Fort Kochi","location":"Princess Street, Kochi","price_per_night":1100,"rating":3.9,"image":"https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&q=80","website":"https://www.casalindakochi.com"},
    ],
    "Balanced": [
        {"id":"fk-m1","name":"Old Harbour Hotel","location":"Tower Road, Fort Kochi","price_per_night":5000,"rating":4.5,"image":"https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400&q=80","website":"https://www.oldharbourhotel.com"},
        {"id":"fk-m2","name":"Brunton Boatyard","location":"Calvathy Road, Kochi","price_per_night":8500,"rating":4.6,"image":"https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&q=80","website":"https://www.cghearth.com/brunton-boatyard"},
        {"id":"fk-m3","name":"Fort House Hotel","location":"2/6A Calvathy Road, Kochi","price_per_night":3500,"rating":4.2,"image":"https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400&q=80","website":"https://www.forthousehotel.com"},
    ],
    "Luxury": [
        {"id":"fk-l1","name":"Taj Malabar Resort","location":"Willingdon Island, Kochi","price_per_night":15000,"rating":4.8,"image":"https://images.unsplash.com/photo-1551882547-ff40c63fe2f5?w=400&q=80","website":"https://www.tajhotels.com/kochi"},
        {"id":"fk-l2","name":"Le Meridien Kochi","location":"Maradu, Kochi","price_per_night":10000,"rating":4.6,"image":"https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=400&q=80","website":"https://www.marriott.com/le-meridien-kochi"},
        {"id":"fk-l3","name":"Casino Hotel CGH Earth","location":"Willingdon Island, Kochi","price_per_night":12000,"rating":4.7,"image":"https://images.unsplash.com/photo-1540541338537-41b8f72dfbb3?w=400&q=80","website":"https://www.cghearth.com/casino-hotel"},
    ],
}

HOTELS["Varanasi"] = {
    "Budget": [
        {"id":"vr-b1","name":"Zostel Varanasi","location":"Assi Ghat, Varanasi","price_per_night":700,"rating":4.3,"image":"https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&q=80","website":"https://www.zostel.com/zostel/varanasi/"},
        {"id":"vr-b2","name":"Hotel Alka","location":"Meer Ghat, Varanasi","price_per_night":1200,"rating":4.0,"image":"https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&q=80","website":"https://www.hotelalka.com"},
        {"id":"vr-b3","name":"Ganges View Hotel","location":"Assi Ghat, Varanasi","price_per_night":1500,"rating":4.2,"image":"https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400&q=80","website":"https://www.gangesview.com"},
    ],
    "Balanced": [
        {"id":"vr-m1","name":"BrijRama Palace","location":"Darbhanga Ghat, Varanasi","price_per_night":6000,"rating":4.6,"image":"https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400&q=80","website":"https://www.brijrama.com"},
        {"id":"vr-m2","name":"Ramada Varanasi","location":"The Mall, Varanasi","price_per_night":3500,"rating":4.1,"image":"https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&q=80","website":"https://www.wyndhamhotels.com"},
        {"id":"vr-m3","name":"Hotel Surya","location":"S-20/51, Varanasi","price_per_night":2800,"rating":4.0,"image":"https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400&q=80","website":"https://www.hotelsurya.com"},
    ],
    "Luxury": [
        {"id":"vr-l1","name":"Taj Nadesar Palace","location":"Nadesar, Varanasi","price_per_night":22000,"rating":4.9,"image":"https://images.unsplash.com/photo-1609944213536-80ee16b0c8d5?w=400&q=80","website":"https://www.tajhotels.com/nadesar-palace"},
        {"id":"vr-l2","name":"Brijrama Palace Heritage","location":"Darbhanga Ghat","price_per_night":12000,"rating":4.7,"image":"https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=400&q=80","website":"https://www.brijrama.com"},
        {"id":"vr-l3","name":"Radisson Hotel Varanasi","location":"The Mall Road, Varanasi","price_per_night":8000,"rating":4.5,"image":"https://images.unsplash.com/photo-1540541338537-41b8f72dfbb3?w=400&q=80","website":"https://www.radissonhotels.com"},
    ],
}

HOTELS["Rishikesh"] = {
    "Budget": [
        {"id":"rk-b1","name":"Zostel Rishikesh","location":"Laxman Jhula, Rishikesh","price_per_night":700,"rating":4.5,"image":"https://images.unsplash.com/photo-1582719508461-905c673771fd?w=400&q=80","website":"https://www.zostel.com/zostel/rishikesh/"},
        {"id":"rk-b2","name":"Bunk Rishikesh","location":"Tapovan, Rishikesh","price_per_night":850,"rating":4.3,"image":"https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&q=80","website":"https://www.bunkrishikesh.com"},
        {"id":"rk-b3","name":"Hotel Natraj","location":"Haridwar Road, Rishikesh","price_per_night":1100,"rating":3.8,"image":"https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&q=80","website":"https://www.hotelnatrajrishikesh.com"},
    ],
    "Balanced": [
        {"id":"rk-m1","name":"Aloha on the Ganges","location":"Muni Ki Reti, Rishikesh","price_per_night":4500,"rating":4.4,"image":"https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400&q=80","website":"https://www.alohashivpuri.com"},
        {"id":"rk-m2","name":"Atali Ganga","location":"Byasi, Rishikesh","price_per_night":5500,"rating":4.5,"image":"https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&q=80","website":"https://www.ataliganga.com"},
        {"id":"rk-m3","name":"Ganga Kinare","location":"16 Virbhadra Marg, Rishikesh","price_per_night":3500,"rating":4.2,"image":"https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400&q=80","website":"https://www.gangakinare.com"},
    ],
    "Luxury": [
        {"id":"rk-l1","name":"Ananda in the Himalayas","location":"Narendra Nagar, Rishikesh","price_per_night":35000,"rating":5.0,"image":"https://images.unsplash.com/photo-1551882547-ff40c63fe2f5?w=400&q=80","website":"https://www.anandaspa.com"},
        {"id":"rk-l2","name":"Taj Rishikesh Resort","location":"Shivpuri, Rishikesh","price_per_night":28000,"rating":4.9,"image":"https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=400&q=80","website":"https://www.tajhotels.com/rishikesh"},
        {"id":"rk-l3","name":"Vana Malsi Estate","location":"Dehradun Road, Rishikesh","price_per_night":18000,"rating":4.8,"image":"https://images.unsplash.com/photo-1540541338537-41b8f72dfbb3?w=400&q=80","website":"https://www.vana.co.in"},
    ],
}

HOTELS["Ooty"] = {
    "Budget": [
        {"id":"oo-b1","name":"Zostel Ooty","location":"Charring Cross, Ooty","price_per_night":750,"rating":4.2,"image":"https://images.unsplash.com/photo-1582719508461-905c673771fd?w=400&q=80","website":"https://www.zostel.com"},
        {"id":"oo-b2","name":"Hotel Welbeck","location":"Ettines Road, Ooty","price_per_night":1100,"rating":3.9,"image":"https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&q=80","website":"https://www.hotelwelbeck.com"},
        {"id":"oo-b3","name":"YHA Youth Hostel Ooty","location":"Ettines Road, Ooty","price_per_night":650,"rating":3.7,"image":"https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&q=80","website":"https://www.yhaindia.org"},
    ],
    "Balanced": [
        {"id":"oo-m1","name":"Savoy Hotel Ooty","location":"Sylks Road, Ooty","price_per_night":4500,"rating":4.3,"image":"https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400&q=80","website":"https://www.tajhotels.com/savoy-ooty"},
        {"id":"oo-m2","name":"Fortune Hotel Sullivan Court","location":"Havelock Road, Ooty","price_per_night":3200,"rating":4.1,"image":"https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&q=80","website":"https://www.fortunehotels.in"},
        {"id":"oo-m3","name":"Lymond House","location":"Havelock Road, Ooty","price_per_night":5000,"rating":4.4,"image":"https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400&q=80","website":"https://www.lymondhouse.com"},
    ],
    "Luxury": [
        {"id":"oo-l1","name":"Taj Savoy Hotel","location":"Sylks Road, Ooty","price_per_night":12000,"rating":4.8,"image":"https://images.unsplash.com/photo-1551882547-ff40c63fe2f5?w=400&q=80","website":"https://www.tajhotels.com/savoy-ooty"},
        {"id":"oo-l2","name":"Fernhills Royal Palace","location":"Mysore Road, Ooty","price_per_night":18000,"rating":4.7,"image":"https://images.unsplash.com/photo-1609944213536-80ee16b0c8d5?w=400&q=80","website":"https://www.fernhillspalace.com"},
        {"id":"oo-l3","name":"Sterling Elk Hill","location":"Elk Hill, Ooty","price_per_night":9000,"rating":4.5,"image":"https://images.unsplash.com/photo-1540541338537-41b8f72dfbb3?w=400&q=80","website":"https://www.sterlingholidays.com"},
    ],
}

HOTELS["Darjeeling"] = {
    "Budget": [
        {"id":"dj-b1","name":"Zostel Darjeeling","location":"Gandhi Road, Darjeeling","price_per_night":750,"rating":4.4,"image":"https://images.unsplash.com/photo-1582719508461-905c673771fd?w=400&q=80","website":"https://www.zostel.com/zostel/darjeeling/"},
        {"id":"dj-b2","name":"Hotel Tower View","location":"The Mall, Darjeeling","price_per_night":1000,"rating":3.8,"image":"https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&q=80","website":"https://www.hoteltowerviewdarjeeling.com"},
        {"id":"dj-b3","name":"Hotel Dekeling","location":"Gandhi Road, Darjeeling","price_per_night":1200,"rating":4.0,"image":"https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&q=80","website":"https://www.dekeling.com"},
    ],
    "Balanced": [
        {"id":"dj-m1","name":"Mayfair Darjeeling","location":"The Mall, Darjeeling","price_per_night":5000,"rating":4.4,"image":"https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400&q=80","website":"https://www.mayfairhotels.com"},
        {"id":"dj-m2","name":"Hotel Sinclairs Darjeeling","location":"18/1 Gandhi Road, Darjeeling","price_per_night":3500,"rating":4.2,"image":"https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&q=80","website":"https://www.sinclairshotels.com"},
        {"id":"dj-m3","name":"Cedar Inn Darjeeling","location":"Zakir Hussain Road, Darjeeling","price_per_night":4200,"rating":4.3,"image":"https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400&q=80","website":"https://www.cedarinn.in"},
    ],
    "Luxury": [
        {"id":"dj-l1","name":"Glenburn Tea Estate","location":"Darjeeling Hills","price_per_night":28000,"rating":4.9,"image":"https://images.unsplash.com/photo-1551882547-ff40c63fe2f5?w=400&q=80","website":"https://www.glenburnteaestate.com"},
        {"id":"dj-l2","name":"Windamere Hotel","location":"Observatory Hill, Darjeeling","price_per_night":12000,"rating":4.7,"image":"https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=400&q=80","website":"https://www.windamerehotel.com"},
        {"id":"dj-l3","name":"Elgin Darjeeling","location":"H.D. Lama Road, Darjeeling","price_per_night":10000,"rating":4.6,"image":"https://images.unsplash.com/photo-1540541338537-41b8f72dfbb3?w=400&q=80","website":"https://www.elginhotels.com"},
    ],
}

HOTELS["Tirupati"] = {
    "Budget": [
        {"id":"tp-b1","name":"Hotel Mayura","location":"G.Car Street, Tirupati","price_per_night":900,"rating":3.8,"image":"https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&q=80","website":"https://www.hotelmayuratirupati.com"},
        {"id":"tp-b2","name":"Hotel Bhimas Residency","location":"Car Street, Tirupati","price_per_night":1200,"rating":4.0,"image":"https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&q=80","website":"https://www.bhimasresidency.com"},
        {"id":"tp-b3","name":"OYO Tirupati","location":"Renigunta Road, Tirupati","price_per_night":850,"rating":3.6,"image":"https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400&q=80","website":"https://www.oyorooms.com"},
    ],
    "Balanced": [
        {"id":"tp-m1","name":"Hotel Bliss","location":"TP Area, Tirupati","price_per_night":3000,"rating":4.2,"image":"https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400&q=80","website":"https://www.hotelblisstirupati.com"},
        {"id":"tp-m2","name":"Marasa Sarovar Premiere","location":"Airport Road, Tirupati","price_per_night":4500,"rating":4.4,"image":"https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&q=80","website":"https://www.sarovarhotels.com"},
        {"id":"tp-m3","name":"Sitara Grand","location":"Leela Mahal Circle, Tirupati","price_per_night":3500,"rating":4.1,"image":"https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400&q=80","website":"https://www.sitaragrand.com"},
    ],
    "Luxury": [
        {"id":"tp-l1","name":"Novotel Vijayawada Varun","location":"MG Road, Vijayawada","price_per_night":9000,"rating":4.6,"image":"https://images.unsplash.com/photo-1551882547-ff40c63fe2f5?w=400&q=80","website":"https://www.accorhotels.com"},
        {"id":"tp-l2","name":"Fortune Kences","location":"TP Area, Tirupati","price_per_night":7500,"rating":4.5,"image":"https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=400&q=80","website":"https://www.fortunehotels.in"},
        {"id":"tp-l3","name":"ITC Kakatiya Hyderabad","location":"Begumpet, Hyderabad","price_per_night":12000,"rating":4.7,"image":"https://images.unsplash.com/photo-1540541338537-41b8f72dfbb3?w=400&q=80","website":"https://www.itchotels.com"},
    ],
}

# Aliases for alternate destination name spellings
HOTELS["Palolem Beach"] = HOTELS.get("Palolem Beach", HOTELS["Baga Beach"])
HOTELS["Basilica of Bom Jesus"] = HOTELS.get("Basilica of Bom Jesus", HOTELS["Baga Beach"])
HOTELS["Golden Temple"] = HOTELS.get("Golden Temple", {
    "Budget": [
        {"id":"gt-b1","name":"Zostel Amritsar","location":"Near Golden Temple, Amritsar","price_per_night":700,"rating":4.4,"image":"https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&q=80","website":"https://www.zostel.com/zostel/amritsar/"},
        {"id":"gt-b2","name":"Hotel Grand Legacy","location":"GT Road, Amritsar","price_per_night":1100,"rating":3.9,"image":"https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&q=80","website":"https://www.hotelgrandlegacy.com"},
        {"id":"gt-b3","name":"Hotel Ritz Plaza","location":"The Mall, Amritsar","price_per_night":1500,"rating":4.0,"image":"https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400&q=80","website":"https://www.hotelritzplaza.com"},
    ],
    "Balanced": [
        {"id":"gt-m1","name":"Hyatt Amritsar","location":"MF Husain Marg, Amritsar","price_per_night":5500,"rating":4.4,"image":"https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400&q=80","website":"https://www.hyatt.com/amritsar"},
        {"id":"gt-m2","name":"Hotel CJ International","location":"GT Road, Amritsar","price_per_night":2800,"rating":4.0,"image":"https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&q=80","website":"https://www.hotelcjinternational.com"},
        {"id":"gt-m3","name":"Lemon Tree Premier Amritsar","location":"GT Road, Amritsar","price_per_night":3500,"rating":4.2,"image":"https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400&q=80","website":"https://www.lemontreehotels.com"},
    ],
    "Luxury": [
        {"id":"gt-l1","name":"Taj Swarna Amritsar","location":"Town Hall Chowk, Amritsar","price_per_night":12000,"rating":4.8,"image":"https://images.unsplash.com/photo-1551882547-ff40c63fe2f5?w=400&q=80","website":"https://www.tajhotels.com/amritsar"},
        {"id":"gt-l2","name":"Hyatt Regency Amritsar","location":"MF Husain Marg, Amritsar","price_per_night":9000,"rating":4.6,"image":"https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=400&q=80","website":"https://www.hyatt.com"},
        {"id":"gt-l3","name":"ITC Mughal Agra","location":"Taj Nagri, Agra","price_per_night":14000,"rating":4.7,"image":"https://images.unsplash.com/photo-1540541338537-41b8f72dfbb3?w=400&q=80","website":"https://www.itchotels.com"},
    ],
})


TIER_PRICE_BANDS = {
    "Budget": (500, 2000),
    "Balanced": (2001, 7000),
    "Luxury": (7001, 100000),
}

# Default fallback hotels by tier when destination not found
DEFAULT_HOTELS = {
    "Budget": [
        {"id": "def-b1", "name": "Zostel", "location": "City Centre", "price_per_night": 800, "rating": 4.2, "image": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&q=80", "website": "https://www.zostel.com"},
        {"id": "def-b2", "name": "FabHotel Select", "location": "Main Market", "price_per_night": 1200, "rating": 3.8, "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&q=80", "website": "https://www.fabhotels.com"},
        {"id": "def-b3", "name": "OYO Flagship", "location": "Bus Stand Road", "price_per_night": 950, "rating": 3.6, "image": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400&q=80", "website": "https://www.oyorooms.com"},
    ],
    "Balanced": [
        {"id": "def-m1", "name": "Lemon Tree Hotel", "location": "City Centre", "price_per_night": 3500, "rating": 4.2, "image": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400&q=80", "website": "https://www.lemontreehotels.com"},
        {"id": "def-m2", "name": "Sarovar Portico", "location": "Main Road", "price_per_night": 2800, "rating": 4.1, "image": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&q=80", "website": "https://www.sarovarhotels.com"},
        {"id": "def-m3", "name": "Fortune Hotel", "location": "Commercial Area", "price_per_night": 4200, "rating": 4.3, "image": "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400&q=80", "website": "https://www.fortunehotels.in"},
    ],
    "Luxury": [
        {"id": "def-l1", "name": "Taj Hotel & Resort", "location": "City Centre", "price_per_night": 15000, "rating": 4.8, "image": "https://images.unsplash.com/photo-1551882547-ff40c63fe2f5?w=400&q=80", "website": "https://www.tajhotels.com"},
        {"id": "def-l2", "name": "ITC Grand", "location": "Business District", "price_per_night": 12000, "rating": 4.7, "image": "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=400&q=80", "website": "https://www.itchotels.com"},
        {"id": "def-l3", "name": "Radisson Blu", "location": "Airport Zone", "price_per_night": 10000, "rating": 4.6, "image": "https://images.unsplash.com/photo-1540541338537-41b8f72dfbb3?w=400&q=80", "website": "https://www.radissonhotels.com"},
    ],
}


def get_hotels(destination, plan_name):
    """Return hotels for a destination and plan tier."""
    tier = plan_name.replace(" Plan", "")
    dest_hotels = HOTELS.get(destination, {})
    hotels = dest_hotels.get(tier, DEFAULT_HOTELS.get(tier, []))
    # Attach destination name to each hotel for display
    result = []
    for h in hotels:
        hotel = dict(h)
        if destination not in hotel["location"]:
            hotel["location"] = f"{hotel['location']}, {destination}"
        result.append(hotel)
    return result
