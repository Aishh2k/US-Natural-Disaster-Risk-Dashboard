# US Natural Disaster Risk Dashboard

This project visualizes and analyzes natural disaster trends across the United States. It integrates NOAA historical disaster data, FEMA National Risk Index metrics, and ML-based projections for 2025 to provide a clearer view of climate-related risks for the general public, researchers, and decision-makers.

The dashboard features a colored heat map of all US states, allowing users to switch between historical data, future predictions, and socio-economic risk indicators. Users can filter disasters by event type, explore state-wise and year-wise statistics, and use interactive charts to better understand the impact of each disaster. An integrated AI Assistant provides context-aware answers about the projected data, risk patterns, and mitigation guidance.

<img width="1470" height="801" alt="image" src="https://github.com/user-attachments/assets/64de9ad2-2439-4a2b-8263-a7b60d96d95e" />

## Features

- Interactive US state map with hover and click behavior
- Historical NOAA disaster losses and fatalities from 2000-2024
- 2025 predicted disaster trends by state
- FEMA National Risk Index socio-economic risk view
- Event type filters for historical disaster analysis
- State-level sidebar with losses, fatalities, risk metrics, and safety tips
- Charts for monthly trends, event distributions, historical context, risk quadrants, social vulnerability, and risk efficiency
- AI Assistant button in the header for asking questions about dashboard data

## Requirements

- Python 3.8+
- pip
- A modern web browser
- Optional: a Groq API key for the AI Assistant

Frontend libraries are loaded from CDNs:

- Leaflet
- Chart.js
- Plotly.js

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Dashboard

Start the local server:

```bash
python serve_dashboard.py
```

Open the dashboard at:

```text
http://localhost:8000
```

## AI Assistant Setup

The dashboard works without the AI Assistant, but chat responses require a Groq API key.

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_api_key_here
```

Then start or restart the server:

```bash
python serve_dashboard.py
```

If `GROQ_API_KEY` is not set in `.env`, the dashboard will still load, but chatbot requests will return an API key error.


## How to Use

Use the Dataset dropdown to switch between:

- Historical Loss Database (NOAA)
- Predictions in next 12 months
- FEMA National Risk Index - Socio-Economic

Map behavior:

- Hover over a state to update the sidebar and charts for that state.
- Click a state to lock the sidebar and charts to that state.
- Click the same state again to unlock it and return to hover-based updates.

Historical view controls:

- Use the year slider to select a year from 2000-2024.
- Toggle between Economic and Human-centered NOAA metrics.
- Filter visible disaster event types from the Event Filters panel.

## Tech Stack

- Python local HTTP server
- Vanilla JavaScript
- HTML/CSS
- Leaflet for the map
- Chart.js and Plotly for visualizations
- Groq API for AI assistant responses
- pandas, scikit-learn, XGBoost, SHAP, NumPy, Matplotlib, and dbfread for data and ML workflows
