# ============================================================
# seed_data.py — Generate sample reports for demo
# Run this once to fill the app with example data:
#   python seed_data.py
# ============================================================

import json
import uuid
import random
import os
from datetime import datetime, timedelta

# Where to save the data
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")
REPORTS_FILE = os.path.join(DATA_FOLDER, "reports.json")

# Sample GTA locations (some repeated to create hotspots)
LOCATIONS = [
    {"name": "King & Spadina, Toronto", "lat": 43.6444, "lon": -79.3947, "postal": "M5V 1K4"},
    {"name": "King & Spadina, Toronto", "lat": 43.6448, "lon": -79.3952, "postal": "M5V 1K4"},
    {"name": "King & Spadina, Toronto", "lat": 43.6441, "lon": -79.3943, "postal": "M5V 1K4"},
    {"name": "King & Spadina, Toronto", "lat": 43.6446, "lon": -79.3949, "postal": "M5V 1K4"},
    {"name": "Yonge & Dundas Square", "lat": 43.6561, "lon": -79.3802, "postal": "M5B 1N2"},
    {"name": "Yonge & Dundas Square", "lat": 43.6558, "lon": -79.3806, "postal": "M5B 1N2"},
    {"name": "Yonge & Dundas Square", "lat": 43.6564, "lon": -79.3799, "postal": "M5B 1N2"},
    {"name": "Queen & Bathurst, Toronto", "lat": 43.6484, "lon": -79.4113, "postal": "M5V 2B4"},
    {"name": "Bloor & Ossington, Toronto", "lat": 43.6601, "lon": -79.4265, "postal": "M6H 1Y8"},
    {"name": "Harbourfront Centre", "lat": 43.6389, "lon": -79.3819, "postal": "M5J 2H1"},
    {"name": "Harbourfront Centre", "lat": 43.6391, "lon": -79.3822, "postal": "M5J 2H1"},
    {"name": "Harbourfront Centre", "lat": 43.6387, "lon": -79.3816, "postal": "M5J 2H1"},
    {"name": "Kensington Market", "lat": 43.6547, "lon": -79.4007, "postal": "M5T 2K2"},
    {"name": "Distillery District", "lat": 43.6503, "lon": -79.3596, "postal": "M5A 3C4"},
    {"name": "Liberty Village", "lat": 43.6379, "lon": -79.4209, "postal": "M6K 3P6"},
    {"name": "Danforth & Broadview", "lat": 43.6688, "lon": -79.3532, "postal": "M4K 1P3"},
    {"name": "Mississauga City Centre", "lat": 43.5890, "lon": -79.6441, "postal": "L5B 2C9"},
    {"name": "Mississauga City Centre", "lat": 43.5893, "lon": -79.6438, "postal": "L5B 2C9"},
    {"name": "Brampton Downtown", "lat": 43.6834, "lon": -79.7590, "postal": "L6X 0E2"},
    {"name": "Scarborough Town Centre", "lat": 43.7764, "lon": -79.2578, "postal": "M1P 4P5"},
    {"name": "North York Centre", "lat": 43.7680, "lon": -79.4136, "postal": "M2N 5N8"},
    {"name": "Etobicoke Lakeshore", "lat": 43.6205, "lon": -79.4863, "postal": "M8V 1A1"},
    {"name": "St. Clair & Yonge", "lat": 43.6879, "lon": -79.3935, "postal": "M4T 1W5"},
]

# Weighted towards construction and bins (based on SCI feedback)
CATEGORIES = [
    "Construction", "Construction", "Construction", "Construction",
    "Garbage / Recycling Bins", "Garbage / Recycling Bins", "Garbage / Recycling Bins",
    "E-Scooter", "E-Scooter",
    "Bicycle / E-Bike",
    "Signboard",
    "Other",
]

DESCRIPTIONS = [
    "Construction barriers blocking the curb cut completely.",
    "Recycling bins left out on the sidewalk after collection day.",
    "Two e-scooters parked across the accessible ramp.",
    "Construction fencing forces pedestrians onto the road.",
    "Garbage bags piled up blocking the entire sidewalk width.",
    "A-frame sign from a restaurant narrowing the walkway.",
    "E-scooter knocked over in front of the bus stop.",
    "Construction materials blocking the tactile paving strip.",
    "Bins and bags taking up the whole sidewalk section.",
    "E-bike chained to the accessibility ramp handrail.",
    "Delivery van parked on the sidewalk blocking the path.",
    "Multiple scooters clustered near the pedestrian crossing.",
    "Construction debris with no accessible detour provided.",
]

CONFIDENCES = [
    ("High", 85), ("High", 88), ("High", 92), ("High", 80),
    ("Medium", 65), ("Medium", 70), ("Medium", 75),
    ("Low", 35), ("Low", 42),
]


def generate_sample_reports():
    """Create a list of sample reports."""
    reports = []
    now = datetime.now()

    for loc in LOCATIONS:
        conf = random.choice(CONFIDENCES)
        report = {
            "id": str(uuid.uuid4()),
            "timestamp": (now - timedelta(
                days=random.randint(0, 60),
                hours=random.randint(6, 22),
                minutes=random.randint(0, 59),
            )).isoformat(),
            "category": random.choice(CATEGORIES),
            "description": random.choice(DESCRIPTIONS),
            "street_intersection": loc["name"],
            "postal_code": loc["postal"],
            "latitude": loc["lat"] + random.uniform(-0.0005, 0.0005),
            "longitude": loc["lon"] + random.uniform(-0.0005, 0.0005),
            "location_name": loc["name"],
            "authenticity_score": random.randint(62, 98),
            "confidence": conf[0],
            "confidence_percent": conf[1],
        }
        reports.append(report)

    return reports


if __name__ == "__main__":
    # Create data folder if needed
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    reports = generate_sample_reports()

    with open(REPORTS_FILE, "w") as f:
        json.dump(reports, f, indent=2)

    print(f"Done! Created {len(reports)} sample reports in {REPORTS_FILE}")
