# ============================================================
# file_storage.py
# This is our simple "database" using a JSON file.
# Instead of a real database like MySQL or PostgreSQL,
# we just save everything to a file called reports.json.
# This is fine for a school project or prototype!
# ============================================================

import json
import os
from datetime import datetime

# Where we store the reports file
DATA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
REPORTS_FILE = os.path.join(DATA_FOLDER, "reports.json")


def make_sure_data_folder_exists():
    """Create the data folder and reports file if they don't exist yet."""
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    if not os.path.exists(REPORTS_FILE):
        with open(REPORTS_FILE, "w") as f:
            json.dump([], f)


def load_all_reports():
    """Read all reports from the JSON file and return them as a list."""
    make_sure_data_folder_exists()
    try:
        with open(REPORTS_FILE, "r") as f:
            reports = json.load(f)
        return reports
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_new_report(report):
    """Add one new report to the JSON file."""
    make_sure_data_folder_exists()
    # Load existing reports
    all_reports = load_all_reports()
    # Add the new one
    all_reports.append(report)
    # Write everything back to the file
    with open(REPORTS_FILE, "w") as f:
        json.dump(all_reports, f, indent=2, default=str)


def clear_all_reports():
    """Delete all reports (for testing/admin)."""
    make_sure_data_folder_exists()
    with open(REPORTS_FILE, "w") as f:
        json.dump([], f)
