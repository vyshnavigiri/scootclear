# ============================================================
# obstruction_detector.py
# This module looks at the uploaded photo and tries to figure
# out what kind of obstruction is in it (scooter, bin, etc.)
# It uses simple image analysis ,not a full AI model, but
# enough to show the concept for our prototype.
# ============================================================

import numpy as np
from PIL import Image, ImageStat, ImageFilter


# Messages for each obstruction type
OBSTRUCTION_MESSAGES = {
    "Construction":          "Construction materials or barriers appear to be present on the sidewalk.",
    "Garbage / Recycling Bins": "A garbage or recycling bin seems to be obstructing the pathway.",
    "E-Scooter":             "An e-scooter or kick scooter appears to be blocking the sidewalk.",
    "Bicycle / E-Bike":      "A bicycle or e-bike may be blocking the accessible route.",
    "Signboard":             "A signboard or A-frame sign may be narrowing the walkway.",
    "Other":                 "A potential sidewalk obstruction has been detected in the image.",
}


def detect_obstruction(img, category_selected_by_user):
    """
    Analyse the image and return information about the obstruction.

    Parameters:
        img: a PIL Image object (the uploaded photo)
        category_selected_by_user: the obstruction type the user chose in the form

    Returns a dictionary with:
        - category: the type of obstruction
        - message: a description of what was detected
        - confidence: "High", "Medium", or "Low"
        - confidence_percent: a number from 0 to 100
        - details: a list of observations about the image
    """
    details = []
    width, height = img.size

    # --- ANALYSIS 1: Where are the objects? ---
    # Sidewalk obstructions are usually in the lower half of the photo
    grey = img.convert("L")
    edges = grey.filter(ImageFilter.FIND_EDGES)
    edge_array = np.array(edges)

    middle_y = height // 2
    lower_half_edges = edge_array[middle_y:, :].mean()
    upper_half_edges = edge_array[:middle_y, :].mean()

    if lower_half_edges > upper_half_edges * 1.3:
        details.append("Objects detected in the lower half of the image, consistent with sidewalk-level obstructions.")
    elif upper_half_edges > lower_half_edges * 1.3:
        details.append("Most visual activity is in the upper portion — the obstruction may be elevated (like a sign).")
    else:
        details.append("Objects are distributed across the frame.")

    # --- ANALYSIS 2: Colour analysis ---
    rgb = np.array(img.convert("RGB"))
    red_avg = rgb[:, :, 0].mean()
    green_avg = rgb[:, :, 1].mean()
    blue_avg = rgb[:, :, 2].mean()

    # Check for green (foliage/grass nearby)
    if green_avg > red_avg * 1.15 and green_avg > blue_avg * 1.1:
        details.append("Green tones detected — there may be grass or trees near the obstruction.")

    # Check if it's dark (night photo)
    if red_avg < 80 and green_avg < 80 and blue_avg < 80:
        details.append("Image appears dark — possibly taken at night or in low light.")

    # Check if it's well-lit
    if red_avg > 180 and green_avg > 180 and blue_avg > 180:
        details.append("Image is bright and well-lit — good visibility.")

    # Check for grey/metallic tones (common for scooters, bikes, bins)
    grey_pixels = np.abs(rgb[:, :, 0].astype(int) - rgb[:, :, 1].astype(int)) < 15
    grey_pixels = grey_pixels & (np.abs(rgb[:, :, 1].astype(int) - rgb[:, :, 2].astype(int)) < 15)
    grey_ratio = grey_pixels.mean()

    if grey_ratio > 0.35:
        details.append("Significant grey/metallic tones detected — consistent with scooters, bikes, or metal bins.")

    # --- ANALYSIS 3: Calculate confidence ---
    edge_mean = edge_array.mean()

    if edge_mean > 15:
        confidence = "High"
        confidence_percent = 85
        details.append("Rich detail in the image — quality is good for verification.")
    elif edge_mean > 7:
        confidence = "Medium"
        confidence_percent = 65
        details.append("Moderate detail — image is usable but could be clearer.")
    else:
        confidence = "Low"
        confidence_percent = 35
        details.append("Low detail — consider uploading a higher-quality photo.")

    # Get the message for this type of obstruction
    message = OBSTRUCTION_MESSAGES.get(
        category_selected_by_user,
        OBSTRUCTION_MESSAGES["Other"]
    )

    return {
        "category": category_selected_by_user,
        "message": message,
        "confidence": confidence,
        "confidence_percent": confidence_percent,
        "details": details,
    }
