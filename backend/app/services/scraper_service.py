"""Web scraping service for destination enrichment using BeautifulSoup."""

import requests
from bs4 import BeautifulSoup
from flask import current_app
from app import get_db
from app.utils.constants import DESTINATIONS


def scrape_destination_info(destination_name):
    """Scrape Wikipedia for destination information."""
    try:
        search_url = f"https://en.wikipedia.org/wiki/{destination_name.replace(' ', '_')}"
        headers = {"User-Agent": "IndiaSmartTripPlanner/1.0"}
        resp = requests.get(search_url, headers=headers, timeout=10)

        if resp.status_code != 200:
            return None

        soup = BeautifulSoup(resp.text, "html.parser")

        # Extract first two paragraphs as description
        content = soup.find("div", {"id": "mw-content-text"})
        paragraphs = []
        if content:
            for p in content.find_all("p", recursive=True):
                text = p.get_text(strip=True)
                if len(text) > 50:
                    paragraphs.append(text)
                    if len(paragraphs) >= 2:
                        break

        description = " ".join(paragraphs) if paragraphs else f"{destination_name} is a popular tourist destination in India."

        return {
            "description": description[:500],
            "source": "wikipedia",
        }

    except Exception as e:
        current_app.logger.warning(f"Scrape error for {destination_name}: {e}")
        return None


def enrich_destinations():
    """Scrape and enrich all destinations in the database."""
    db = get_db()
    enriched = 0

    for state, places in DESTINATIONS.items():
        for place in places:
            existing = db.destinations.find_one({"state": state, "name": place})
            if existing and existing.get("description") and len(existing["description"]) > 50:
                continue

            info = scrape_destination_info(place)
            if info:
                db.destinations.update_one(
                    {"state": state, "name": place},
                    {"$set": {"description": info["description"], "source": info["source"]}},
                )
                enriched += 1

    return enriched
