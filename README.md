# CFC_Vizathon

The Chelsea Dashboard is an interactive web application built with Dash and Plotly to visualize metrics for Chelsea FC players. The dashboard provides multiple pages that allow you to explore a player's statistics over the current season, the link between the evolution of his training load, his load ratio and his injury history, as well as data linked to the player's recovery.

This work was carried out as part of the **CFC Performance Insights Vizathon**.
![image](https://github.com/user-attachments/assets/5f4ae088-87ee-435e-98e7-9ce51bb404ca)


## Features
### Overview
- **Player Informations**: Player's identity card with details (nationality, age, etc.).
- **Season Stats**:  Get a summary of the player's statistics for the current season, with certain characteristics depending on the position he occupies.
- **Donuts Charts**:  See an overview of player usage for the current season.
- **Last 5 matches**:  Get information on the player's recent dynamics, with his usage over the last 5 matches and his performances thanks to tooltips.

### Load Demand
- **Acute and Chronic Load (TRIMP)**: Visualizes a player's acute and chronic training load (7-day and 28-day load), calculated on the basis of cardiac data collected during matches and training sessions.
- **Availability**:  Get information on player status. Is he injured or available during a specific period?
- **Load Ratio (ACWR) & Injury Risk Zones**:  Visualizes the load ratio between acute and chronic load. Depending on the value of this ratio, you can obtain information on the potential risk of injury faced by the player.

### Recovery
- **Daily Recovery Metrics Evolution**: View line charts showing the evolution of recovery metrics (Subjective, Sleep, Soreness) on a daily basis.
- **Overall Recovery Heatmap**: Explore a heatmap displaying the overall recovery score (Emboss) aggregated by month and day.
- **Weekly Recovery Metrics Evolution**: See weekly trends of composite recovery metrics with an interactive dropdown to filter each metric.
- **Radar Chart Summary**: Display a radar chart summarizing average recovery values (e.g., Bio, Joint Range, Load Tolerance, Sleep, Soreness, Subjective) over the last 7 days. Values are color-coded (green for positive, red for negative) and include explicit '+' or '-' signs.

## Project Structure
```bash
CFC_Vizathon/
├── app.py                      # Main entry point, sets up the Dash app and its layout
├── data_loader.py              # Contains functions to load and process raw recovery data
├── components.py               # Contains functions to render various charts and components
├── constants.py                # Contains constants using in components (colors, font size, etc.)
├── gps_data_generator.py       # Contains functions to generate mocked data for GPS data
├── recovery_data_generator.py  # Contains functions to generate mocked data for recovery data
├── styles.py                   # Contains layout configuration
└── assets/                     # Static assets (CSS, fonts, etc.)
└── data/                       # Raw files used for the Dash constuction
```

## Customization

The dashboard is highly customizable:
- **Layout and Styling**: Easily adjust the position (`top`, `left`), size (`width` in vw, `height` in vh), and background colors.
- **Typography**: Customize font families, sizes, and colors for titles, axes, legends, and other text elements.
- **Color Schemes**: Specify colors for positive and negative values in charts, as well as for individual metrics.
- **Interactive Filters**: Use dropdown menus to filter data by season and to toggle the display of individual metric curves.

## How to Run

1. **Install Dependencies**:  
  Ensure you have Python installed along with the required libraries. You can install the dependencies using:
    ```bash
    pip install dash plotly pandas dash-bootstrap-components
    ```
    
    To install the required Python packages for this project, run:
    
    ```bash
    pip install -r requirements.txt
    ```

2. **Run the Application:**:  
  Execute the main app file:
    ```bash
    python app.py
    ```

The application should launch locally (usually at http://127.0.0.1:8050).

## Usage

**Navigation:**  
The dashboard is organized into multiple pages accessible via a tab bar.

**Filtering:**  
Use dropdown menus to filter data by season and select different players.

**Interactivity:**  
Interactive menus allow you to display specific metrics in the weekly charts and view detailed information in the radar and summary sections.

## License

This project is provided "as is" without warranty of any kind. You are free to use and modify the code for your own projects.
