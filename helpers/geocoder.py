# ============================================================
# geocoder.py
# Converts a street intersection + postal code into latitude
# and longitude coordinates.
#
# We use "geopy" with "Nominatim" (OpenStreetMap) which is
# FREE and does NOT need an API key.
#
# Example:
#   get_coordinates("King and Spadina", "M5V 1K4")
#   --> {"latitude": 43.6444, "longitude": -79.3947, "found": True, ...}
# ============================================================

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time


# Create the geocoder (only once, reused for all lookups)
# The user_agent is just a name to identify our app to OpenStreetMap
geocoder = Nominatim(user_agent="scootclear-app")


def get_coordinates(street_intersection, postal_code=""):
    """
    Look up the latitude and longitude for a street intersection.

    Parameters:
        street_intersection: like "King and Spadina" or "Yonge & Dundas"
        postal_code: like "M5V 1K4" (optional but helps accuracy)

    Returns a dictionary:
        {
            "latitude": 43.6444,
            "longitude": -79.3947,
            "found": True,
            "full_address": "King Street West & Spadina Avenue, Toronto, ON, Canada",
            "error": None
        }
    If the location cannot be found, "found" will be False.
    """

    # Build the search query
    # Adding "Ontario, Canada" helps Nominatim find GTA locations
    if postal_code:
        query = f"{street_intersection}, {postal_code}, Ontario, Canada"
    else:
        query = f"{street_intersection}, Ontario, Canada"

    try:
        # Ask Nominatim to find the coordinates
        # timeout=10 means wait up to 10 seconds for a response
        result = geocoder.geocode(query, timeout=10)

        # Small delay to be polite to the free server (max 1 request per second)
        time.sleep(1)

        if result:
            return {
                "latitude": round(result.latitude, 6),
                "longitude": round(result.longitude, 6),
                "found": True,
                "full_address": result.address,
                "error": None,
            }
        else:
            # Nominatim didn't find anything — try without postal code
            if postal_code:
                result = geocoder.geocode(
                    f"{street_intersection}, Ontario, Canada",
                    timeout=10,
                )
                time.sleep(1)
                if result:
                    return {
                        "latitude": round(result.latitude, 6),
                        "longitude": round(result.longitude, 6),
                        "found": True,
                        "full_address": result.address,
                        "error": None,
                    }

            return {
                "latitude": None,
                "longitude": None,
                "found": False,
                "full_address": None,
                "error": "Location not found. Please check the intersection name and try again.",
            }

    except GeocoderTimedOut:
        return {
            "latitude": None,
            "longitude": None,
            "found": False,
            "full_address": None,
            "error": "The location lookup timed out. Please try again.",
        }
    except GeocoderUnavailable:
        return {
            "latitude": None,
            "longitude": None,
            "found": False,
            "full_address": None,
            "error": "The geocoding service is currently unavailable. Please try again later.",
        }
    except Exception as e:
        return {
            "latitude": None,
            "longitude": None,
            "found": False,
            "full_address": None,
            "error": f"Something went wrong: {str(e)}",
        }
