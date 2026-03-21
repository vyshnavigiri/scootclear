# ============================================================
# 3_Re-Routing_Alerts.py — Re-Routing Alerts (Upcoming)
# This page is a placeholder for the re-routing feature.
# The idea came from Spinal Cord Injury Ontario's suggestion
# to have alerts similar to TTC elevator-down notices.
# This feature is planned but not built yet.
# ============================================================

import streamlit as st
from helpers.theme import apply_page_config, apply_custom_css, show_top_navigation

# --- Page setup ---
apply_page_config("ScootClear — Re-Routing Alerts")
apply_custom_css()
show_top_navigation("Re-Routing Alerts")

st.markdown("## 🔔 Re-Routing Alerts")

# --- Upcoming feature banner ---
st.markdown("""
<div class="upcoming-badge">
    <h2 style="color: #0369a1; margin-top: 0;">🚧 Coming Soon!</h2>
    <p style="font-size: 1.1rem; color: #334155; max-width: 600px; margin: 0 auto;">
        This feature is currently under development and will be available in a future update.
    </p>
</div>
""", unsafe_allow_html=True)

# --- Explanation of what this feature will do ---
st.markdown("### What are Re-Routing Alerts?")

st.markdown("""
Based on valuable feedback from **Spinal Cord Injury Ontario**, we are developing 
a re-routing alert system inspired by how the **TTC posts notices when an elevator 
is down** and suggests alternate accessible routes.
""")

st.markdown("### How it will work:")

st.markdown("""
<div class="info-card">
    <strong>1. Automatic Detection</strong><br>
    When an area receives multiple obstruction reports (hitting our threshold), 
    the system will automatically generate an alert for that street or intersection.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <strong>2. Alert Message</strong><br>
    Users approaching the area will see a message like:<br>
    <em>"⚠️ Obstruction reported on King St near Spadina. 
    Please consider re-routing your path to another street to avoid 
    accessibility barriers in this area."</em>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <strong>3. Suggested Alternate Routes</strong><br>
    The system will suggest nearby accessible streets that have fewer 
    reported obstructions — similar to how Google Maps shows transit 
    disruptions.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <strong>4. Active Alerts Map</strong><br>
    A map showing all currently active re-routing alerts across the GTA, 
    colour-coded by severity.
</div>
""", unsafe_allow_html=True)

# --- Why this matters ---
st.markdown("### Why this matters")

st.markdown("""
<div class="impact-section">
    <h4>Feedback from Spinal Cord Injury Ontario</h4>
    <h3>Real challenges faced by wheelchair users</h3>
    <p>
        When a sidewalk is blocked, wheelchair users have to track back and find 
        an alternate route, which can be very time-consuming. Sometimes there is 
        no alternate route and they are forced to go down a curb — which is unsafe. 
        Construction zones are especially problematic, particularly in downtown Toronto.
    </p>
    <p style="margin-top: 12px;">
        A re-routing system would help by warning people <strong>before</strong> 
        they reach the obstruction, saving time and keeping them safe.
    </p>
</div>
""", unsafe_allow_html=True)

# --- Future integration note ---
st.markdown("""
<div class="warning-card">
    <strong>🔮 Future Vision:</strong> We hope to eventually integrate this 
    with <strong>Google Maps</strong> so that re-routing alerts show up when 
    someone looks up a route — just like how transit disruptions currently appear. 
    This was recommended by SCI Ontario as the best way to reach the most people.
</div>
""", unsafe_allow_html=True)
