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
apply_page_config("ScootClear - Community Impact")
apply_custom_css()
show_top_navigation("Community Impact")

st.markdown("## Community Impact")
st.markdown("ScootClear is designed for the people who need safe sidewalks most.")

# ============================================================
# WHO WE SERVE
# ============================================================
st.markdown("""
<div class="dark-section" style="
    background: #0a1628;
    border-radius: 12px;
    padding: 24px;
    margin: 15px 0;
">
    <h4 style="color:#06d6a0; text-transform:uppercase; font-size:0.75rem;
        letter-spacing:2px; margin-bottom:4px;">Accessibility Impact</h4>
    <h3 style="margin-top:0;">Designed for the people who need safe sidewalks most</h3>
    <p style="color:#94a3b8; font-size:0.9rem;">
        ScootClear is built around public safety, inclusive mobility, and
        equitable access to city spaces. Our community includes:
    </p>
    <div style="margin-top: 15px;">
        <span style="display:inline-block; background:rgba(255,255,255,0.08);
            border:1px solid rgba(255,255,255,0.15); border-radius:6px;
            padding:6px 14px; margin:4px; font-size:0.85rem;">Wheelchair users</span>
        <span style="display:inline-block; background:rgba(255,255,255,0.08);
            border:1px solid rgba(255,255,255,0.15); border-radius:6px;
            padding:6px 14px; margin:4px; font-size:0.85rem;">Seniors</span>
        <span style="display:inline-block; background:rgba(255,255,255,0.08);
            border:1px solid rgba(255,255,255,0.15); border-radius:6px;
            padding:6px 14px; margin:4px; font-size:0.85rem;">Parents with strollers</span>
        <span style="display:inline-block; background:rgba(255,255,255,0.08);
            border:1px solid rgba(255,255,255,0.15); border-radius:6px;
            padding:6px 14px; margin:4px; font-size:0.85rem;">Visually impaired pedestrians</span>
        <span style="display:inline-block; background:rgba(255,255,255,0.08);
            border:1px solid rgba(255,255,255,0.15); border-radius:6px;
            padding:6px 14px; margin:4px; font-size:0.85rem;">People with spinal cord injuries</span>
        <span style="display:inline-block; background:rgba(255,255,255,0.08);
            border:1px solid rgba(255,255,255,0.15); border-radius:6px;
            padding:6px 14px; margin:4px; font-size:0.85rem;">Mobility device users</span>
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
        <strong>The Problem</strong><br>
        Shared e-scooters, garbage bins, construction barriers, and signboards
        are frequently left blocking sidewalks, curb cuts, and accessible routes
        across the GTA. This creates major barriers for people with disabilities.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <strong>Time Impact</strong><br>
        When a sidewalk is blocked, wheelchair users have to backtrack and find
        an alternate route — which can be very time-consuming and frustrating.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="danger-card">
        <strong>Safety Risk</strong><br>
        Sometimes there is no alternate route, forcing wheelchair users to go
        down a curb, which is dangerous and can cause falls or injury.
        <br><br>
        <em>— Feedback from Spinal Cord Injury Ontario</em>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warning-card">
        <strong>Construction Zones</strong><br>
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
st.markdown("### Impact Metrics")

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
    st.info("Impact metrics will appear once reports are submitted.")
# """, unsafe_allow_html=True)
