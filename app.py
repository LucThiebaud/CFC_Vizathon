import dash
from dash import html, dcc, Input, Output, ctx, ALL
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from styles import LAYOUT_STYLE
from components import *
from constants import *
from data_loader import *

# =============================================================================
# Initialize the Dash app
# =============================================================================

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.title = "CFC Performance Insights Vizathon LTH"
server = app.server

# =============================================================================
# Define the app layout
# =============================================================================

app.layout = html.Div(
    style=LAYOUT_STYLE,
    children=[
        dcc.Store(id="selected-tab", data=1),
        dcc.Store(id="selected-player", data=5),
        dcc.Store(id="selected-season", data="2024/2025"),
        get_header_background(),
        get_sidebar_background(),
        get_logo(),
        get_separation_line(),
        get_sidebar(),
        get_tab_bar(),
        get_page_content()
    ]
)

# =============================================================================
# Callbacks for Tab and Player Selection
# =============================================================================

@app.callback(
    Output("selected-tab", "data"),
    [Input(tab_id, "n_clicks") for tab_id in TAB_IDS],
    prevent_initial_call=True
)
def select_tab(*_):
    triggered_id = ctx.triggered_id
    return TAB_IDS.index(triggered_id) + 1

# =============================================================================
# Update Main Content Based on Selected Tab, Player, and Season
# =============================================================================

@app.callback(
    Output("page-content", "children"),
    Input("selected-tab", "data"),
    Input("selected-player", "data"),
    Input("selected-season", "data")
)
def update_content(tab_index, player_id, stored_season):
    if tab_index == 1:
        player = df_player_resume[df_player_resume["player_id"] == player_id].iloc[0]
        matches = df_last_5_matches[df_last_5_matches["player_id"] == player_id]
        # Define positions and sizes
        image_top = 43
        image_left = 12
        image_height = 70
        number_top = 32
        number_left = 17
        number_font_size = 15
        text_top = 1
        text_left = 2
        title_size = TITLE_SIZE
        subtitle_size = SUBTITLE_SIZE
        body_size = BODY_SIZE
        info_top = 82
        info_left = image_left
        info_value_size = SUBTITLE_SIZE
        info_label_size = BODY_SIZE
        season_top = 15
        season_left = 30
        last_5_matches_top = 52
        last_5_matches_left = season_left
        margin_bottom_vh = 1
        logo_height_vh = 8
        top_donut = 10
        left_starting_donut = 48
        left_minutes_played_donut = 70
        size_donut_vh = 32
        return html.Div(
            children=[
                render_player_image(player, image_top, image_left, image_height),
                render_player_number(player, number_top, number_left, number_font_size),
                render_player_header(player, text_top, text_left, title_size, body_size),
                render_info_block(player, info_top, info_left, info_value_size, info_label_size),
                render_season_stats(player, season_top, season_left, subtitle_size, body_size),
                render_last_5_matches_tab(
                    matches,
                    last_5_matches_top,
                    last_5_matches_left,
                    body_size,
                    title="LAST 5 MATCHES",
                    title_font_size=subtitle_size,
                    margin_bottom_vh=margin_bottom_vh,
                    logo_height_vh=logo_height_vh
                ),
                render_donut(
                    df_player_resume, 'starting_eleven_pct', player_id, top_donut, left_starting_donut, size_donut_vh,
                    COLOR_LIGHT_BLUE, COLOR_DARK_BLUE, title='STARTING ELEVEN', title_font_size=body_size/1.5
                ),
                render_donut(
                    df_player_resume, 'minutes_played_pct', player_id, top_donut, left_minutes_played_donut, size_donut_vh,
                    COLOR_LIGHT_BLUE, COLOR_DARK_BLUE, title='MINUTES PLAYED', title_font_size=body_size/1.5
                )
            ],
            style={"position": "relative", "height": "100%", "width": "100%"}
        )
    elif tab_index == 2:
        saisons = sorted(df_cfc_gps_data_processed["season"].dropna().unique())
        season_filter_left_vw = 0
        season_filter_top_vh = -0.5
        season_filter_width_vw = 7
        season_filter_fontsize_vw = 0.75
        return html.Div(
            style={"position": "relative", "height": "100%", "width": "100%"},
            children=[
                dcc.Dropdown(
                    id="season-dropdown",
                    options=[{"label": s, "value": s} for s in sorted(saisons, reverse=True)],
                    value=stored_season,
                    clearable=False,
                    style={
                        "position": "absolute",
                        "top": f"{season_filter_top_vh}vh",
                        "left": f"{season_filter_left_vw}vw",
                        "width": f"{season_filter_width_vw}vw",
                        "zIndex": "999",
                        "fontSize": f"{season_filter_fontsize_vw}vw",
                        "color": COLOR_DARK_BLUE,
                        "backgroundColor": COLOR_SNOW
                    }
                ),
                html.Div(
                    id="page2-content",
                    style={"position": "relative", "top": "0vh", "left": "0vw", "width": "100%", "height": "100%"}
                )
            ]
        )
    elif tab_index == 3:
        saisons = sorted(df_cfc_recovery_augmented["seasonName"].dropna().unique(), reverse=True)
        season_filter_left_vw = 0
        season_filter_top_vh = -0.5
        season_filter_width_vw = 7
        season_filter_fontsize_vw = 0.75
        
        return html.Div(
            children=[
                dcc.Dropdown(
                    id="season-dropdown",
                    options=[{"label": s, "value": s} for s in saisons],
                    value=stored_season,
                    clearable=False,
                    style={
                        "position": "absolute",
                        "top": f"{season_filter_top_vh}vh",
                        "left": f"{season_filter_left_vw}vw",
                        "width": f"{season_filter_width_vw}vw",
                        "zIndex": "999",
                        "fontSize": f"{season_filter_fontsize_vw}vw",
                        "color": COLOR_DARK_BLUE,
                        "backgroundColor": COLOR_SNOW
                    }
                ),
                html.Div(
                    id="page3-content",
                    style={"position": "relative", "height": "100%", "width": "100%"}
                )
            ],
            style={"position": "relative", "height": "100%", "width": "100%"}
        )

# =============================================================================
# Additional Callbacks for Season and Player Selection
# =============================================================================

@app.callback(
    Output("selected-season", "data"),
    Input("season-dropdown", "value"),
    prevent_initial_call=True
)
def store_selected_season(selected_season):
    if selected_season is None:
        raise dash.exceptions.PreventUpdate
    return selected_season

@app.callback(
    Output("selected-player", "data"),
    Input({'type': 'player-img', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def select_player_from_image(n_clicks_list):
    trigger = ctx.triggered_id
    if trigger is None:
        raise dash.exceptions.PreventUpdate
    return trigger['index']

@app.callback(
    Output("tab-bar", "children"),
    Input("selected-tab", "data")
)
def update_tab_bar(tab_index):
    return [
        html.Div(
            title,
            id=TAB_IDS[i],
            n_clicks=0,
            style={
                "flex": "none",
                "width": TAB_WIDTH,
                "textAlign": "center",
                "cursor": "pointer",
                "fontFamily": "ChelseaBold" if (i + 1) == tab_index else "ChelseaRegular",
                "fontSize": FONTSIZE_TAB_VH,
                "color": COLOR_SNOW,
                "lineHeight": f"{6}vh",
                "backgroundColor": COLOR_BLUE if (i + 1) == tab_index else "transparent",
                "borderLeft": f"{0.1}vh solid {COLOR_SNOW}" if i > 0 else "none",
                "borderBottom": f"{0.1}vh solid {COLOR_SNOW}" if (i + 1) != tab_index else "none"
            }
        )
        for i, title in enumerate(TAB_TITLES)
    ]

@app.callback(
    Output("sidebar", "children"),
    Input("selected-player", "data")
)
def update_sidebar(selected_player_id):
    df_sorted = df_player_resume.sort_values('group_id')
    return html.Div(
        style={
            "height": "100%",
            "width": f"{SIDEBAR_WIDTH_VW}vw",
            "position": "absolute",
            "top": "0",
            "left": "0",
            "zIndex": "4",
            "paddingTop": f"{HEADER_HEIGHT_VH + LOGO_SIZE_VH / 2}vh",
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "overflowY": "auto"
        },
        children=[
            html.Div(
                id={'type': 'player-img', 'index': row['player_id']},
                title=row['name'],
                style={
                    "width": f"{SCALE_IMAGE_PLAYER_SIDEBAR_VW}vw",
                    "height": f"{SCALE_IMAGE_PLAYER_SIDEBAR_VW}vw",
                    "borderRadius": "50%",
                    "margin": "2vh 0",
                    "cursor": "pointer",
                    "overflow": "hidden",
                    "backgroundColor": COLOR_BLUE,
                    "display": "flex",
                    "alignItems": "flex-start",
                    "justifyContent": "center",
                    "border": f"{3 * LINEWIDTH_SEPARATION_VH}vh solid white" if row['player_id'] == selected_player_id else "none"
                },
                children=html.Img(
                    src=row['player_picture_url'],
                    style={
                        "height": "240%",
                        "objectFit": "cover"
                    }
                )
            )
            for _, row in df_sorted.iterrows()
        ]
    )

@app.callback(
    Output("page2-content", "children"),
    Input("selected-season", "data"),
    Input("selected-player", "data")
)
def update_page2_content(selected_season, player_id):
    if not selected_season or not player_id:
        return html.Div("Select a season and a player.")
    df_filtered = df_cfc_gps_data_processed[
        (df_cfc_gps_data_processed["player_id"] == player_id) &
        (df_cfc_gps_data_processed["season"] == selected_season)
    ]
    top_val = -7
    left_val = -1
    width_vw_val = 92
    height_vh_val = 98
    acute_color_val = "dodgerblue"
    chronic_color_val = "limegreen"
    acwr_color_val = COLOR_LIGHT_BLUE
    zone_under_color_val = COLOR_UNDER_TRAINING_LOAD
    zone_optimal_color_val = COLOR_OPTIMAL_TRAINING_LOAD
    zone_danger_color_val = COLOR_DANGER_LOAD
    font_color_val = COLOR_SNOW
    title1_val = "ACUTE & CHRONIC LOAD (TRIMP)"
    title2_val = "LOAD RATIO (ACWR) & INJURY RISK ZONES"
    fontsize_title_val = 20
    fontsize_axis_val = 16
    fontsize_legend_val = 10
    logo_size_val = 100
    return render_load_and_acwr_subplots(
        df=df_filtered,
        top=top_val,
        left=left_val,
        width_vw=width_vw_val,
        height_vh=height_vh_val,
        acute_color=acute_color_val,
        chronic_color=chronic_color_val,
        acwr_color=acwr_color_val,
        zone_under_color=zone_under_color_val,
        zone_optimal_color=zone_optimal_color_val,
        zone_danger_color=zone_danger_color_val,
        font_color=font_color_val,
        title1=title1_val,
        title2=title2_val,
        fontsize_title=fontsize_title_val,
        fontsize_axis=fontsize_axis_val,
        fontsize_legend=fontsize_legend_val,
        logo_size=logo_size_val
    )

@app.callback(
    Output("page3-content", "children"),
    [Input("season-dropdown", "value"),
     Input("selected-player", "data")]
)
def update_page3_content(selected_season, player_id):
    if not selected_season or not player_id:
        return html.Div("Select a season and a player.")
    
    # Filter processed DataFrames by selected season
    df_daily_filtered = df_cfc_recovery_data_processed_daily[
        df_cfc_recovery_data_processed_daily["seasonName"] == selected_season
    ]
    df_heatmap_filtered = df_cfc_recovery_data_processed_heatmap[
        df_cfc_recovery_data_processed_heatmap["seasonName"] == selected_season
    ]
    df_weekly_filtered = df_cfc_recovery_data_processed_weekly[
        df_cfc_recovery_data_processed_weekly["seasonName"] == selected_season
    ]
    
    # --------------------------------------------------------------------------
    # Define style and layout variables for graphs
    # --------------------------------------------------------------------------
    fontsize_title_val = 20
    fontsize_axis_val = 12
    fontsize_legend_val = 10

    subjective_color = "#FF00FF"
    sleep_color = "#00FFFF"
    soreness_color = "#FFA500"
    msk_joint_range_color = "#00FF00"
    msk_load_tolerance_color = "#FFFF00"
    bio_color = "#FF0000"

    top_val_daily = 0
    left_val = -1
    width_vw_val = 60
    height_vh_val = 27

    top_val_heatmap = top_val_daily + height_vh_val + 5
    top_val_weekly = top_val_heatmap + height_vh_val + 5

    # Recovery heatmap (radar chart) parameters
    top_heatmap_val = 35
    left_heatmap_val = 63
    width_vw_heatmap_val = 27
    height_vh_heatmap_val = 45
    title_heatmap_val = "LAST 7 DAYS RECOVERY (WEIGHTED)"
    title_font_size_heatmap_val = 18
    title_font_family_heatmap_val = "ChelseaBold"
    title_color_heatmap_val = COLOR_SNOW
    background_color_heatmap_val = 'rgba(0,0,0,0)'
    axis_font_size_heatmap_val = 10
    axis_font_family_heatmap_val = "ChelseaRegular"
    axis_font_color_heatmap_val = COLOR_DARK_BLUE
    theta_label_color_heatmap_val = COLOR_SNOW
    theta_label_fontsize_heatmap_val = 10
    theta_label_font_family_heatmap_val = "ChelseaRegular"
    positive_value_color_heatmap_val = COLOR_GREEN
    negative_value_color_heatmap_val = COLOR_RED
    marker_size_heatmap_val = 6

    # Daily recovery graph parameters
    daily_title = "DAILY RECOVERY METRICS EVOLUTION"
    daily_title_font_family = "ChelseaBold"
    daily_axis_font_family = "ChelseaRegular"
    daily_font_color = COLOR_SNOW
    daily_title_font_size = fontsize_title_val
    daily_axis_font_size = fontsize_axis_val
    daily_legend_font_size = fontsize_legend_val

    # Recovery heatmap graph parameters
    heatmap_title = "OVERALL RECOVERY SCORE (EMBOSS) HEATMAP"
    heatmap_font_color = COLOR_SNOW
    heatmap_font_family = "ChelseaRegular"
    heatmap_title_font_family = "ChelseaBold"
    heatmap_title_font_size = fontsize_title_val
    heatmap_axis_font_size = fontsize_axis_val
    heatmap_legend_font_size = fontsize_legend_val

    # Weekly recovery graph parameters
    weekly_title = "WEEKLY RECOVERY METRICS EVOLUTION"
    weekly_font_color = COLOR_SNOW
    weekly_title_font_family = "ChelseaBold"
    weekly_axis_font_family = "ChelseaRegular"
    weekly_title_font_size = fontsize_title_val
    weekly_axis_font_size = fontsize_axis_val
    weekly_legend_font_size = fontsize_legend_val
    weekly_color_map = {
        "bio_baseline_composite": bio_color,
        "msk_joint_range_baseline_composite": msk_joint_range_color,
        "msk_load_tolerance_baseline_composite": msk_load_tolerance_color,
        "soreness_baseline_composite": soreness_color,
        "subjective_baseline_composite": subjective_color,
        "sleep_baseline_composite": sleep_color
    }
    
    # Recovery summary info parameters
    summary_top = 5
    summary_left = 65
    summary_line_spacing = 5
    summary_title_text = "LAST 7 DAYS"
    summary_title_font_size = TITLE_SIZE
    summary_title_font_family = "ChelseaBold"
    summary_title_color = "#FFFFFF"
    summary_info_font_size = BODY_SIZE
    summary_info_font_family = "ChelseaRegular"
    summary_value_font_size = SUBTITLE_SIZE
    summary_value_font_family = "ChelseaBold"
    summary_positive_color = COLOR_GREEN
    summary_negative_color = COLOR_RED

    # Colored square background parameters
    square_top = 2
    square_left = 63
    square_width_vw = 27
    square_height_vh = 80
    square_background_color = COLOR_DARK_BLUE

    # --------------------------------------------------------------------------
    # Build Page 3 layout by calling rendering functions with defined variables
    # --------------------------------------------------------------------------
    return html.Div(
        children=[
            render_colored_square(
                top=square_top,
                left=square_left,
                width_vw=square_width_vw,
                height_vh=square_height_vh,
                background_color=square_background_color
            ),
            render_daily_recovery_graph(
                player_id=player_id,
                processed_df=df_daily_filtered,
                top=top_val_daily,
                left=left_val,
                width_vw=width_vw_val,
                height_vh=height_vh_val,
                font_color=daily_font_color,
                title=daily_title,
                title_font_family=daily_title_font_family,
                title_font_size=daily_title_font_size,
                axis_font_family=daily_axis_font_family,
                axis_font_size=daily_axis_font_size,
                legend_font_size=daily_legend_font_size,
                subjective_color=subjective_color,
                sleep_color=sleep_color,
                soreness_color=soreness_color
            ),
            render_recovery_heatmap(
                processed_df=df_heatmap_filtered,
                player_id=player_id,
                top=top_val_heatmap,
                left=left_val,
                width_vw=width_vw_val,
                height_vh=height_vh_val,
                title=heatmap_title,
                font_color=heatmap_font_color,
                font_family=heatmap_font_family,
                title_font_family=heatmap_title_font_family,
                title_font_size=heatmap_title_font_size,
                axis_font_size=heatmap_axis_font_size,
                legend_font_size=heatmap_legend_font_size
            ),
            render_weekly_recovery_graph(
                processed_df=df_weekly_filtered,
                player_id=player_id,
                top=top_val_weekly,
                left=left_val,
                width_vw=width_vw_val,
                height_vh=height_vh_val,
                title=weekly_title,
                font_color=weekly_font_color,
                title_font_family=weekly_title_font_family,
                title_font_size=weekly_title_font_size,
                axis_font_family=weekly_axis_font_family,
                axis_font_size=weekly_axis_font_size,
                legend_font_size=weekly_legend_font_size,
                color_discrete_map=weekly_color_map
            ),
            render_recovery_summary_info(
                df=df_cfc_recovery_last_7d,
                player_id=player_id,
                top=summary_top,
                left=summary_left,
                line_spacing=summary_line_spacing,
                title_text=summary_title_text,
                title_font_size=summary_title_font_size,
                title_font_family=summary_title_font_family,
                title_color=summary_title_color,
                info_font_size=summary_info_font_size,
                info_font_family=summary_info_font_family,
                value_font_size=summary_value_font_size,
                value_font_family=summary_value_font_family,
                positive_color=summary_positive_color,
                negative_color=summary_negative_color
            ),
            render_recovery_radar_chart(
                processed_df=df_cfc_recovery_last_7d,
                player_id=player_id,
                top=top_heatmap_val,
                left=left_heatmap_val,
                width_vw=width_vw_heatmap_val,
                height_vh=height_vh_heatmap_val,
                title=title_heatmap_val,
                title_font_size=title_font_size_heatmap_val,
                title_font_family=title_font_family_heatmap_val,
                title_color=title_color_heatmap_val,
                background_color=background_color_heatmap_val,
                axis_font_size=axis_font_size_heatmap_val,
                axis_font_family=axis_font_family_heatmap_val,
                axis_font_color=axis_font_color_heatmap_val,
                theta_label_color=theta_label_color_heatmap_val,
                theta_label_fontsize=theta_label_fontsize_heatmap_val,
                theta_label_font_family=theta_label_font_family_heatmap_val,
                positive_value_color=positive_value_color_heatmap_val,
                negative_value_color=negative_value_color_heatmap_val,
                marker_size=marker_size_heatmap_val
            )
        ],
        style={"position": "relative", "height": "100%", "width": "100%"}
    )

# =============================================================================
# Run the app
# =============================================================================

if __name__ == "__main__":
    app.run(debug=True)
