# ============================================================
# image_checks.py
# This module checks if an uploaded photo is genuine.
# It runs 6 simple tests on the image and gives a score
# from 0 to 100 (higher = more likely real).
# ============================================================

import numpy as np
from PIL import Image, ImageStat, ImageFilter


def check_image_is_genuine(img):
    """
    Run 6 checks on the image to see if it looks like a real photo.
    Returns a dictionary with:
        - passed: True or False
        - score: number from 0 to 100
        - checks: list of each individual check result
        - message: a summary message
    """
    checks = []
    score = 100  # start at 100 and subtract for problems

    # --- CHECK 1: Resolution ---
    width, height = img.size
    if width < 200 or height < 200:
        checks.append({
            "name": "Resolution",
            "status": "warning",
            "detail": f"Image is very small ({width}x{height}). Could be a thumbnail."
        })
        score = score - 15
    else:
        checks.append({
            "name": "Resolution",
            "status": "pass",
            "detail": f"Image resolution {width}x{height} is good."
        })

    # --- CHECK 2: Pixel Density ---
    total_pixels = width * height
    if total_pixels < 10000:
        checks.append({
            "name": "Pixel Density",
            "status": "warning",
            "detail": "Very few pixels — might be an icon or synthetic image."
        })
        score = score - 10
    else:
        checks.append({
            "name": "Pixel Density",
            "status": "pass",
            "detail": "Pixel count looks normal for a real photo."
        })

    # --- CHECK 3: Colour Variance ---
    # Real photos have lots of different colours. Fake/synthetic images
    # often have very uniform colours.
    rgb_image = img.convert("RGB")
    stats = ImageStat.Stat(rgb_image)
    avg_colour_spread = sum(stats.stddev) / 3

    if avg_colour_spread < 10:
        checks.append({
            "name": "Colour Variance",
            "status": "warning",
            "detail": "Almost no colour variation — image may be synthetic."
        })
        score = score - 20
    elif avg_colour_spread < 25:
        checks.append({
            "name": "Colour Variance",
            "status": "caution",
            "detail": "Low colour variety. Could be heavily filtered."
        })
        score = score - 10
    else:
        checks.append({
            "name": "Colour Variance",
            "status": "pass",
            "detail": "Good colour variety, consistent with real photos."
        })

    # --- CHECK 4: Edge Density ---
    # Real outdoor photos have lots of edges (buildings, trees, objects).
    # AI-generated or blurred images have very few.
    grey_image = img.convert("L")
    edges = grey_image.filter(ImageFilter.FIND_EDGES)
    edge_average = ImageStat.Stat(edges).mean[0]

    if edge_average < 3:
        checks.append({
            "name": "Edge Density",
            "status": "warning",
            "detail": "Very few edges — might be AI-generated or heavily blurred."
        })
        score = score - 15
    elif edge_average > 80:
        checks.append({
            "name": "Edge Density",
            "status": "caution",
            "detail": "Unusually many edges — could be a screenshot of text."
        })
        score = score - 10
    else:
        checks.append({
            "name": "Edge Density",
            "status": "pass",
            "detail": "Edge pattern looks like a real-world photo."
        })

    # --- CHECK 5: Sensor Noise ---
    # Real camera photos have tiny random noise from the sensor.
    # Perfectly clean images are suspicious.
    grey_array = np.array(grey_image, dtype=np.float64)
    if grey_array.shape[0] >= 50 and grey_array.shape[1] >= 50:
        # Check a small corner patch for noise
        patch = grey_array[:50, :50]
        noise_level = np.var(patch)
        if noise_level < 1:
            checks.append({
                "name": "Sensor Noise",
                "status": "warning",
                "detail": "No camera noise found — might not be a real photo."
            })
            score = score - 15
        else:
            checks.append({
                "name": "Sensor Noise",
                "status": "pass",
                "detail": "Normal camera noise pattern detected."
            })
    else:
        checks.append({
            "name": "Sensor Noise",
            "status": "warning",
            "detail": "Image too small to check for noise."
        })
        score = score - 5

    # --- CHECK 6: Aspect Ratio ---
    # Phone cameras use standard ratios like 4:3, 16:9, 3:2, etc.
    ratio = max(width, height) / max(min(width, height), 1)
    common_ratios = [1.0, 1.33, 1.5, 1.78, 2.0, 2.17]
    closest_ratio = min(common_ratios, key=lambda r: abs(r - ratio))

    if abs(ratio - closest_ratio) < 0.15:
        checks.append({
            "name": "Aspect Ratio",
            "status": "pass",
            "detail": f"Aspect ratio ({ratio:.2f}) matches common cameras."
        })
    else:
        checks.append({
            "name": "Aspect Ratio",
            "status": "caution",
            "detail": f"Unusual aspect ratio ({ratio:.2f}). May be cropped."
        })
        score = score - 5

    # --- FINAL SCORE ---
    # Make sure score stays between 0 and 100
    if score < 0:
        score = 0
    if score > 100:
        score = 100

    passed = score >= 50

    if score >= 80:
        message = "This image appears to be a genuine photograph."
    elif score >= 50:
        message = "This image has some minor concerns but seems acceptable."
    else:
        message = "This image failed multiple checks and may be fake or heavily manipulated."

    return {
        "passed": passed,
        "score": score,
        "checks": checks,
        "message": message,
    }
