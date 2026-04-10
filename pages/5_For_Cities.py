# ============================================================
# 5_For_Cities.py — For Cities (Safety Dashboard)
# This page is for municipal officials and city planners.
# It shows analytics: obstruction type distribution, reports
# over time, top locations, time-of-day patterns, confidence
# breakdown, and a hotspot risk table.
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from helpers.theme import apply_page_config, apply_custom_css, show_top_navigation
from helpers.file_storage import load_all_reports
from helpers.hotspot_finder import calculate_hotspots

# --- Page setup ---
apply_page_config("ScootClear - For Cities")
apply_custom_css()
show_top_navigation("For Cities")

st.markdown("## For Cities - Safety Dashboard")
st.markdown("Analytics and insights for municipal planning, bylaw enforcement, and urban design.")

# --- Load data ---
reports = load_all_reports()

if not reports:
    st.info("No data yet! Reports will appear here once they are submitted.")
    st.stop()

df = pd.DataFrame(reports)
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df["date"] = df["timestamp"].dt.date
df["hour"] = df["timestamp"].dt.hour

# ============================================================
# TIME PERIOD FILTER
# ============================================================
time_filter = st.selectbox(
    "Time Period",
    ["Last 7 Days", "Last 30 Days", "Last 3 Months"],
    index=1,
)

# Apply the time filter
now = datetime.now()
if time_filter == "Last 7 Days":
    cutoff = now - timedelta(days=7)
elif time_filter == "Last 30 Days":
    cutoff = now - timedelta(days=30)
else:
    cutoff = now - timedelta(days=90)

filtered_df = df[df["timestamp"] >= cutoff].copy()

if filtered_df.empty:
    st.warning(f"No reports found in the {time_filter.lower()} period.")
    st.stop()

# ============================================================
# SUMMARY METRICS
# ============================================================
total = len(filtered_df)
categories = filtered_df["category"].nunique()
locations = filtered_df["location_name"].nunique()

st.markdown(f"""
<div class="stat-row">
    <div class="stat-box">
        <div class="number">{total}</div>
        <div class="label">Reports ({time_filter})</div>
    </div>
    <div class="stat-box">
        <div class="number">{categories}</div>
        <div class="label">Obstruction Types</div>
    </div>
    <div class="stat-box">
        <div class="number">{locations}</div>
        <div class="label">Unique Locations</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# CHARTS
# ============================================================
col1, col2 = st.columns(2)

# --- Chart 1: Obstruction Type Distribution ---
with col1:
    st.markdown("#### Obstruction Type Distribution")
    type_counts = filtered_df["category"].value_counts().reset_index()
    type_counts.columns = ["Type", "Count"]
    fig1 = px.pie(type_counts, names="Type", values="Count",
                  color_discrete_sequence=px.colors.qualitative.Set2, hole=0.4)
    fig1.update_traces(textinfo="label+percent", textposition="outside")
    fig1.update_layout(height=320, margin=dict(t=10, b=10), showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

# --- Chart 2: Reports Over Time ---
with col2:
    st.markdown("#### Reports Over Time")
    daily = filtered_df.groupby("date").size().reset_index(name="Reports")
    fig2 = px.area(daily, x="date", y="Reports",
                   color_discrete_sequence=["#0ea5e9"])
    fig2.update_layout(height=320, margin=dict(t=10, b=10),
                       xaxis_title="Date", yaxis_title="Reports")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

# --- Chart 3: Top Problem Locations ---
with col3:
    st.markdown("#### Top Problem Locations")
    loc_counts = filtered_df["location_name"].value_counts().head(8).reset_index()
    loc_counts.columns = ["Location", "Reports"]
    fig3 = px.bar(loc_counts, x="Reports", y="Location", orientation="h",
                  color="Reports",
                  color_continuous_scale=["#bae6fd", "#f59e0b", "#ef4444"])
    fig3.update_layout(height=320, margin=dict(t=10, b=10),
                       yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)

# --- Chart 4: Reports by Time of Day ---
with col4:
    st.markdown("#### Reports by Time of Day")
    hourly = filtered_df.groupby("hour").size().reset_index(name="Reports")
    all_hours = pd.DataFrame({"hour": range(24)})
    hourly = all_hours.merge(hourly, on="hour", how="left").fillna(0)
    hourly["Reports"] = hourly["Reports"].astype(int)
    fig4 = px.bar(hourly, x="hour", y="Reports",
                  color_discrete_sequence=["#06d6a0"],
                  labels={"hour": "Hour of Day"})
    fig4.update_layout(height=320, margin=dict(t=10, b=10))
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ============================================================
# DETECTION CONFIDENCE BREAKDOWN
# ============================================================
st.markdown("#### Detection Confidence Breakdown")
st.markdown("How many reports had High, Medium, or Low confidence in the AI detection.")

if "confidence" in filtered_df.columns:
    conf_counts = filtered_df["confidence"].value_counts().reset_index()
    conf_counts.columns = ["Confidence Level", "Count"]

    colour_map = {"High": "#198754", "Medium": "#f59e0b", "Low": "#dc3545"}
    fig5 = px.bar(conf_counts, x="Confidence Level", y="Count",
                  color="Confidence Level",
                  color_discrete_map=colour_map)
    fig5.update_layout(height=280, margin=dict(t=10, b=10), showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)
else:
    st.info("Confidence data will appear as new reports are submitted.")

# ============================================================
# PHOTO AUTHENTICITY GAUGE
# ============================================================
st.markdown("#### Photo Authenticity Overview")

if "authenticity_score" in filtered_df.columns:
    avg_score = filtered_df["authenticity_score"].mean()
    fig6 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_score,
        title={"text": "Average Authenticity Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#0ea5e9"},
            "steps": [
                {"range": [0, 50], "color": "#fef2f2"},
                {"range": [50, 80], "color": "#fffbeb"},
                {"range": [80, 100], "color": "#d1fae5"},
            ],
        },
    ))
    fig6.update_layout(height=250, margin=dict(t=40, b=10))
    st.plotly_chart(fig6, use_container_width=True)

# ============================================================
# HOTSPOT RISK TABLE
# ============================================================
st.markdown("---")
st.markdown("#### Hotspot Risk Table")
st.markdown("Areas colour-coded by risk level based on report frequency.")

hotspots = calculate_hotspots(reports)
if not hotspots.empty:
    display_df = hotspots[["lat", "lon", "count", "risk_level", "description", "types"]].copy()
    display_df.columns = ["Latitude", "Longitude", "Reports", "Risk Level", "Description", "Obstruction Types"]
    display_df = display_df.sort_values("Reports", ascending=False).reset_index(drop=True)
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.info("Hotspot data will appear once enough reports are submitted from nearby areas.")
