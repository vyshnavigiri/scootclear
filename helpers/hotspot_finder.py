# ============================================================
# hotspot_finder.py
# This module figures out which areas have the most reports.
# It groups reports by location and assigns risk levels:
#   Red = High Risk (lots of reports)
#   Orange = Moderate Risk
#   Green = Low Risk
# ============================================================

import math
import pandas as pd


def find_nearby_reports(new_lat, new_lon, all_reports, radius_km=0.3):
    """
    Find all existing reports within a certain distance of a new report.

    Parameters:
        new_lat: latitude of the new report
        new_lon: longitude of the new report
        all_reports: list of all existing reports
        radius_km: how close reports need to be (default 300 metres)

    Returns: a list of nearby reports
    """
    nearby = []

    for report in all_reports:
        try:
            report_lat = float(report.get("latitude", 0))
            report_lon = float(report.get("longitude", 0))
        except (ValueError, TypeError):
            continue

        # Calculate distance using the Haversine formula
        # (this is the formula for distance between two GPS points)
        distance = calculate_distance_km(new_lat, new_lon, report_lat, report_lon)

        if distance <= radius_km:
            nearby.append(report)

    return nearby


def calculate_distance_km(lat1, lon1, lat2, lon2):
    """
    Calculate the distance in kilometres between two GPS coordinates.
    Uses the Haversine formula.
    """
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    # Haversine formula
    a = (math.sin(delta_lat / 2) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) *
         math.sin(delta_lon / 2) ** 2)
    distance = 2 * 6371 * math.asin(math.sqrt(a))  # 6371 = Earth's radius in km

    return distance


def calculate_hotspots(reports, grid_size=0.002):
    """
    Group reports into a grid and figure out which areas are hotspots.

    Parameters:
        reports: list of all reports
        grid_size: size of each grid cell in degrees (~200 metres)

    Returns: a pandas DataFrame with columns:
        lat, lon, count, colour, risk_level, description, types
    """
    if not reports:
        return pd.DataFrame()

    # Convert to DataFrame
    df = pd.DataFrame(reports)
    if "latitude" not in df.columns or "longitude" not in df.columns:
        return pd.DataFrame()

    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df = df.dropna(subset=["latitude", "longitude"])

    if df.empty:
        return pd.DataFrame()

    # Snap each report to a grid cell
    df["grid_lat"] = (df["latitude"] / grid_size).round() * grid_size
    df["grid_lon"] = (df["longitude"] / grid_size).round() * grid_size

    # Count reports in each grid cell
    grouped = df.groupby(["grid_lat", "grid_lon"]).agg(
        count=("id", "count"),
        types=("category", lambda x: ", ".join(x.unique())),
    ).reset_index()

    grouped.rename(columns={"grid_lat": "lat", "grid_lon": "lon"}, inplace=True)

    # Assign risk levels based on how many reports are in each cell
    max_count = grouped["count"].max()

    colours = []
    risk_levels = []
    descriptions = []

    for count in grouped["count"]:
        ratio = count / max(max_count, 1)
        if ratio >= 0.7:
            colours.append("red")
            risk_levels.append("High Risk")
            descriptions.append("Critical area — frequent obstructions reported")
        elif ratio >= 0.4:
            colours.append("orange")
            risk_levels.append("Moderate Risk")
            descriptions.append("Multiple reports received in this area")
        else:
            colours.append("green")
            risk_levels.append("Low Risk")
            descriptions.append("Occasional reports — monitor this area")

    grouped["colour"] = colours
    grouped["risk_level"] = risk_levels
    grouped["description"] = descriptions

    return grouped
