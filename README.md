# FC Performance Insights

### Overview

FC Performance Insights is a Streamlit application to track, analyze, and visualize the physical performance of football players across matches and training. It helps coaches and performance staff monitor GPS metrics, physical capabilities, and recovery status to support evidence-based decisions.


### Key Pages

- **Home**: Intro and high-level guidance to the platform.
- **Games & Training Performance**: Explore GPS-based performance metrics for matches and training (distance, speed, intensity, HR zones, clustering).
- **Physical Capabilities Analysis**: Analyze test performance, benchmarks, movements (jump/sprint/agility/etc.), and development trends.
- **Recovery Analysis**: Monitor recovery status over time (sleep, wellness, nutrition, etc.), composite scores, and load–recovery interactions.


### Features

- **Injury/availability context**: View metrics that relate to availability and load exposure.
- **Physical development**: Benchmark percentiles by test/movement, trends, and recent results.
- **Recovery analytics**: Category scores, completeness heatmaps, pre/post-match snapshots, and load vs recovery dynamics.
- **Player profile**: Nationality, age, position, image, and season selector.


### Quickstart

1) Install dependencies
```bash
pip install -r requirements.txt
```

2) Run the app
```bash
streamlit run main.py
```

3) Open the Streamlit URL printed in your terminal (usually `http://localhost:8501`).


### Recommended Environment

- Python 3.10+ (virtual environment recommended)
- Streamlit `1.43.2` (pinned in `requirements.txt`)
- Plotly `5.13.1`

Create and activate a virtual environment (optional but recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows PowerShell
```


### Data Requirements and Structure

The app expects a small metadata file and per-player folders with CSVs.

- `data/players.json`: registry of players available in the app
- `data/players_data/<player_id>/`: per-player assets and datasets
  - `picture_id.jpeg`: headshot used in the sidebar
  - `CFC GPS Data.csv`: GPS data (training + matches)
  - `CFC Physical Capability Data.csv`: test results and benchmark percentiles
  - `CFC Recovery status Data.csv`: recovery questionnaire and composite metrics

Season filtering currently supports: `2023/2024`, `2024/2025`.


### Application Architecture

- `main.py`
  - Configures Streamlit, builds the sidebar (player/season selection), and routes to pages.
  - Loads `data/players.json` and surfaces player info and image.
- `pages/`
  - `gps_exploration.py`: KPIs for matches/trainings, radar charts, HR zones, load, clustering.
  - `physical_capabilities.py`: Benchmark trends, movement analysis, load vs expression, recent results.
  - `recovery_status.py`: Recovery scores over time, category breakdowns, weekly heatmaps, pre/post-match.
- `src/`
  - `data_preprocessing.py`: IO helpers for GPS, physical capabilities, and recovery datasets.
  - `gps_viz.py`, `physical_viz.py`, `recovery_viz.py`, `additional_viz.py`: Plotly/visual helpers and KPI computations.
- `images/`
  - Static assets (e.g., `chelsea.png`).
- `data/`
  - Player registry and per-player data folders.


### Usage Tips

- Use the sidebar to choose the season and player. The selected state is stored in Streamlit session state.
- Tabs within each page reveal different perspectives of the same dataset (KPIs, trends, distributions, clustering, etc.).
- Hover on Plotly figures to see interactive tooltips and export options.
