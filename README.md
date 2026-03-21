# ScootClear - Community Sidewalk Accessibility Reporter

A web app that helps make GTA sidewalks accessible for everyone.
Built for the **Technovation Girls 2026** challenge.

## What does this app do?

- **Report obstructions** — Upload photos of blocked sidewalks with location info
- **AI validates photos** — Checks if the photo is genuine (not fake/AI-generated)
- **AI detects obstructions** — Figures out what type of obstruction is in the photo
- **Hotspot map** — Shows where obstructions happen most on an interactive map
- **Safety dashboard** — Charts and analytics for city planners
- **Report history** — Browse and filter all submitted reports


## Project structure

```
scootclear2/
├── Home.py                      <-- Landing page (main file to run)
├── requirements.txt             <-- Python packages needed
├── seed_data.py                 <-- Creates sample data for demo
├── helpers/                     <-- Helper modules
│   ├── __init__.py
│   ├── file_storage.py          <-- Reads/writes reports to JSON file
│   ├── image_checks.py          <-- Checks if photos are genuine
│   ├── obstruction_detector.py  <-- Detects obstruction type in photos
│   ├── hotspot_finder.py        <-- Finds hotspot areas
│   └── theme.py                 <-- Styling and navigation
├── pages/                       <-- App pages
│   ├── 1_Report_Issue.py        <-- Report form + AI pipeline
│   ├── 2_Hotspot_Map.py         <-- Interactive map
│   ├── 3_Re-Routing_Alerts.py   <-- Coming soon page
│   ├── 4_Community_Impact.py    <-- Who we serve
│   ├── 5_For_Cities.py          <-- Safety dashboard
│   └── 6_Report_History.py      <-- Browse reports
└── data/
    └── reports.json             <-- Our "database" (auto-created)
```


## How to set up and run

### Step 1: Open a terminal

On Windows, open **PowerShell**. On Mac, open **Terminal**.

### Step 2: Go to the project folder

```
cd path\to\scootclear2
```

### Step 3: Create a virtual environment

**Windows:**
```
py -m venv venv
.\venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install packages

```
py -m pip install -r requirements.txt
```

### Step 5: Create sample data (optional but recommended)

```
py seed_data.py
```

### Step 6: Run the app!

```
py -m streamlit run Home.py
```

The app will open in your browser at **http://localhost:8501**


## About the "database"

This project uses a **JSON file** (`data/reports.json`) instead of a real database.
This is simpler and works fine for a prototype. Every report gets saved as a
JSON object in this file, and we read from it whenever we need data.

For a production app, you would use a real database like **SQLite** (still a file,
but faster) or **PostgreSQL** (a proper database server).


## Credits

- Built for the **Technovation Girls 2026** challenge
- Feedback from **Spinal Cord Injury Ontario** shaped the re-routing alerts concept
- Built for the **Greater Toronto Area** community
