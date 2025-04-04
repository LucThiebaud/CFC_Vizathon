from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from constants import *
from styles import *
import dash_bootstrap_components as dbc

# =============================================================================
# Static Components
# =============================================================================

def get_header_background() -> html.Div:
    """Return a Div with the header background style."""
    return html.Div(style=HEADER_BACKGROUND_STYLE)

def get_sidebar_background() -> html.Div:
    """Return a Div with the sidebar background style."""
    return html.Div(style=SIDEBAR_BACKGROUND_STYLE)

def get_logo() -> html.Img:
    """Return an image component displaying the Chelsea logo."""
    return html.Img(src=URL_CHELSEA_LOGO, style=LOGO_STYLE)

def get_separation_line() -> html.Div:
    """Return a Div styled as a separation line."""
    return html.Div(style=SEPARATION_LINE_STYLE)

def get_tab_bar() -> html.Div:
    """Return a Div for the tab bar with its associated style."""
    return html.Div(id="tab-bar", style=TAB_BAR_STYLE)

def get_page_content() -> html.Div:
    """Return a Div for the page content with its associated style."""
    return html.Div(id="page-content", style=PAGE_CONTENT_STYLE)

def get_sidebar() -> html.Div:
    """Return a Div for the sidebar."""
    return html.Div(id="sidebar")

# =============================================================================
# Dynamic Rendering Functions
# =============================================================================

##############################################
# PAGE 1 - Player Details and Stats
##############################################

def render_player_image(player, top, left, height):
    """Render the player's image with absolute positioning."""
    return html.Img(
        src=player["player_picture_url"],
        style={
            "position": "absolute",
            "height": f"{height}vh",
            "left": f"{left}vw",
            "top": f"{top}vh",
            "transform": "translate(-50%, -50%)",
            "objectFit": "contain",
            "zIndex": "2"
        }
    )

def render_player_number(player, top, left, font_size):
    """Render the player's number with absolute positioning."""
    return html.Div(
        str(player["number"]),
        style={
            "position": "absolute",
            "top": f"{top}vh",
            "left": f"{left}vw",
            "transform": "translate(0%, -50%)",
            "fontSize": f"{font_size}vh",
            "fontFamily": "ChelseaBold",
            "color": COLOR_LIGHT_BLUE,
            "zIndex": "1"
        }
    )

def render_player_header(player, top, left, title_size, body_size):
    """Render the player's header with name and group information."""
    return html.Div(
        children=[
            html.Div([
                html.Span(player["name"].upper(), style={"marginRight": "1vw"}),
                html.Img(
                    src=player["url_picture_country"],
                    style={
                        "height": f"{title_size * 0.8}vh",
                        "verticalAlign": "middle"
                    }
                )
            ], style={"display": "flex", "alignItems": "center"}),
            html.Div(
                player["group"].upper(),
                style={
                    "fontSize": f"{body_size}vh",
                    "marginTop": "0.5vh",
                    "fontFamily": "ChelseaRegular"
                }
            )
        ],
        style={
            "position": "absolute",
            "left": f"{left}vw",
            "top": f"{top}vh",
            "fontSize": f"{title_size}vh",
            "color": COLOR_SNOW,
            "fontFamily": "ChelseaBold",
            "zIndex": "2"
        }
    )

def render_info_block(player, top, left, value_size, label_size):
    """Render a block showing player's info (age, height, weight, foot)."""
    def info_item(value, label):
        return html.Div([
            html.Div(str(value), style={
                "fontWeight": "bold",
                "fontSize": f"{value_size}vh",
                "fontFamily": "ChelseaBold"
            }),
            html.Div(label, style={
                "fontSize": f"{label_size}vh",
                "fontFamily": "ChelseaRegular"
            })
        ])
    return html.Div(
        children=[
            info_item(player["age"], "YR"),
            info_item(player["height"], "CM"),
            info_item(player["weight"], "KG"),
            info_item(player["foot"].upper(), "FOOT")
        ],
        style={
            "position": "absolute",
            "top": f"{top}vh",
            "left": f"{left}vw",
            "transform": "translateX(-50%)",
            "display": "flex",
            "gap": "2.5vw",
            "color": COLOR_SNOW,
            "textAlign": "center",
            "zIndex": "2"
        }
    )

def render_season_stats(player, top, left, subtitle_size, body_size):
    """Render the player's season statistics."""
    group_id = player["group_id"]
    def stat_line(label, value):
        return html.Div([
            html.Span(f"{label} ", style={
                "fontSize": f"{body_size}vh",
                "fontFamily": "ChelseaRegular"
            }),
            html.Span(str(value), style={
                "fontSize": f"{body_size}vh",
                "fontFamily": "ChelseaBold",
                "fontWeight": "bold"
            })
        ], style={"marginBottom": "1vh"})
    lines = [
        html.Div("SEASON STATS", style={
            "fontSize": f"{subtitle_size}vh",
            "fontFamily": "ChelseaBold",
            "marginBottom": "1.5vh"
        }),
        stat_line("Appearances (Starts):", f"{player['appearances']} ({player['starts']})"),
        stat_line("Minutes played:", f"{player['minutes']}"),
        stat_line("Goals / Assists:", f"{player['goals']} / {player['assists']}")
    ]
    if group_id == 1:
        lines += [
            stat_line("Pass accuracy (%):", player["pass_accuracy"]),
            stat_line("Saves:", player["save"]),
            stat_line("Save (%):", player["pct_save"])
        ]
    elif group_id == 2:
        lines += [
            stat_line("Pass accuracy (%):", player["pass_accuracy"]),
            stat_line("Tackles:", player["tackles"]),
            stat_line("Interceptions:", player["interceptions"])
        ]
    elif group_id == 3:
        lines += [
            stat_line("Pass accuracy (%):", player["pass_accuracy"]),
            stat_line("Key Passes:", player["key_passes"]),
            stat_line("Tackles:", player["tackles"]),
            stat_line("Interceptions:", player["interceptions"])
        ]
    elif group_id == 4:
        lines += [
            stat_line("Pass accuracy (%):", player["pass_accuracy"]),
            stat_line("Key Passes:", player["key_passes"]),
            stat_line("Shots:", player["shots"]),
            stat_line("Shots on target:", player["shots_on_target"])
        ]
    elif group_id == 5:
        lines += [
            stat_line("Pass accuracy (%):", player["pass_accuracy"]),
            stat_line("Shots:", player["shots"]),
            stat_line("Shots on target:", player["shots_on_target"])
        ]
    return html.Div(
        children=lines,
        style={
            "position": "absolute",
            "top": f"{top}vh",
            "left": f"{left}vw",
            "color": COLOR_SNOW,
            "textAlign": "left",
            "zIndex": "2"
        }
    )

def render_match_column_with_tooltip(
    row: pd.Series,
    match_index: int,
    body_font_size_vw: float,
    margin_bottom_vh: float,
    logo_height_vh: float
):
    """
    Create a match column with a tooltip showing match details.
    
    Returns a tuple: (match Div, associated dbc.Tooltip).
    """
    from constants import COLOR_RED, COLOR_SNOW, COLOR_GREEN
    import dash_bootstrap_components as dbc
    from dash import html

    is_missing_minutes = pd.isna(row["minutes_played"])
    starter_color = COLOR_RED if is_missing_minutes else COLOR_SNOW
    col_id = f"match-col-{match_index}"
    
    result = row.get("result", "")
    if result == 'W':
        score_color = COLOR_GREEN
    elif result == 'L':
        score_color = COLOR_RED
    elif result == 'D':
        score_color = COLOR_SNOW
    else:
        score_color = "inherit"

    tooltip_elements = [
        html.Div(
            ["Date: ", html.Span(row['match_date'].strftime('%Y-%m-%d'), style={"fontFamily": "ChelseaBold"})],
            style={"fontFamily": "ChelseaRegular"}
        ),
        html.Div(
            ["Opponent: ", html.Span(row.get('opponent_name', 'Unknown'), style={"fontFamily": "ChelseaBold"})],
            style={"fontFamily": "ChelseaRegular"}
        ),
        html.Div(
            ["Score: ", html.Span(row.get("score", ""), style={"color": score_color, "fontFamily": "ChelseaBold"})],
            style={"fontFamily": "ChelseaRegular"}
        )
    ]
    if row.get("goals", 0) > 0:
        tooltip_elements.append(
            html.Div(
                ["Goal(s): ", html.Span(int(row['goals']), style={"fontFamily": "ChelseaBold"})],
                style={"fontFamily": "ChelseaRegular"}
            )
        )
    if row.get("assists", 0) > 0:
        tooltip_elements.append(
            html.Div(
                ["Assist(s): ", html.Span(int(row['assists']), style={"fontFamily": "ChelseaBold"})],
                style={"fontFamily": "ChelseaRegular"}
            )
        )

    tooltip_content = html.Div(tooltip_elements, style={"fontFamily": "ChelseaRegular"})
    match_div = html.Div(
        id=col_id,
        children=[
            html.Img(
                src=row["opponent_url_picture"],
                style={
                    "height": f"{logo_height_vh}vh",
                    "objectFit": "contain",
                    "marginBottom": f"{margin_bottom_vh}vh"
                }
            ),
            html.Div(
                row["match_date"].strftime("%b. %#d"),
                style={
                    "fontSize": f"{body_font_size_vw}vh",
                    "fontFamily": "ChelseaRegular",
                    "marginBottom": f"{margin_bottom_vh}vh"
                }
            ),
            html.Div(
                "Home" if row["is_home"] else "Away",
                style={
                    "fontSize": f"{body_font_size_vw}vh",
                    "fontFamily": "ChelseaRegular",
                    "marginBottom": f"{margin_bottom_vh}vh"
                }
            ),
            html.Div(
                str(row["starter_group"]),
                style={
                    "fontSize": f"{body_font_size_vw}vh",
                    "fontFamily": "ChelseaBold",
                    "marginBottom": f"{margin_bottom_vh}vh",
                    "color": starter_color
                }
            ),
            html.Div(
                "" if is_missing_minutes else f"{int(row['minutes_played'])}'",
                style={
                    "fontSize": f"{body_font_size_vw}vh",
                    "fontFamily": "ChelseaBold"
                }
            )
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "justifyContent": "flex-start",
            "width": "9vw",
            "margin": "0 1vw"
        }
    )
    match_tooltip = dbc.Tooltip(
        children=tooltip_content,
        target=col_id,
        placement="top",
        className="custom-tooltip"
    )
    return match_div, match_tooltip

def render_last_5_matches_tab(
    matches: pd.DataFrame,
    top: float,
    left: float,
    body_font_size_vw: float,
    title: str = "LAST 5 MATCHES",
    title_font_size: float = 2,
    margin_bottom_vh: float = 1,
    logo_height_vh: float = 5
) -> html.Div:
    """Generate a component displaying the last 5 matches with tooltips."""
    filtered_matches = (matches.drop_duplicates("match_id")
                        .sort_values("match_date", ascending=True)
                        .head(5))
    title_div = html.Div(
        title,
        style={
            "fontSize": f"{title_font_size}vh",
            "fontFamily": "ChelseaBold",
            "color": COLOR_SNOW,
            "marginBottom": "2vh",
            "textAlign": "left"
        }
    )
    match_columns = []
    for i, (_, row) in enumerate(filtered_matches.iterrows()):
        col_div, col_tooltip = render_match_column_with_tooltip(
            row,
            match_index=i,
            body_font_size_vw=body_font_size_vw,
            margin_bottom_vh=margin_bottom_vh,
            logo_height_vh=logo_height_vh
        )
        match_columns.append(col_div)
        match_columns.append(col_tooltip)
    matches_div = html.Div(
        children=match_columns,
        style={
            "display": "flex",
            "flexDirection": "row",
            "justifyContent": "center",
            "alignItems": "flex-start"
        }
    )
    return html.Div(
        children=[title_div, matches_div],
        style={
            "position": "absolute",
            "top": f"{top}vh",
            "left": f"{left}vw",
            "zIndex": "2",
            "textAlign": "center"
        }
    )

def render_donut(df, pct_column, player_id, top, left, size_vh, color, background_color, title, title_font_size):
    """
    Render a donut chart with a tooltip displaying either the number of starts or minutes.
    For 'starting_eleven_pct', tooltip shows "Starts: <value> out of 45 games".
    For 'minutes_played_pct', tooltip shows "Minutes: <value> out of 4050".
    """
    player_data = df[df["player_id"] == player_id]
    pct = player_data[pct_column].iloc[0]
    if pct_column == 'starting_eleven_pct':
        tooltip_label = "Starts: "
        tooltip_value = player_data["starts"].iloc[0]
        tooltip_suffix = " out of 45 games"
    elif pct_column == 'minutes_played_pct':
        tooltip_label = "Minutes: "
        tooltip_value = player_data["minutes"].iloc[0]
        tooltip_suffix = " out of 4050"
    else:
        tooltip_label = "Value: "
        tooltip_value = "N/A"
        tooltip_suffix = ""
    value = int(round(pct * 100, 1))
    remaining = 100 - value
    fig = go.Figure(data=[go.Pie(
        values=[value, remaining],
        hole=0.6,
        marker=dict(colors=[color, background_color]),
        textinfo='none',
        hoverinfo='skip',
        sort=False
    )])
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        annotations=[dict(
            text=f"{value}%",
            font=dict(size=20, family="ChelseaBold", color=color),
            showarrow=False,
            x=0.5,
            y=0.5
        )]
    )
    donut_id = f"donut-{player_id}-{pct_column}"
    donut_div = html.Div(
        children=[
            html.Div(title, style={
                "fontSize": f"{title_font_size}vw",
                "fontFamily": "ChelseaBold",
                "color": color,
                "marginBottom": "2vh",
                "textAlign": "center"
            }),
            dcc.Graph(
                figure=fig,
                config={"displayModeBar": False},
                style={"width": f"{size_vh}vh", "height": f"{size_vh}vh"}
            )
        ],
        id=donut_id,
        style={
            "position": "absolute",
            "top": f"{top}vh",
            "left": f"{left}vw",
            "zIndex": "2"
        }
    )
    tooltip_content = html.Div([
        html.Span(tooltip_label, style={"fontFamily": "ChelseaRegular"}),
        html.Span(tooltip_value, style={"fontFamily": "ChelseaBold"}),
        html.Span(tooltip_suffix, style={"fontFamily": "ChelseaRegular"})
    ])
    donut_tooltip = dbc.Tooltip(
        children=tooltip_content,
        target=donut_id,
        placement="top",
        className="custom-tooltip"
    )
    return html.Div(children=[donut_div, donut_tooltip], style={"position": "relative"})

##############################################
# PAGE 2 - Load, ACWR & Injury Zones
##############################################

def render_load_and_acwr_subplots(
    df,
    top,
    left,
    width_vw,
    height_vh,
    acute_color,
    chronic_color,
    acwr_color,
    zone_under_color,
    zone_optimal_color,
    zone_danger_color,
    font_color,
    title1,
    title2,
    fontsize_title,
    fontsize_axis,
    fontsize_legend,
    logo_size
):
    """
    Render a composite subplot displaying load, ACWR, and injury zone data.
    Creates three subplots:
      1. Loads: Acute and chronic load.
      2. Injury Zones: Training availability with injury overlays.
      3. ACWR & Risk Zones: ACWR trends with risk zones and injury markers.
    """
    df = df.dropna(subset=["trimp_edwards_acute_load", "trimp_edwards_chronic_load", "acwr"])
    df = df.sort_values("date")
    df["date"] = pd.to_datetime(df["date"])
    x0 = df["date"].min()
    x1 = df["date"].max()
    total_interval_ms = (x1 - x0).total_seconds() * 1000
    computed_sizex = (logo_size / 100) * total_interval_ms

    from plotly.subplots import make_subplots
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        row_heights=[0.6, 0.03, 0.3],
        vertical_spacing=0.12,
        subplot_titles=(title1, "", title2)
    )

    # Subplot 1: Loads
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["trimp_edwards_chronic_load"],
            name="Chronic Load",
            mode="lines",
            line=dict(color=chronic_color, width=3, dash="dash"),
            fill="tozeroy",
            fillcolor="rgba(50,205,50,0.2)",
            hovertemplate="Chronic Load: %{y:.0f}<extra></extra>"
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df["trimp_edwards_acute_load"],
            name="Acute Load",
            marker=dict(color=acute_color, line=dict(width=0)),
            opacity=0.85,
            hovertemplate="Acute Load: %{y:.0f}<extra></extra>"
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["trimp_edwards_chronic_load"],
            mode="markers",
            marker=dict(size=0, color="rgba(0,0,0,0)"),
            customdata=df[[ 
                "distance_km", "day_duration", "trimp_edwards",
                "distance_label", "duration_label", "load_label",
                "opposition_text", "acwr"
            ]].values.tolist(),
            hovertemplate=(
                "ACWR: %{customdata[7]:.2f}<br><br>"
                "%{customdata[6]}%{customdata[3]}%{customdata[0]:.1f}<br>"
                "%{customdata[4]}%{customdata[1]:.0f}<br>"
                "%{customdata[5]}%{customdata[2]:.0f}<extra></extra>"
            ),
            showlegend=False
        ),
        row=1, col=1
    )
    for _, row_ in df.iterrows():
        logo_url = row_.get("url_logo_opponent")
        if pd.notna(logo_url) and logo_url != "" and row_.get("day_duration", 0) > 0:
            fig.add_shape(
                type="line",
                xref="x", yref="y",
                x0=row_["date"], x1=row_["date"],
                y0=0, y1=200 - logo_size / 2 - 2,
                line=dict(dash="dot", color=font_color, width=1),
                layer="above"
            )
            fig.add_layout_image(
                dict(
                    source=logo_url,
                    xref="x",
                    yref="y",
                    x=row_["date"],
                    y=200,
                    sizex=computed_sizex,
                    sizey=logo_size,
                    xanchor="center",
                    yanchor="middle",
                    layer="above"
                )
            )
    fig.update_yaxes(range=[0, 1500], row=1, col=1)

    # Subplot 2: Injury Zones
    fig.add_trace(
        go.Scatter(x=df["date"], y=[None], showlegend=False),
        row=2, col=1
    )
    fig.update_yaxes(
        range=[0, 1],
        title_text="Availability",
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        row=2, col=1
    )
    fig.add_shape(
        type="rect",
        xref="x",
        yref="y2",
        x0=df["date"].min(),
        x1=df["date"].max(),
        y0=0,
        y1=1,
        fillcolor=COLOR_GREEN,
        opacity=1,
        layer="below",
        line_width=0
    )
    season_start = df["date"].min()
    season_end = df["date"].max()
    from data_loader import df_injuries_histo
    injuries_player = df_injuries_histo[
        (df_injuries_histo["player_id"] == df["player_id"].iloc[0]) &
        (df_injuries_histo["injury_date"] <= season_end) &
        (df_injuries_histo["return_date"] >= season_start)
    ]
    for _, inj_row in injuries_player.iterrows():
        x0_inj = max(inj_row["injury_date"], season_start)
        x1_inj = min(inj_row["return_date"], season_end)
        if x0_inj >= x1_inj:
            continue
        fig.add_shape(
            type="rect",
            xref="x",
            yref="y2",
            x0=x0_inj,
            x1=x1_inj,
            y0=0,
            y1=1,
            fillcolor=COLOR_RED,
            opacity=1,
            layer="above",
            line_width=0
        )
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=[1] * len(df),
            mode="markers",
            marker=dict(size=20, color="rgba(0,0,0,0)"),
            customdata=df[[ 'injury_label', 'injury_date_label', 'return_date_label',
                             'body_part_label', 'injury_name_label' ]].values.tolist(),
            hovertemplate=(
                "%{customdata[0]}%{customdata[1]}%{customdata[2]}"
                "%{customdata[3]}%{customdata[4]}<extra></extra>"
            ),
            showlegend=False
        ),
        row=2, col=1
    )

    # Subplot 3: ACWR and Risk Zones
    fig.add_shape(
        type="rect",
        xref="x3", yref="y3",
        x0=x0, x1=x1,
        y0=0, y1=0.8,
        fillcolor=zone_under_color,
        opacity=0.7,
        layer="below",
        line_width=0,
        row=3, col=1
    )
    fig.add_shape(
        type="rect",
        xref="x3", yref="y3",
        x0=x0, x1=x1,
        y0=0.8, y1=1.5,
        fillcolor=zone_optimal_color,
        opacity=0.7,
        layer="below",
        line_width=0,
        row=3, col=1
    )
    fig.add_shape(
        type="rect",
        xref="x3", yref="y3",
        x0=x0, x1=x1,
        y0=1.5, y1=4,
        fillcolor=zone_danger_color,
        opacity=0.7,
        layer="below",
        line_width=0,
        row=3, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["acwr"],
            name="ACWR",
            mode="lines",
            line=dict(color=acwr_color, width=2),
            marker=dict(color=acwr_color),
            hovertemplate="ACWR: %{y:.2f}<extra></extra>"
        ),
        row=3, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["acwr"],
            mode="markers",
            marker=dict(size=0, color="rgba(0,0,0,0)"),
            customdata=df[["trimp_edwards_acute_load", "trimp_edwards_chronic_load"]].values.tolist(),
            hovertemplate=(
                "Chronic Load: %{customdata[1]:.0f}<br>"
                "Acute Load: %{customdata[0]:.0f}<extra></extra>"
            ),
            showlegend=False
        ),
        row=3, col=1
    )
    from data_loader import df_injuries_histo
    df_injuries_on_acwr = pd.merge(
        df[["player_id", "date", "acwr"]],
        df_injuries_histo[["player_id", "injury_date", "return_date", "body_part", "injury_name"]],
        how="inner",
        left_on=["player_id", "date"],
        right_on=["player_id", "injury_date"]
    )
    fig.add_trace(
        go.Scatter(
            x=df_injuries_on_acwr["date"],
            y=df_injuries_on_acwr["acwr"],
            mode="markers",
            marker=dict(
                symbol="cross",
                size=15,
                color="white",
                line=dict(color="red", width=2)
            ),
            name="Injury",
            customdata=df_injuries_on_acwr[["body_part", "injury_name"]].values.tolist(),
            hovertemplate=(
                "Body part: %{customdata[0]}<br>"
                "Injury: %{customdata[1]}<extra></extra>"
            ),
            showlegend=True
        ),
        row=3, col=1
    )
    fig.update_layout(hovermode="closest", hoverdistance=1)
    for _, row_ in df_injuries_on_acwr.iterrows():
        fig.add_shape(
            type="line",
            xref="x3",
            yref="y3",
            x0=row_["date"],
            x1=row_["date"],
            y0=0,
            y1=row_["acwr"],
            line=dict(dash="dot", color=COLOR_SNOW, width=1),
            layer="below",
            row=3, col=1
        )
    fig.update_yaxes(range=[0, 2], row=3, col=1)

    dummy_under = go.Scatter(
        x=[None],
        y=[None],
        mode="markers",
        marker=dict(color=zone_under_color, size=10),
        name="Under Training (ACWR < 0.8)"
    )
    dummy_optimal = go.Scatter(
        x=[None],
        y=[None],
        mode="markers",
        marker=dict(color=zone_optimal_color, size=10),
        name="Optimal Workload (0.8 - 1.5)"
    )
    dummy_danger = go.Scatter(
        x=[None],
        y=[None],
        mode="markers",
        marker=dict(color=zone_danger_color, size=10),
        name="Danger zone (ACWR > 1.5)"
    )
    fig.add_trace(dummy_under)
    fig.add_trace(dummy_optimal)
    fig.add_trace(dummy_danger)

    fig.update_layout(
        hovermode="x unified",
        xaxis=dict(
            tickformat="%b %d",
            tickfont=dict(color=font_color, family="ChelseaRegular", size=fontsize_axis),
            linecolor=font_color,
            mirror=True
        ),
        yaxis=dict(
            title="Load (TRIMP)",
            tickfont=dict(color=font_color, family="ChelseaRegular", size=fontsize_axis),
            zeroline=True,
            zerolinecolor="gray"
        ),
        yaxis3=dict(
            title="ACWR",
            tickfont=dict(color=font_color, family="ChelseaRegular", size=fontsize_axis),
            zeroline=True,
            zerolinecolor="gray",
            showgrid=False
        ),
        xaxis3=dict(
            title=None,
            tickfont=dict(color=font_color),
            linecolor=font_color,
            mirror=True
        ),
        hoverlabel=dict(
            bgcolor=COLOR_SNOW,
            font_size=fontsize_legend,
            font_family="ChelseaRegular",
            font_color="black"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="ChelseaRegular", color=font_color),
        legend=dict(
            font=dict(color=font_color, family="ChelseaRegular", size=fontsize_legend),
            x=1.02,
            y=0.5
        )
    )
    if fig.layout.annotations:
        for annotation in fig.layout.annotations:
            annotation.font.size = fontsize_title
            annotation.font.family = "ChelseaBold"
            annotation.font.color = font_color

    return html.Div(
        [dcc.Graph(
            figure=fig,
            config={"displayModeBar": False},
            style={"width": f"{width_vw}vw", "height": f"{height_vh}vh"}
        )],
        style={
            "position": "absolute",
            "top": f"{top}vh",
            "left": f"{left}vw",
            "zIndex": "2"
        }
    )

################################
# = PAGE 3 =
################################

def render_daily_recovery_graph(
    player_id: int,
    processed_df: pd.DataFrame,
    top: float,
    left: float,
    width_vw: float,
    height_vh: float,
    font_color: str,
    title: str,
    title_font_family: str,
    title_font_size: int,
    axis_font_family: str,
    axis_font_size: int,
    legend_font_size: int,
    subjective_color: str,
    sleep_color: str,
    soreness_color: str
):
    """
    Filters the processed DataFrame for the selected player and creates a graph showing
    the daily evolution of composite scores.

    Args:
        player_id (int): The player's identifier.
        processed_df (pd.DataFrame): Processed DataFrame (result of process_recovery_data).
        top (float): Vertical position (in vh) of the graph container.
        left (float): Horizontal position (in vw) of the graph container.
        width_vw (float): Width of the container (in vw).
        height_vh (float): Height of the container (in vh).
        font_color (str): General text color.
        title (str): Title of the graph.
        title_font_family (str): Font family for the title.
        title_font_size (int): Font size for the title.
        axis_font_family (str): Font family for the axes and tick labels.
        axis_font_size (int): Font size for the axes.
        legend_font_size (int): Font size for the legend.
        subjective_color (str): Color for the "Subjective" line.
        sleep_color (str): Color for the "Sleep" line.
        soreness_color (str): Color for the "Soreness" line.

    Returns:
        dcc.Graph: A Dash Graph component containing the Plotly figure.
    """
    # Filter data for the selected player
    df_player = processed_df[processed_df['player_id'] == player_id]
    
    # Create the figure
    fig = go.Figure()

    # Trace for "subjective_baseline_composite"
    if 'subjective_baseline_composite' in df_player.columns:
        fig.add_trace(go.Scatter(
            x=df_player['sessionDate'], 
            y=df_player['subjective_baseline_composite'],
            mode='lines+markers', 
            name='Subjective',
            line=dict(color=subjective_color),
            showlegend=True
        ))
    
    # Trace for "sleep_baseline_composite"
    if 'sleep_baseline_composite' in df_player.columns:
        fig.add_trace(go.Scatter(
            x=df_player['sessionDate'], 
            y=df_player['sleep_baseline_composite'],
            mode='lines+markers', 
            name='Sleep',
            line=dict(color=sleep_color),
            showlegend=True
        ))
    
    # Trace for "soreness_baseline_composite"
    if 'soreness_baseline_composite' in df_player.columns:
        fig.add_trace(go.Scatter(
            x=df_player['sessionDate'], 
            y=df_player['soreness_baseline_composite'],
            mode='lines+markers', 
            name='Soreness',
            line=dict(color=soreness_color),
            showlegend=True
        ))
    
    # Visibility control buttons
    buttons = [
        dict(
            label='Display All',
            method='update',
            args=[{'visible': [True, True, True]}]
        ),
        dict(
            label='Subjective Only',
            method='update',
            args=[{'visible': [True, False, False]}]
        ),
        dict(
            label='Sleep Only',
            method='update',
            args=[{'visible': [False, True, False]}]
        ),
        dict(
            label='Soreness Only',
            method='update',
            args=[{'visible': [False, False, True]}]
        )
    ]
    
    # Update the layout of the figure
    fig.update_layout(
        title={
            "text": title,
            "font": {"size": title_font_size, "color": font_color, "family": title_font_family},
            "x": 0.5,
            "xanchor": "center",
            "pad": {"t": 0, "b": 0}
        },
        margin=dict(t=50, b=0, l=0, r=0),
        xaxis_title=None,
        yaxis_title='Score',
        template='plotly_white',
        font={"color": font_color, "family": axis_font_family},
        xaxis={
            "tickfont": {"size": axis_font_size, "color": font_color, "family": axis_font_family},
        },
        yaxis={
            "tickfont": {"size": axis_font_size, "color": font_color, "family": axis_font_family},
        },
        legend={
            "font": {"size": legend_font_size, "color": font_color, "family": axis_font_family}
        },
        updatemenus=[dict(
            type="dropdown",
            direction="down",
            buttons=buttons,
            showactive=True,
            x=1.1,
            xanchor="right",
            y=1.05,
            yanchor="bottom",
            bgcolor=COLOR_SNOW,
            font={'color':COLOR_DARK_BLUE}
        )],
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_yaxes(range=[-1, 1])

    return dcc.Graph(
        figure=fig, 
        config={"displayModeBar": False},
        style={
            "position": "absolute",
            "top": f"{top}vh",
            "left": f"{left}vw",
            "width": f"{width_vw}vw",
            "height": f"{height_vh}vh",
            "background": "transparent"
        }
    )


def render_recovery_heatmap(
    processed_df: pd.DataFrame,
    player_id: int,
    top: float,
    left: float,
    width_vw: float,
    height_vh: float,
    title: str,
    font_color: str,
    font_family: str,
    title_font_family: str,
    title_font_size: int,
    axis_font_size: int,
    legend_font_size: int
):
    """
    Creates a heatmap from the processed DataFrame for the given player.

    The DataFrame is filtered by player_id, sorted by month (using '%B %Y' format), and then
    a heatmap is generated using Plotly Express's imshow.

    Args:
        processed_df (pd.DataFrame): Pivoted table from process_heatmap_data.
        player_id (int): The player's identifier.
        top (float): Vertical position (in vh) of the container.
        left (float): Horizontal position (in vw) of the container.
        width_vw (float): Width of the container (in vw).
        height_vh (float): Height of the container (in vh).
        title (str): Title of the graph.
        font_color (str): General text color.
        font_family (str): Font family for text (axes, ticks, legend).
        title_font_family (str): Font family for the title.
        title_font_size (int): Font size for the title.
        axis_font_size (int): Font size for axes and tick labels.
        legend_font_size (int): Font size for the legend.

    Returns:
        dcc.Graph: A Dash Graph component containing the heatmap.
    """
    # Filter data for the specified player
    df_player = processed_df[processed_df['player_id'] == player_id].copy()
    
    # Sort by 'Month' in ascending order (convert string to datetime)
    df_player = df_player.sort_values(by='Month', key=lambda col: pd.to_datetime(col, format='%B %Y'))
    
    # Set 'Month' as the index for the heatmap's y-axis
    heatmap_data = df_player.set_index('Month')
    
    # Use all columns except 'player_id' and 'seasonName' for the heatmap
    cols = [c for c in heatmap_data.columns if c not in ['player_id', 'seasonName']]
    
    # Create the heatmap using Plotly Express
    fig_heatmap = px.imshow(
        heatmap_data[cols],
        labels=dict(x="Month day", y="Month", color="Overall score"),
        x=heatmap_data[cols].columns,
        y=heatmap_data.index,
        color_continuous_scale='RdYlGn',
        range_color=(-1, 1),
        color_continuous_midpoint=0,
        text_auto='.2f',
        aspect='auto',
        title=title
    )
    
    # Place the x-axis at the bottom
    fig_heatmap.update_xaxes(side="bottom")
    
    # Update layout with styles and transparent background
    fig_heatmap.update_layout(
        title={
            "text": title,
            "font": {"size": title_font_size, "color": font_color, "family": title_font_family},
            "x": 0.5,
            "xanchor": "center",
            "pad": {"t": 0, "b": 0}
        },
        margin=dict(t=40, b=0, l=0, r=0),
        font={"color": font_color, "family": font_family},
        xaxis={
            "tickfont": {"size": axis_font_size, "color": font_color, "family": font_family},
        },
        yaxis={
            "tickfont": {"size": axis_font_size, "color": font_color, "family": font_family},
        },
        legend={
            "font": {"size": legend_font_size, "color": font_color, "family": font_family}
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return dcc.Graph(
        figure=fig_heatmap,
        config={"displayModeBar": False},
        style={
            "position": "absolute",
            "top": f"{top}vh",
            "left": f"{left}vw",
            "width": f"{width_vw}vw",
            "height": f"{height_vh}vh",
            "background": "transparent"
        }
    )


def render_weekly_recovery_graph(
    processed_df: pd.DataFrame,
    player_id: int,
    top: float,
    left: float,
    width_vw: float,
    height_vh: float,
    title: str,
    font_color: str,
    title_font_family: str,
    title_font_size: int,
    axis_font_family: str,
    axis_font_size: int,
    legend_font_size: int,
    color_discrete_map: dict = None
):
    """
    Filters the aggregated DataFrame for the given player and creates a Plotly line graph
    showing the weekly evolution of composite scores. A dropdown menu is added to filter
    the display by metric.

    Args:
        processed_df (pd.DataFrame): Aggregated DataFrame from process_weekly_recovery_data.
        player_id (int): The player's identifier.
        top (float): Vertical position (in vh) of the graph container.
        left (float): Horizontal position (in vw) of the graph container.
        width_vw (float): Width of the container (in vw).
        height_vh (float): Height of the container (in vh).
        title (str): Title of the graph.
        font_color (str): General text color.
        title_font_family (str): Font family for the title.
        title_font_size (int): Font size for the title.
        axis_font_family (str): Font family for the axes and tick labels.
        axis_font_size (int): Font size for the axes.
        legend_font_size (int): Font size for the legend.
        color_discrete_map (dict, optional): Mapping of colors for each metric.

    Returns:
        dcc.Graph: A Dash Graph component containing the Plotly line graph.
    """
    # Filter data for the specified player
    df_player = processed_df[processed_df['player_id'] == player_id].copy()
    df_player = df_player.sort_values(by='week_date', ascending=True)
    
    # Create the line graph with Plotly Express
    fig = px.line(
        df_player,
        x='week_date',
        y='value_composite',
        color='metric',
        markers=True,
        title=title,
        color_discrete_map=color_discrete_map,
        labels={'metric': ''}
    )
    
    # Rename legend entries using a mapping
    legend_mapping = {
        "subjective_baseline_composite": "Subjective",
        "sleep_baseline_composite": "Sleep",
        "soreness_baseline_composite": "Soreness",
        "bio_baseline_composite": "Bio",
        "msk_joint_range_baseline_composite": "Joint Range",
        "msk_load_tolerance_baseline_composite": "Load Tolerance"
    }
    for trace in fig.data:
        trace.name = legend_mapping.get(trace.name, trace.name)
    
    # Update the x-axis to be of date type
    fig.update_xaxes(type='date')
    
    # Create dropdown buttons for filtering metrics
    unique_metrics = df_player['metric'].unique().tolist()
    buttons = []
    buttons.append(dict(
        label="Display All",
        method="update",
        args=[{"visible": [True] * len(unique_metrics)}]
    ))
    for i, metric in enumerate(unique_metrics):
        visible = [False] * len(unique_metrics)
        visible[i] = True
        buttons.append(dict(
            label=f"{legend_mapping.get(metric, metric)}",
            method="update",
            args=[{"visible": visible}]
        ))
    
    # Update layout with styling and dropdown menu
    fig.update_layout(
        title={
            "text": title,
            "font": {"size": title_font_size, "color": font_color, "family": title_font_family},
            "x": 0.5,
            "xanchor": "center",
            "pad": {"t": 0, "b": 0}
        },
        margin=dict(t=40, b=0, l=0, r=0),
        xaxis_title='Week (Date)',
        yaxis_title='Average composite value',
        template='plotly_white',
        font={"color": font_color, "family": axis_font_family},
        xaxis={
            "tickfont": {"size": axis_font_size, "color": font_color, "family": axis_font_family},
        },
        yaxis={
            "tickfont": {"size": axis_font_size, "color": font_color, "family": axis_font_family},
        },
        legend={
            "font": {"size": legend_font_size, "color": font_color, "family": axis_font_family}
        },
        updatemenus=[dict(
            type="dropdown",
            direction="down",
            buttons=buttons,
            showactive=True,
            x=1.1,
            xanchor="right",
            y=1.05,
            yanchor="bottom",
            bgcolor=COLOR_SNOW,
            font={'color':COLOR_DARK_BLUE}
        )],
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_yaxes(range=[-1, 1])

    return dcc.Graph(
        figure=fig,
        config={"displayModeBar": False},
        style={
            "position": "absolute",
            "top": f"{top}vh",
            "left": f"{left}vw",
            "width": f"{width_vw}vw",
            "height": f"{height_vh}vh",
            "background": "transparent"
        }
    )


def render_recovery_summary_info(
    df: pd.DataFrame,
    player_id: int,
    top: float,
    left: float,
    line_spacing: float,
    title_text: str,
    title_font_size: float,
    title_font_family: str,
    title_color: str,
    info_font_size: float,
    info_font_family: str,
    value_font_size: float,
    value_font_family: str,
    positive_color: str,
    negative_color: str
):
    """
    Displays the 7-day average ('avg') for three specific metrics for the given player:
      - "Average EMBOSS" for emboss_baseline_score,
      - "Weighted average Subjective value" for subjective_baseline,
      - "Weighted average Sleep value" for sleep_baseline.
    
    Each value is prefixed with '+' if positive and '-' if negative. The value's text color
    reflects its positivity or negativity.

    Args:
        df (pd.DataFrame): DataFrame containing at least the columns 'player_id', 'metric', and 'avg'.
        player_id (int): The player's identifier.
        top (float): Vertical position (in vh) for the first line.
        left (float): Horizontal position (in vw) for the first line.
        line_spacing (float): Vertical spacing (in vh) between each line.
        title_text (str): Title text displayed at the top.
        title_font_size (float): Font size for the title (in vh).
        title_font_family (str): Font family for the title.
        title_color (str): Color for the title text.
        info_font_size (float): Font size for the label (in vh).
        info_font_family (str): Font family for the label.
        value_font_size (float): Font size for the value (in vh).
        value_font_family (str): Font family for the value.
        positive_color (str): Color for positive values.
        negative_color (str): Color for negative or zero values.

    Returns:
        html.Div: A Dash Div component containing the summary information.
    """
    # Mapping of metrics to desired labels
    label_mapping = {
        "emboss_baseline_score": "Average EMBOSS",
        "subjective_baseline": "Weighted average Subjective value",
        "sleep_baseline": "Weighted average Sleep value"
    }
    
    # Filter data for the selected player
    df_player = df[df['player_id'] == player_id]
    children = []
    current_top = top
    
    # Add title if provided
    if title_text:
        children.append(
            html.Div(
                title_text,
                style={
                    "position": "absolute",
                    "top": f"{current_top}vh",
                    "left": f"{left}vw",
                    "fontSize": f"{title_font_size}vh",
                    "fontFamily": title_font_family,
                    "color": title_color,
                    "textAlign": "left",
                    "whiteSpace": "nowrap"
                }
            )
        )
        current_top += line_spacing
    
    # Create a line for each metric of interest
    for metric in label_mapping.keys():
        row = df_player[df_player['metric'] == metric]
        if row.empty:
            display_value = "N/A"
            value_color = negative_color
        else:
            val = row.iloc[0]['avg']
            if pd.isna(val):
                display_value = "N/A"
                value_color = negative_color
            else:
                val_float = float(val)
                sign = '+' if val_float >= 0 else '-'
                display_value = f"{sign}{abs(val_float):.2f}"
                value_color = positive_color if val_float >= 0 else negative_color
        
        line_content = html.Div(
            [
                html.Span(
                    f"{label_mapping[metric]}: ",
                    style={
                        "fontSize": f"{info_font_size}vh",
                        "fontFamily": info_font_family,
                        "color": "#FFFFFF",
                        "textAlign": "left"
                    }
                ),
                html.Span(
                    display_value,
                    style={
                        "fontSize": f"{value_font_size}vh",
                        "fontFamily": value_font_family,
                        "color": value_color,
                        "textAlign": "left"
                    }
                )
            ],
            style={
                "position": "absolute",
                "top": f"{current_top}vh",
                "left": f"{left}vw",
                "whiteSpace": "nowrap"
            }
        )
        children.append(line_content)
        current_top += line_spacing

    return html.Div(children=children, style={"position": "relative", "width": "100%"})


def render_recovery_radar_chart(
    processed_df: pd.DataFrame,
    player_id: int,
    top: float,
    left: float,
    width_vw: float,
    height_vh: float,
    title: str,
    title_font_size: float,
    title_font_family: str,
    title_color: str,
    background_color: str,
    axis_font_size: float,
    axis_font_family: str,
    axis_font_color: str,
    theta_label_color: str,
    theta_label_fontsize: float,
    theta_label_font_family: str,
    positive_value_color: str,
    negative_value_color: str,
    marker_size: int
) -> dcc.Graph:
    """
    Creates a radar chart (Scatterpolar) displaying the average ('avg') for each metric of interest
    for the given player. The metrics displayed are defined in a preset order and renamed according
    to a mapping. Each value is prefixed with '+' if positive and '-' if negative, with the text color
    reflecting its sign. The legend is hidden, and the angular axis labels are styled accordingly.

    Args:
        processed_df (pd.DataFrame): DataFrame containing at least the columns ['player_id', 'metric', 'avg'].
        player_id (int): The player's identifier.
        top (float): Vertical position (in vh) of the container.
        left (float): Horizontal position (in vw) of the container.
        width_vw (float): Width of the container (in vw).
        height_vh (float): Height of the container (in vh).
        title (str): Title of the chart.
        title_font_size (float): Font size for the title (in vh).
        title_font_family (str): Font family for the title.
        title_color (str): Color of the title.
        background_color (str): Background color for the chart.
        axis_font_size (float): Font size for the radial axis tick labels.
        axis_font_family (str): Font family for the radial axis tick labels.
        axis_font_color (str): Color for the radial axis tick labels.
        theta_label_color (str): Color for the angular axis labels.
        theta_label_fontsize (float): Font size for the angular axis labels.
        theta_label_font_family (str): Font family for the angular axis labels.
        positive_value_color (str): Color for positive values.
        negative_value_color (str): Color for negative or zero values.
        marker_size (int): Size of the markers.

    Returns:
        dcc.Graph: A Dash Graph component containing the radar chart.
    """
    # Define the order of metrics and corresponding labels
    metrics_order = [
        "bio_baseline",
        "msk_joint_range_baseline",
        "msk_load_tolerance_baseline",
        "sleep_baseline",
        "soreness_baseline",
        "subjective_baseline"
    ]
    rename_dict = {
        "bio_baseline": "Bio",
        "msk_joint_range_baseline": "Joint Range",
        "msk_load_tolerance_baseline": "Load Tolerance",
        "sleep_baseline": "Sleep",
        "soreness_baseline": "Soreness",
        "subjective_baseline": "Subjective"
    }
    
    # Filter data for the selected player and metrics of interest
    df_player = processed_df[
        (processed_df['player_id'] == player_id) & 
        (processed_df['metric'].isin(metrics_order))
    ].copy()
    
    # Convert 'avg' to numeric if necessary
    df_player['avg'] = pd.to_numeric(df_player['avg'], errors='coerce')
    
    # Order the metrics
    df_player['metric'] = pd.Categorical(df_player['metric'], categories=metrics_order, ordered=True)
    df_player = df_player.sort_values('metric')
    
    # Create the list of renamed labels
    metrics_labels = [rename_dict[m] for m in df_player['metric']]
    
    # Extract values and format display values with sign
    values = df_player['avg'].tolist()
    colors = []
    display_values = []
    for v in values:
        if pd.isna(v):
            display_values.append("N/A")
            colors.append(negative_value_color)
        else:
            v_float = float(v)
            sign = "+" if v_float >= 0 else "-"
            display_values.append(f"{sign}{abs(v_float):.2f}")
            colors.append(positive_value_color if v_float >= 0 else negative_value_color)
    
    # Create the radar chart trace
    trace_values = go.Scatterpolar(
        r=values,
        theta=metrics_labels,
        mode='lines+markers',
        fill='toself',
        name=f"Player {player_id}",
        marker=dict(color=colors, size=marker_size),
        line=dict(width=0)
    )
    
    fig = go.Figure(data=[trace_values])
    
    # Update layout for the radar chart
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[-1, 1],
                tickfont=dict(size=axis_font_size, color=axis_font_color, family=axis_font_family)
            ),
            angularaxis=dict(
                tickfont=dict(size=theta_label_fontsize, color=theta_label_color, family=theta_label_font_family)
            )
        ),
        margin=dict(t=40, b=10, l=0, r=0),
        showlegend=False,
        title=dict(
            text=title,
            font=dict(size=title_font_size, color=title_color, family=title_font_family),
            x=0.5,
            xanchor="center",
            pad=dict(t=0, b=0)
        ),
        paper_bgcolor=background_color,
        plot_bgcolor=background_color
    )
    
    return dcc.Graph(
        figure=fig,
        config={"displayModeBar": False},
        style={
            "position": "absolute",
            "top": f"{top}vh",
            "left": f"{left}vw",
            "width": f"{width_vw}vw",
            "height": f"{height_vh}vh",
            "background": background_color
        }
    )


def render_colored_square(
    top: float,
    left: float,
    width_vw: float,
    height_vh: float,
    background_color: str
):
    """
    Creates a square (or rectangle) with the specified background color,
    positioned using vw and vh units.

    Args:
        top (float): Vertical position (in vh) of the square.
        left (float): Horizontal position (in vw) of the square.
        width_vw (float): Width of the square (in vw).
        height_vh (float): Height of the square (in vh).
        background_color (str): Background color.

    Returns:
        html.Div: A Dash Div component representing the colored square.
    """
    return html.Div(
        style={
            "position": "absolute",
            "top": f"{top}vh",
            "left": f"{left}vw",
            "width": f"{width_vw}vw",
            "height": f"{height_vh}vh",
            "backgroundColor": background_color
        }
    )