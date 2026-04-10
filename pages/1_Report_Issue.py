# ============================================================
# 1_Report_Issue.py — Report an Obstruction
# This page lets users fill out a form, upload a photo,
# and submit a report. The photo goes through:
#   Step 1: Authenticity validation (is it a real photo?)
#   Step 2: AI obstruction detection (what type of obstruction?)
#   Step 3: Hotspot check (is this area a recurring problem?)
# ============================================================

import streamlit as st
import uuid
import datetime
from PIL import Image

from helpers.theme import apply_page_config, apply_custom_css, show_top_navigation
from helpers.file_storage import load_all_reports, save_new_report
from helpers.image_checks import check_image_is_genuine
from helpers.obstruction_detector import detect_obstruction
from helpers.hotspot_finder import find_nearby_reports
from helpers.geocoder import get_coordinates

# --- Page setup ---
apply_page_config("ScootClear — Report Issue")
apply_custom_css()
show_top_navigation("Report Issue")

# --- Page title ---
st.markdown("## Report a Sidewalk Obstruction")
st.markdown("Help make GTA sidewalks safer by reporting obstructions you encounter.")

# ============================================================
# REPORT FORM
# ============================================================
with st.form("report_form", clear_on_submit=True):
    col1, col2 = st.columns([1, 1])

    with col1:
        # Obstruction type dropdown
        category = st.selectbox(
            "Type of Obstruction",
            [
                "Construction",
                "Garbage / Recycling Bins",
                "E-Scooter",
                "Bicycle / E-Bike",
                "Signboard",
                "Other",
            ],
        )
        # Description
        description = st.text_area(
            "Describe the issue",
            placeholder="Example: Construction barriers blocking the curb cut at King & Yonge...",
            height=100,
        )

    with col2:
        # Location inputs — street name and postal code
        st.markdown("**Location**")
        street_intersection = st.text_input(
            "Street Intersection",
            placeholder="Example: King and Spadina, Toronto",
            help="Enter the nearest intersection or street address",
        )
        postal_code = st.text_input(
            "Postal Code",
            placeholder="Example: M5V 1K4",
            help="The postal code of the area (helps find the exact location)",
        )

    # Photo upload
    st.markdown("**Upload a Photo of the Obstruction**")
    uploaded_file = st.file_uploader(
        "Choose a JPG or PNG image (max 10 MB)",
        type=["jpg", "jpeg", "png"],
    )

    # Submit button
    submitted = st.form_submit_button("Submit Report", use_container_width=True)


# ============================================================
# WHAT HAPPENS AFTER SUBMIT
# ============================================================
if submitted:
    # Check that required fields are filled
    if not uploaded_file:
        st.error("Please upload a photo before submitting.")
        st.stop()
    if not street_intersection:
        st.warning("Please enter a street intersection (e.g., King and Spadina, Toronto).")
        st.stop()

    # Open the uploaded image
    img = Image.open(uploaded_file)
    st.image(img, caption="Your uploaded photo", use_container_width=True)

    # ----------------------------------------------------------
    # GEOCODING: Convert street intersection to lat/long
    # ----------------------------------------------------------
    st.markdown("### Finding Location Coordinates")
    with st.spinner("Looking up the location..."):
        geo_result = get_coordinates(street_intersection, postal_code)

    if geo_result["found"]:
        latitude = geo_result["latitude"]
        longitude = geo_result["longitude"]
        location_name = street_intersection  # store the user-friendly name

        st.markdown(f"""
        <div class="success-card">
            ✅ <strong>Location found!</strong><br>
            {geo_result['full_address']}<br>
            <span style="color:#64748b; font-size:0.85rem;">
                Coordinates: {latitude}, {longitude} (calculated automatically)
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="danger-card">
            <strong>❌ Could not find this location</strong><br>
            {geo_result['error']}<br><br>
            <strong>Tips:</strong> Try including the city name (e.g., "King and Spadina, Toronto")
            or check the spelling of the street names.
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # ----------------------------------------------------------
    # STEP 1: IMAGE AUTHENTICITY VALIDATION
    # ----------------------------------------------------------
    st.markdown("### Step 1: Image Authenticity Validation")
    with st.spinner("Checking if the photo is genuine..."):
        validation_result = check_image_is_genuine(img)

    # Show the score
    score = validation_result["score"]
    if score >= 80:
        score_colour = "#198754"  # green
    elif score >= 50:
        score_colour = "#f59e0b"  # orange
    else:
        score_colour = "#dc3545"  # red

    st.markdown(f"""
    <div class="score-display">
        <div class="score-number" style="color:{score_colour}">{score}/100</div>
        <div>
            <strong>Authenticity Score</strong><br>
            <span style="color:#64748b;">{validation_result['message']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Show each individual check
    for check in validation_result["checks"]:
        if check["status"] == "pass":
            icon = "✅"
            card_class = "info-card"
        elif check["status"] == "caution":
            icon = "⚠️"
            card_class = "warning-card"
        else:
            icon = "⚠️"
            card_class = "warning-card"

        st.markdown(f"""
        <div class="{card_class}">
            {icon} <strong>{check['name']}</strong>: {check['detail']}
        </div>
        """, unsafe_allow_html=True)

    # If the image failed, stop here
    if not validation_result["passed"]:
        st.markdown("""
        <div class="danger-card">
            <strong>❌ Image Rejected</strong><br>
            This photo did not pass our authenticity checks. Please upload a
            genuine, unedited photograph taken at the location.
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # ----------------------------------------------------------
    # STEP 2: AI OBSTRUCTION DETECTION
    # ----------------------------------------------------------
    st.markdown("### Step 2: AI Obstruction Detection")
    with st.spinner("Analysing the image for obstructions..."):
        detection_result = detect_obstruction(img, category)

    # Show detection results
    confidence = detection_result["confidence"]
    conf_pct = detection_result["confidence_percent"]

    if confidence == "High":
        conf_colour = "#198754"
    elif confidence == "Medium":
        conf_colour = "#f59e0b"
    else:
        conf_colour = "#dc3545"

    st.markdown(f"""
    <div class="info-card">
        <strong>Detected:</strong> {detection_result['category']}<br>
        <strong>Confidence:</strong>
        <span style="color:{conf_colour}; font-weight:bold;">{confidence} ({conf_pct}%)</span><br><br>
         <em>{detection_result['message']}</em>
    </div>
    """, unsafe_allow_html=True)

    # Show detailed observations
    for detail in detection_result["details"]:
        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;🔍 {detail}")

    # ----------------------------------------------------------
    # STEP 3: RECURRING HOTSPOT CHECK
    # ----------------------------------------------------------
    st.markdown("### Step 3: Recurring Hotspot Check")

    existing_reports = load_all_reports()
    nearby_reports = find_nearby_reports(latitude, longitude, existing_reports, radius_km=0.3)

    if len(nearby_reports) >= 3:
        # This area has hit the threshold!
        st.markdown(f"""
        <div class="warning-card">
            <strong>⚠️ Recurring Hotspot Alert!</strong><br>
            <strong>{len(nearby_reports)} previous reports</strong> have been filed
            within 300 metres of this location. This area appears to be a
            recurring obstruction hotspot.<br><br>
            🚧 <strong>Please consider re-routing your path to another street
            to avoid accessibility barriers in this area.</strong><br><br>
            <em>Visit the Hotspot Map page for a full view of problem areas.</em>
        </div>
        """, unsafe_allow_html=True)
    elif len(nearby_reports) >= 1:
        st.markdown(f"""
        <div class="info-card">
             <strong>{len(nearby_reports)} other report(s)</strong> exist near this location.
            We are monitoring this area.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-card">
            No previous reports near this location. This appears to be a new report area.
        </div>
        """, unsafe_allow_html=True)

    # ----------------------------------------------------------
    # SAVE THE REPORT
    # ----------------------------------------------------------
    new_report = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.now().isoformat(),
        "category": category,
        "description": description,
        "street_intersection": street_intersection,
        "postal_code": postal_code,
        "latitude": latitude,
        "longitude": longitude,
        "location_name": location_name,
        "authenticity_score": score,
        "confidence": confidence,
        "confidence_percent": conf_pct,
    }

    save_new_report(new_report)

    st.markdown("""
    <div class="success-card">
        <strong> Report submitted successfully!</strong><br>
        Thank you for helping make GTA sidewalks safer and more accessible.
        Your report will appear on the Hotspot Map and Safety Dashboard.
    </div>
    """, unsafe_allow_html=True)
    st.balloons()
