# ============================================================
# 6_Report_History.py — Report History
# Browse all submitted reports with filters.
# Time period limited to: Last 7 Days, 30 Days, 3 Months.
# Report cards show: Type, Confidence, Location, Time,
# Authenticity Score, Description. (No reporter name, no export.)
# ============================================================

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from helpers.theme import apply_page_config, apply_custom_css, show_top_navigation
from helpers.file_storage import load_all_reports

# --- Page setup ---
apply_page_config("ScootClear — Report History")
apply_custom_css()
show_top_navigation("Home")

st.markdown("## 📜 Report History")
st.markdown("Browse all submitted obstruction reports.")

# --- Load data ---
reports = load_all_reports()

if not reports:
    st.info("📜 No reports yet! Submit one on the Report Issue page.")
    st.stop()

df = pd.DataFrame(reports)
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# ============================================================
# FILTERS
# ============================================================
col1, col2, col3 = st.columns(3)

with col1:
    # Category filter
    all_categories = ["All"] + sorted(df["category"].unique().tolist())
    selected_category = st.selectbox("Filter by Type", all_categories)

with col2:
    # Time period filter (limited to 3 months max)
    time_filter = st.selectbox(
        "Time Period",
        ["Last 7 Days", "Last 30 Days", "Last 3 Months"],
        index=2,
    )

with col3:
    # Sort order
    sort_order = st.selectbox("Sort by", ["Newest First", "Oldest First"])

# --- Apply filters ---
now = datetime.now()
if time_filter == "Last 7 Days":
    cutoff = now - timedelta(days=7)
elif time_filter == "Last 30 Days":
    cutoff = now - timedelta(days=30)
else:
    cutoff = now - timedelta(days=90)

filtered = df[df["timestamp"] >= cutoff].copy()

if selected_category != "All":
    filtered = filtered[filtered["category"] == selected_category]

if sort_order == "Newest First":
    filtered = filtered.sort_values("timestamp", ascending=False)
else:
    filtered = filtered.sort_values("timestamp", ascending=True)

st.markdown(f"**Showing {len(filtered)} of {len(df)} total reports**")
st.markdown("---")

# ============================================================
# REPORT CARDS
# ============================================================
# Icons for each obstruction type
type_icons = {
    "Construction": "🚧",
    "Garbage / Recycling Bins": "🗑️",
    "E-Scooter": "🛴",
    "Bicycle / E-Bike": "🚲",
    "Signboard": "🪧",
    "Other": "⚠️",
}

for _, row in filtered.iterrows():
    category = row.get("category", "Unknown")
    icon = type_icons.get(category, "⚠️")
    auth_score = row.get("authenticity_score", "N/A")
    confidence = row.get("confidence", "N/A")
    conf_pct = row.get("confidence_percent", "")
    timestamp = str(row.get("timestamp", ""))[:19]
    location = row.get("location_name", row.get("street_intersection", "N/A"))
    postal = row.get("postal_code", "")
    description = row.get("description", "")

    # Colour for authenticity score
    if isinstance(auth_score, (int, float)):
        if auth_score >= 80:
            score_colour = "#198754"
        elif auth_score >= 50:
            score_colour = "#f59e0b"
        else:
            score_colour = "#dc3545"
    else:
        score_colour = "#64748b"

    # Colour for confidence
    conf_colours = {"High": "#198754", "Medium": "#f59e0b", "Low": "#dc3545"}
    conf_colour = conf_colours.get(confidence, "#64748b")

    # Display the report card
    with st.container():
        c1, c2, c3 = st.columns([0.4, 3, 1.2])

        with c1:
            st.markdown(
                f"<div style='font-size:2.2rem; text-align:center; padding-top:5px;'>{icon}</div>",
                unsafe_allow_html=True,
            )

        with c2:
            location_display = f"**{category}** — {location}"
            if postal:
                location_display += f" ({postal})"
            st.markdown(location_display)
            st.caption(f"🕐 {timestamp}")
            if description:
                st.markdown(f"> {description[:150]}")

        with c3:
            st.markdown(f"""
            <div style="text-align:center; padding:8px; background:#fff;
                        border-radius:8px; border:1px solid #bae6fd;">
                <div style="font-size:1.3rem; font-weight:700; color:{score_colour};">{auth_score}</div>
                <div style="font-size:0.7rem; color:#94a3b8;">Auth Score</div>
                <div style="font-size:0.8rem; margin-top:4px; color:{conf_colour}; font-weight:600;">
                    {confidence} {f'({conf_pct}%)' if conf_pct else ''}
                </div>
                <div style="font-size:0.65rem; color:#94a3b8;">Confidence</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
