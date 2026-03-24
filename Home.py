# ============================================================
# Home.py — ScootClear Landing Page
# This is the main page users see when they open the app.
# It shows stats, features, accessibility info, and links.
# ============================================================

import streamlit as st
from helpers.theme import apply_page_config, apply_custom_css, show_top_navigation
from helpers.file_storage import load_all_reports
from helpers.hotspot_finder import calculate_hotspots

# Auto-seed sample data if the database is empty
from helpers.file_storage import load_all_reports
if len(load_all_reports()) == 0:
    import subprocess
    subprocess.run(["python", "seed_data.py"])
    
# --- Page setup ---
apply_page_config("ScootClear — Home")
apply_custom_css()
show_top_navigation("Home")

# --- Load report data for stats ---
reports = load_all_reports()
total_reports = len(reports)
hotspots_df = calculate_hotspots(reports)
hotspot_count = len(hotspots_df) if not hotspots_df.empty else 0
unique_locations = len(set(
    r.get("location_name", "") for r in reports if r.get("location_name")
))

# ============================================================
# HERO SECTION
# ============================================================
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("""
    <div style="
        background: #e0f2fe;
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        color: #0369a1;
        margin-bottom: 10px;
    ">
        Civic Tech for Safer, More Accessible Sidewalks
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style="font-size: 2.2rem; color: #0a1628; line-height: 1.2; margin-bottom: 10px;">
        Making GTA sidewalks<br>accessible for
        <span style="color: #06d6a0;">everyone</span>
    </h1>
    <p style="color: #64748b; font-size: 1rem; margin-bottom: 20px;">
        Help cities like Mississauga identify sidewalk obstructions,
        protect accessible routes, and respond faster to unsafe scooter parking.
    </p>
    """, unsafe_allow_html=True)

    # CTA Buttons
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        st.page_link("pages/2_Hotspot_Map.py", label="View Hotspot Map", icon="🗺️")
    with btn_col2:
        st.page_link("pages/1_Report_Issue.py", label="Report an Issue", icon="📋")

with col_right:
    # Live Safety Overview panel
    st.markdown(f"""
    <div class="dark-section" style="
        background: #0a1628;
        border-radius: 12px;
        padding: 20px;
    ">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <div>
                <strong style="font-size:1rem;">Live Safety Overview</strong><br>
                <span style="font-size:0.75rem; color:#94a3b8;">
                    Downtown Mississauga · Updated today
                </span>
            </div>
            <span style="
                background:#065f46; color:#06d6a0;
                padding:3px 10px; border-radius:12px; font-size:0.7rem;
            ">Active Monitoring</span>
        </div>
        <div style="display:flex; gap:10px; margin-bottom:15px;">
            <div style="flex:1; text-align:center; padding:10px; background:rgba(255,255,255,0.05); border-radius:8px;">
                <div style="font-size:1.5rem; font-weight:800; color:#06d6a0;">{total_reports}+</div>
                <div style="font-size:0.7rem; color:#94a3b8;">Reports Submitted</div>
            </div>
            <div style="flex:1; text-align:center; padding:10px; background:rgba(255,255,255,0.05); border-radius:8px;">
                <div style="font-size:1.5rem; font-weight:800; color:#0ea5e9;">{hotspot_count}</div>
                <div style="font-size:0.7rem; color:#94a3b8;">Hotspots Identified</div>
            </div>
            <div style="flex:1; text-align:center; padding:10px; background:rgba(255,255,255,0.05); border-radius:8px;">
                <div style="font-size:1.5rem; font-weight:800; color:#f59e0b;">{unique_locations}</div>
                <div style="font-size:0.7rem; color:#94a3b8;">Locations Monitored</div>
            </div>
        </div>
        <div style="display:flex; gap:10px;">
            <div style="flex:1; background:rgba(255,255,255,0.05); border-radius:8px; padding:12px;">
                <strong style="font-size:0.8rem;">Hotspot Preview</strong><br>
                <span style="font-size:0.7rem; color:#94a3b8;">
                    Heatmap highlights recurring obstruction zones
                </span>
            </div>
            <div style="flex:1; background:rgba(255,255,255,0.05); border-radius:8px; padding:12px;">
                <strong style="font-size:0.8rem;">AI Detection</strong><br>
                <span style="font-size:0.7rem; color:#94a3b8;">
                    Analyses photos and detects obstruction types with confidence scores
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# FEATURES SECTION
# ============================================================
st.markdown("""
<div class="feature-row">
    <div class="feature-card">
        <h4>Community Reporting</h4>
        <p>Residents can upload a photo, add a location, and describe
        sidewalk obstructions in seconds.</p>
    </div>
    <div class="feature-card">
        <h4>AI Validation</h4>
        <p>Images are checked to detect obstructions, assess
        blockage severity, and verify report quality.</p>
    </div>
    <div class="feature-card">
        <h4>Hotspot Insights</h4>
        <p>Cities can identify recurring problem zones and
        make smarter accessibility and parking decisions.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# ACCESSIBILITY IMPACT + FOR MUNICIPALITIES
# ============================================================
col_impact, col_muni = st.columns(2)

with col_impact:
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
        <p style="color:#94a3b8; font-size:0.9rem;">ScootClear is built around public safety, inclusive mobility,
        and equitable access to city spaces.</p>
        <div style="margin-top: 12px;">
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
                padding:6px 14px; margin:4px; font-size:0.85rem;">Spinal cord injury</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_muni:
    st.markdown("""
    <div class="dark-section" style="
        background: #0a1628;
        border-radius: 12px;
        padding: 24px;
        margin: 15px 0;
    ">
        <h4 style="color:#06d6a0; text-transform:uppercase; font-size:0.75rem;
            letter-spacing:2px; margin-bottom:4px;">For Municipalities</h4>
        <h3 style="margin-top:0;">Built to support city planning and community response</h3>
        <div style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1);
            border-radius:8px; padding:10px 16px; margin-bottom:8px; font-size:0.9rem;">
            Identify recurring sidewalk obstruction hotspots</div>
        <div style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1);
            border-radius:8px; padding:10px 16px; margin-bottom:8px; font-size:0.9rem;">
            Improve micromobility parking zone planning</div>
        <div style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1);
            border-radius:8px; padding:10px 16px; margin-bottom:8px; font-size:0.9rem;">
            Support bylaw enforcement and response prioritization</div>
        <div style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1);
            border-radius:8px; padding:10px 16px; margin-bottom:8px; font-size:0.9rem;">
            Strengthen accessibility-focused urban design decisions</div>
    </div>
    """, unsafe_allow_html=True)
