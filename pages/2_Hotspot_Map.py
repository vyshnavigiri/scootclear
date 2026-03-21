# ============================================================
# 2_Hotspot_Map.py — Hotspot Map
# Interactive map showing where obstructions are reported most.
# Includes a heatmap layer, colour-coded risk circles,
# top problem locations table, and obstruction type breakdown.
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium

from helpers.theme import apply_page_config, apply_custom_css, show_top_navigation
from helpers.file_storage import load_all_reports
from helpers.hotspot_finder import calculate_hotspots

# --- Page setup ---
apply_page_config("ScootClear — Hotspot Map")
apply_custom_css()
show_top_navigation("Hotspot Map")

st.markdown("## 🗺️ Obstruction Hotspot Map")
st.markdown("See where accessibility barriers are reported most across the GTA.")

# --- Legend ---
st.markdown("""
<div style="display:flex; gap:20px; padding:10px 16px; background:#ffffff;
     border-radius:10px; border:1px solid #bae6fd; margin-bottom:15px;
     flex-wrap:wrap; justify-content:center; font-size:0.9rem;">
    <span>🔴 <strong>High Risk</strong> — Frequent obstructions</span>
    <span>🟠 <strong>Moderate Risk</strong> — Multiple reports</span>
    <span>🟢 <strong>Low Risk</strong> — Occasional reports</span>
</div>
""", unsafe_allow_html=True)

# --- Load data ---
reports = load_all_reports()

if not reports:
    st.info("🗺️ No reports yet! Go to **Report Issue** to submit the first one.")
    # Show empty GTA map
    m = folium.Map(location=[43.6532, -79.3832], zoom_start=11, tiles="CartoDB positron")
    st_folium(m, use_container_width=True, height=500)
    st.stop()

# --- Map controls ---
col1, col2 = st.columns(2)
with col1:
    show_heatmap = st.toggle("Show Heatmap Layer", value=True)
with col2:
    show_markers = st.toggle("Show Individual Markers", value=True)

# --- Build the map ---
df = pd.DataFrame(reports)
df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
df = df.dropna(subset=["latitude", "longitude"])

center_lat = df["latitude"].mean()
center_lon = df["longitude"].mean()

m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles="CartoDB positron")

# Add heatmap
if show_heatmap and len(df) > 0:
    heat_data = df[["latitude", "longitude"]].values.tolist()
    HeatMap(
        heat_data,
        radius=25,
        blur=15,
        gradient={0.2: "#22c55e", 0.5: "#f59e0b", 0.8: "#ef4444", 1.0: "#991b1b"},
    ).add_to(m)

# Add markers
if show_markers:
    # Colour for each obstruction type
    colour_map = {
        "Construction": "orange",
        "Garbage / Recycling Bins": "green",
        "E-Scooter": "red",
        "Bicycle / E-Bike": "blue",
        "Signboard": "purple",
        "Other": "gray",
    }

    marker_cluster = MarkerCluster().add_to(m)

    for _, row in df.iterrows():
        cat = row.get("category", "Other")
        icon_colour = colour_map.get(cat, "gray")

        popup_text = f"""
        <b>{cat}</b><br>
        📍 {row.get('location_name', 'N/A')}<br>
        🕐 {str(row.get('timestamp', ''))[:16]}<br>
        <em>{str(row.get('description', ''))[:80]}</em>
        """

        folium.Marker(
            [row["latitude"], row["longitude"]],
            popup=folium.Popup(popup_text, max_width=250),
            tooltip=f"{cat} — {row.get('location_name', '')}",
            icon=folium.Icon(color=icon_colour, icon="exclamation-sign", prefix="glyphicon"),
        ).add_to(marker_cluster)

    # Add risk circles from hotspot analysis
    hotspots = calculate_hotspots(reports)
    if not hotspots.empty:
        for _, hs in hotspots.iterrows():
            folium.Circle(
                [hs["lat"], hs["lon"]],
                radius=150,
                color=hs["colour"],
                fill=True,
                fill_opacity=0.2,
                popup=f"{hs['risk_level']}: {hs['count']} reports",
                tooltip=f"{hs['risk_level']} ({hs['count']} reports)",
            ).add_to(m)

# Display the map
st_folium(m, use_container_width=True, height=500)

# ============================================================
# TOP PROBLEM LOCATIONS
# ============================================================
st.markdown("### 📍 Top Problem Locations")
st.markdown("Intersections and areas with the most obstruction reports.")

location_counts = df["location_name"].value_counts().head(10).reset_index()
location_counts.columns = ["Location", "Report Count"]

if not location_counts.empty:
    fig_locations = px.bar(
        location_counts,
        x="Report Count",
        y="Location",
        orientation="h",
        color="Report Count",
        color_continuous_scale=["#bae6fd", "#f59e0b", "#ef4444"],
    )
    fig_locations.update_layout(
        height=350,
        margin=dict(t=10, b=10),
        yaxis=dict(autorange="reversed"),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_locations, use_container_width=True)

# ============================================================
# OBSTRUCTION TYPE DISTRIBUTION
# ============================================================
st.markdown("### 📊 Obstruction Type Distribution")
st.markdown("Breakdown of what kinds of obstructions are being reported.")

type_counts = df["category"].value_counts().reset_index()
type_counts.columns = ["Obstruction Type", "Count"]

if not type_counts.empty:
    fig_types = px.pie(
        type_counts,
        names="Obstruction Type",
        values="Count",
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.4,
    )
    fig_types.update_traces(textinfo="label+percent", textposition="outside")
    fig_types.update_layout(height=350, margin=dict(t=10, b=10), showlegend=False)
    st.plotly_chart(fig_types, use_container_width=True)

# ============================================================
# HOTSPOT SUMMARY TABLE
# ============================================================
st.markdown("### 📋 Hotspot Summary Table")
hotspots = calculate_hotspots(reports)
if not hotspots.empty:
    display_df = hotspots[["lat", "lon", "count", "risk_level", "description", "types"]].copy()
    display_df.columns = ["Latitude", "Longitude", "Reports", "Risk Level", "Description", "Obstruction Types"]
    display_df = display_df.sort_values("Reports", ascending=False).reset_index(drop=True)
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.info("Hotspot data will appear once enough reports are submitted from nearby areas.")
