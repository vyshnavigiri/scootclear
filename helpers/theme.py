# ============================================================
# theme.py
# Shared styling for the whole app.
# This keeps all the CSS in one place so every page looks
# consistent and we only have to change colours here.
# ============================================================

import streamlit as st


def apply_page_config(title="ScootClear"):
    """Set up the page with our custom title and layout."""
    st.set_page_config(
        page_title=title,
        layout="wide",
        initial_sidebar_state="collapsed",
    )


def apply_custom_css():
    """Apply the light blue theme CSS to the page."""
    st.markdown("""
    <style>
        /* --- Hide the default Streamlit sidebar nav --- */
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stSidebarCollapsedControl"] { display: none; }
        section[data-testid="stSidebar"] { display: none; }

        /* --- Page background --- */
        .stApp {
            background-color: #f0f7ff;
        }
        .block-container {
            max-width: 1100px;
            padding-top: 0.5rem;
        }

        /* ==============================================
           FIX: Force dark text on ALL Streamlit elements
           This prevents invisible text when the user's
           device defaults to dark mode.
           ============================================== */

        /* All headings */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
            color: #1e293b !important;
        }

        /* All body text, paragraphs, spans, labels */
        .stApp p, .stApp span, .stApp label, .stApp div {
            color: #1e293b;
        }

        /* Streamlit markdown text */
        .stApp .stMarkdown, .stApp .stMarkdown p,
        .stApp [data-testid="stMarkdownContainer"],
        .stApp [data-testid="stMarkdownContainer"] p,
        .stApp [data-testid="stMarkdownContainer"] span,
        .stApp [data-testid="stMarkdownContainer"] li,
        .stApp [data-testid="stMarkdownContainer"] strong,
        .stApp [data-testid="stMarkdownContainer"] em {
            color: #1e293b !important;
        }

        /* Streamlit form labels and input labels */
        .stApp .stTextInput label,
        .stApp .stTextArea label,
        .stApp .stSelectbox label,
        .stApp .stNumberInput label,
        .stApp .stFileUploader label,
        .stApp [data-testid="stWidgetLabel"],
        .stApp [data-testid="stWidgetLabel"] p {
            color: #1e293b !important;
        }

        /* Streamlit captions and help text */
        .stApp .stCaption, .stApp small {
            color: #64748b !important;
        }

        /* Streamlit selectbox, text input, number input text */
        .stApp input, .stApp textarea, .stApp select,
        .stApp [data-baseweb="select"] span,
        .stApp [data-baseweb="input"] input,
        .stApp [data-baseweb="textarea"] textarea {
            color: #1e293b !important;
        }

        /* Streamlit toggle labels */
        .stApp [data-testid="stCheckbox"] label span,
        .stApp .stToggle label span {
            color: #1e293b !important;
        }

        /* Streamlit info, warning, error, success boxes */
        .stApp .stAlert p, .stApp .stAlert span {
            color: #1e293b !important;
        }

        /* Streamlit dataframe text */
        .stApp .stDataFrame {
            color: #1e293b;
        }

        /* Streamlit blockquote text */
        .stApp blockquote, .stApp blockquote p {
            color: #ffffff !important;
        }

        /* Streamlit tab labels */
        .stApp .stTabs [data-baseweb="tab"] {
            color: #1e293b !important;
        }

        /* File uploader text */
        .stApp [data-testid="stFileUploader"] div,
        .stApp [data-testid="stFileUploader"] span,
        .stApp [data-testid="stFileUploader"] small,
        .stApp [data-testid="stFileUploaderDropzone"] div,
        .stApp [data-testid="stFileUploaderDropzone"] span {
            color: #1e293b !important;
        }

        /* EXCEPTIONS: Keep light text inside dark-background sections */
        .top-nav, .top-nav * { color: #ffffff; }
        .top-nav .brand { color: #06d6a0 !important; }
        .top-nav .brand small { color: #64748b !important; }
        .nav-links a { color: #ffffff !important; }
        .nav-links a.active { color: #0a1628 !important; }
        .nav-links a.report-btn { color: #0a1628 !important; }

        .impact-section, .impact-section * { color: #ffffff !important; }
        .impact-section h4 { color: #06d6a0 !important; }
        .impact-section h3 { color: #ffffff !important; }
        .impact-section p { color: #94a3b8 !important; }
        .tag { color: #ffffff !important; }
        .muni-item { color: #ffffff !important; }

        /* === END OF TEXT FIX === */

        /* --- Top navigation bar --- */
        .top-nav {
            background: linear-gradient(135deg, #0a1628 0%, #0f2744 100%);
            padding: 12px 24px;
            border-radius: 0 0 12px 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 8px;
        }
        .top-nav .brand {
            font-size: 1.4rem;
            font-weight: 800;
        }
        .top-nav .brand small {
            font-size: 0.65rem;
            display: block;
            font-weight: 400;
        }
        .nav-links {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            align-items: center;
        }
        .nav-links a {
            text-decoration: none;
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 0.85rem;
            transition: background 0.2s;
        }
        .nav-links a:hover {
            background: rgba(255,255,255,0.1);
        }
        .nav-links a.active {
            background: #06d6a0;
            font-weight: 600;
        }
        .nav-links a.report-btn {
            background: #06d6a0;
            font-weight: 600;
            border-radius: 20px;
            padding: 6px 18px;
        }

        /* --- Info cards --- */
        .info-card {
            background: #e8f4fd;
            border-left: 4px solid #0d6efd;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 10px;
            color: #1e293b !important;
        }
        .info-card * { color: #1e293b !important; }

        .warning-card {
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 10px;
            color: #1e293b !important;
        }
        .warning-card * { color: #1e293b !important; }

        .danger-card {
            background: #fef2f2;
            border-left: 4px solid #ef4444;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 10px;
            color: #1e293b !important;
        }
        .danger-card * { color: #1e293b !important; }

        .success-card {
            background: #d1fae5;
            border-left: 4px solid #198754;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 10px;
            color: #1e293b !important;
        }
        .success-card * { color: #1e293b !important; }

        /* --- Stat boxes on landing page --- */
        .stat-row {
            display: flex;
            gap: 15px;
            margin: 15px 0;
        }
        .stat-box {
            flex: 1;
            text-align: center;
            padding: 18px 10px;
            background: #ffffff;
            border-radius: 12px;
            border: 1px solid #bae6fd;
        }
        .stat-box .number {
            font-size: 2rem;
            font-weight: 800;
            color: #0d6efd !important;
        }
        .stat-box .label {
            font-size: 0.8rem;
            color: #64748b !important;
            margin-top: 2px;
        }

        /* --- Feature cards on landing page --- */
        .feature-row {
            display: flex;
            gap: 15px;
            margin: 20px 0;
        }
        .feature-card {
            flex: 1;
            background: #ffffff;
            border: 1px solid #bae6fd;
            border-radius: 12px;
            padding: 20px;
        }
        .feature-card h4 {
            color: #0a1628 !important;
            margin-top: 0;
        }
        .feature-card p {
            color: #64748b !important;
            font-size: 0.9rem;
        }

        /* --- Impact section (dark background - keep light text) --- */
        .impact-section {
            background: #0a1628;
            border-radius: 12px;
            padding: 24px;
            margin: 15px 0;
        }
        .impact-section h4 {
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 2px;
            margin-bottom: 4px;
        }
        .impact-section h3 {
            margin-top: 0;
        }
        .impact-section p {
            font-size: 0.9rem;
        }
        .tag {
            display: inline-block;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 6px;
            padding: 6px 14px;
            margin: 4px;
            font-size: 0.85rem;
        }

        /* --- Municipality list items (inside dark section) --- */
        .muni-item {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            padding: 10px 16px;
            margin-bottom: 8px;
            font-size: 0.9rem;
        }

        /* --- Score display --- */
        .score-display {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 12px 16px;
            background: #ffffff;
            border-radius: 10px;
            border: 1px solid #bae6fd;
            margin: 10px 0;
        }
        .score-display * { color: #1e293b !important; }
        .score-number {
            font-size: 2.2rem;
            font-weight: 800;
            line-height: 1;
        }

        /* --- Upcoming badge --- */
        .upcoming-badge {
            background: linear-gradient(135deg, #e0f2fe, #bae6fd);
            border: 1px solid #7dd3fc;
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            margin: 15px 0;
        }
        .upcoming-badge * { color: #1e293b !important; }
        .upcoming-badge h2 { color: #0369a1 !important; }
    </style>
    """, unsafe_allow_html=True)


def show_top_navigation(current_page="Home"):
    """
    Display the top navigation bar.
    current_page should be one of: Home, Report Issue, Hotspot Map,
    Re-Routing Alerts, Community Impact, For Cities
    """
    # Build nav links - mark the current page as "active"
    pages = {
        "Home": "/",
        "Report Issue": "/Report_Issue",
        "Hotspot Map": "/Hotspot_Map",
        "Re-Routing Alerts": "/Re-Routing_Alerts",
        "Community Impact": "/Community_Impact",
        "For Cities": "/For_Cities",
    }

    links_html = ""
    for name, url in pages.items():
        if name == current_page:
            css_class = "active"
        else:
            css_class = ""
        links_html += f'<a href="{url}" class="{css_class}">{name}</a> '

    # The "Report Now" button on the right
    report_link = '<a href="/Report_Issue" class="report-btn">Report Now</a>'

    st.markdown(f"""
    <div class="top-nav">
        <div class="brand">
            ScootClear
            <small>AI-powered sidewalk accessibility platform</small>
        </div>
        <div class="nav-links">
            {links_html}
            {report_link}
        </div>
    </div>
    """, unsafe_allow_html=True)
