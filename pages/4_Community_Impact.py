# ============================================================
# 4_Community_Impact.py — Community Impact
# Shows who the app is designed for, accessibility information,
# and the impact metrics of ScootClear.
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

from helpers.theme import apply_page_config, apply_custom_css, show_top_navigation
from helpers.file_storage import load_all_reports

# --- Page setup ---
apply_page_config("ScootClear — Community Impact")
apply_custom_css()
show_top_navigation("Community Impact")

st.markdown("## ♿ Community Impact")
st.markdown("ScootClear is designed for the people who need safe sidewalks most.")

# ============================================================
# WHO WE SERVE
# ============================================================
st.markdown("""
<div class="impact-section">
    <h4>Accessibility Impact</h4>
    <h3>Designed for the people who need safe sidewalks most</h3>
    <p>
        ScootClear is built around public safety, inclusive mobility, and
        equitable access to city spaces. Our community includes:
    </p>
    <div style="margin-top: 15px;">
        <span class="tag">♿ Wheelchair users</span>
        <span class="tag">👴 Seniors</span>
        <span class="tag">👶 Parents with strollers</span>
        <span class="tag">🦯 Visually impaired pedestrians</span>
        <span class="tag">🧑‍🦽 People with spinal cord injuries</span>
        <span class="tag">🦿 Mobility device users</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# WHY THIS MATTERS
# ============================================================
st.markdown("### Why sidewalk obstructions matter")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
        <strong>🚧 The Problem</strong><br>
        Shared e-scooters, garbage bins, construction barriers, and signboards 
        are frequently left blocking sidewalks, curb cuts, and accessible routes 
        across the GTA. This creates major barriers for people with disabilities.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <strong>⏱️ Time Impact</strong><br>
        When a sidewalk is blocked, wheelchair users have to backtrack and find 
        an alternate route — which can be very time-consuming and frustrating.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="danger-card">
        <strong>⚠️ Safety Risk</strong><br>
        Sometimes there is no alternate route, forcing wheelchair users to go 
        down a curb — which is dangerous and can cause falls or injury.
        <br><br>
        <em>— Feedback from Spinal Cord Injury Ontario</em>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warning-card">
        <strong>🏗️ Construction Zones</strong><br>
        Construction is one of the most common causes of sidewalk obstructions, 
        especially in downtown Toronto where construction is everywhere.
        <br><br>
        <em>— Feedback from Spinal Cord Injury Ontario</em>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# IMPACT METRICS
# ============================================================
st.markdown("---")
st.markdown("### 📈 Impact Metrics")

reports = load_all_reports()

if reports:
    df = pd.DataFrame(reports)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    total = len(df)
    categories = df["category"].nunique()
    locations = df["location_name"].nunique()
    recent = len(df[df["timestamp"] >= datetime.now() - timedelta(days=30)])

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-box">
            <div class="number">{total}</div>
            <div class="label">Total Reports</div>
        </div>
        <div class="stat-box">
            <div class="number">{categories}</div>
            <div class="label">Obstruction Types Reported</div>
        </div>
        <div class="stat-box">
            <div class="number">{locations}</div>
            <div class="label">Unique Locations</div>
        </div>
        <div class="stat-box">
            <div class="number">{recent}</div>
            <div class="label">Reports (Last 30 Days)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Obstruction type chart
    type_counts = df["category"].value_counts().reset_index()
    type_counts.columns = ["Type", "Count"]
    fig = px.bar(type_counts, x="Type", y="Count",
                 color_discrete_sequence=["#0ea5e9"])
    fig.update_layout(height=300, margin=dict(t=10, b=10),
                      xaxis_title="Obstruction Type", yaxis_title="Number of Reports")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("📊 Impact metrics will appear once reports are submitted.")

# ============================================================
# FUTURE VISION
# ============================================================
st.markdown("---")
st.markdown("### 🔮 Future Vision")
st.markdown("""
<div class="info-card">
    <strong>Google Maps Integration</strong><br>
    We hope to integrate ScootClear with Google Maps so that obstruction 
    reports show up when someone looks up a route — just like how transit 
    disruptions currently appear. This would help reach the most people and 
    make the biggest impact on sidewalk accessibility.
    <br><br>
    <em>This was recommended by Spinal Cord Injury Ontario as the most 
    effective way to get mass adoption.</em>
</div>
""", unsafe_allow_html=True)
