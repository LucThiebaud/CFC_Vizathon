import pandas as pd
from datetime import datetime, timedelta

# =============================================================================
# Load Raw Data
# =============================================================================

df_agg_player_matches = pd.read_csv('data/agg_player_matches.csv', sep=';')
df_agg_player_season = pd.read_csv('data/agg_player_season.csv', sep=';')
df_matches = pd.read_csv('data/matches.csv', sep=';')
df_ref_competitions = pd.read_csv('data/ref_competitions.csv', sep=';')
df_ref_countries = pd.read_csv('data/ref_country.csv', sep=';')
df_ref_players = pd.read_csv('data/ref_player.csv', sep=';')
df_ref_teams = pd.read_csv('data/ref_team.csv', sep=';')
df_cfc_gps_data_augmented = pd.read_csv('data/cfc_gps_data_augmented.csv', sep=',')
df_injuries_histo = pd.read_csv('data/injuries_histo.csv', sep=';')
df_cfc_recovery_augmented = pd.read_csv('data/cfc_recovery_status_data_augmented.csv', sep=',')

# =============================================================================
# Construct df_player_resume
# =============================================================================

df_player_resume = pd.merge(df_ref_players, df_agg_player_season, on='player_id', how='left')
df_player_resume = pd.merge(
    df_player_resume,
    df_ref_countries[['country_id', 'url_picture']].rename(columns={'url_picture': 'url_picture_country'}),
    on='country_id',
    how='left'
)
df_player_resume['birthdate'] = pd.to_datetime(df_player_resume['birthdate'], format='%Y/%m/%d')
today = pd.Timestamp.today()
df_player_resume['age'] = df_player_resume['birthdate'].apply(
    lambda x: today.year - x.year - ((today.month, today.day) < (x.month, x.day))
)

# =============================================================================
# Construct DataFrame for Last 5 Matches
# =============================================================================

df_player_matches = pd.merge(
    df_matches,
    df_agg_player_matches,
    on='match_id',
    how='left'
)
df_player_matches['is_home'] = df_player_matches['home_team_id'] == 1
df_player_matches['opponent_id'] = df_player_matches.apply(
    lambda row: row['away_team_id'] if row['is_home'] else row['home_team_id'],
    axis=1
)
df_player_matches = df_player_matches.merge(
    df_ref_teams[['team_id', 'team_name', 'url_picture']],
    left_on='opponent_id',
    right_on='team_id',
    how='left'
)
df_result = df_player_matches[[
    'match_id', 'match_date_x', 'player_id', 'team_name',
    'is_home', 'starter_group', 'minutes_played', 'url_picture',
    'home_team_score', 'away_team_score', 'goals', 'assists'
]].rename(columns={
    'match_date_x': 'match_date',
    'team_name': 'opponent_name',
    'url_picture': 'opponent_url_picture'
})
df_result['match_date'] = pd.to_datetime(df_result['match_date'], format='%Y/%m/%d')
df_result = df_result.sort_values(by='match_date', ascending=False).reset_index(drop=True)

def get_result_and_score(row: pd.Series) -> pd.Series:
    """Determine match result (W, D, L) and format the score."""
    if row['is_home']:
        team_score = row['home_team_score']
        opp_score = row['away_team_score']
    else:
        team_score = row['away_team_score']
        opp_score = row['home_team_score']

    if pd.isna(row['home_team_score']) or pd.isna(row['away_team_score']):
        result = ""
        score = ""
    else:
        team_score = int(team_score)
        opp_score = int(opp_score)
        home_score = int(row['home_team_score'])
        away_score = int(row['away_team_score'])
        result = 'W' if team_score > opp_score else 'D' if team_score == opp_score else 'L'
        score = f"{home_score} - {away_score}"
    return pd.Series({'result': result, 'score': score})

df_result[['result', 'score']] = df_result.apply(get_result_and_score, axis=1)
last_5_match_ids = df_result.drop_duplicates(subset='match_id').head(5)['match_id'].tolist()
df_last_5_matches = df_result[df_result['match_id'].isin(last_5_match_ids)]

# =============================================================================
# Construct DataFrame for GPS Data
# =============================================================================

# 1) Convert injury dates
df_injuries_histo['injury_date'] = pd.to_datetime(df_injuries_histo['injury_date'], format='%d/%m/%Y')
df_injuries_histo['return_date'] = pd.to_datetime(df_injuries_histo['return_date'], format='%d/%m/%Y')

# 2) Prepare the GPS DataFrame
df_cfc_gps_data_processed = df_cfc_gps_data_augmented.copy()
df_cfc_gps_data_processed['date'] = pd.to_datetime(df_cfc_gps_data_processed['date'], format='%d/%m/%Y')
cutoff_date_sup = pd.to_datetime('13/03/2025', format='%d/%m/%Y')
cutoff_date_inf = pd.to_datetime('01/08/2023', format='%d/%m/%Y')
df_cfc_gps_data_processed = df_cfc_gps_data_processed[
    (df_cfc_gps_data_processed['date'] <= cutoff_date_sup) &
    (df_cfc_gps_data_processed['date'] >= cutoff_date_inf)
]
exclude_cols = ['player_id', 'date', 'opposition_code', 'opposition_full', 'md_plus_code', 'md_minus_code', 'season']
cols_to_update = [col for col in df_cfc_gps_data_processed.columns if col not in exclude_cols]
hr_zone_cols = [col for col in cols_to_update if col.startswith("hr_zone")]
other_cols = [col for col in cols_to_update if col not in hr_zone_cols]
for col in ["injury_date", "return_date", "body_part", "injury_name", "is_injury_active"]:
    if col not in df_cfc_gps_data_processed.columns:
        df_cfc_gps_data_processed[col] = None

# 3) Update data for injuries
for idx, injury in df_injuries_histo.iterrows():
    mask = (
        (df_cfc_gps_data_processed['player_id'] == injury['player_id']) &
        (df_cfc_gps_data_processed['date'] > injury['injury_date']) &
        (df_cfc_gps_data_processed['date'] < injury['return_date'])
    )
    df_cfc_gps_data_processed.loc[mask, other_cols] = 0
    df_cfc_gps_data_processed.loc[mask, hr_zone_cols] = "00:00:00"
    df_cfc_gps_data_processed.loc[mask, "injury_date"] = injury["injury_date"]
    df_cfc_gps_data_processed.loc[mask, "return_date"] = injury["return_date"]
    df_cfc_gps_data_processed.loc[mask, "body_part"] = injury["body_part"]
    df_cfc_gps_data_processed.loc[mask, "injury_name"] = injury["injury_name"]
    df_cfc_gps_data_processed.loc[mask, "is_injury_active"] = injury["is_injury_active"]

# 4) Compute TRIMP Edwards
df_cfc_gps_data_processed['trimp_edwards'] = (
    pd.to_timedelta(df_cfc_gps_data_processed['hr_zone_1_hms']).dt.total_seconds() / 60 * 1 +
    pd.to_timedelta(df_cfc_gps_data_processed['hr_zone_2_hms']).dt.total_seconds() / 60 * 2 +
    pd.to_timedelta(df_cfc_gps_data_processed['hr_zone_3_hms']).dt.total_seconds() / 60 * 3 +
    pd.to_timedelta(df_cfc_gps_data_processed['hr_zone_4_hms']).dt.total_seconds() / 60 * 4 +
    pd.to_timedelta(df_cfc_gps_data_processed['hr_zone_5_hms']).dt.total_seconds() / 60 * 5
)
df_cfc_gps_data_processed['date'] = pd.to_datetime(df_cfc_gps_data_processed['date'], format='%d/%m/%Y')

# 5) Compute acute (7d) and chronic (28d) loads for each player
dfs = []
for player_id in df_cfc_gps_data_processed['player_id'].unique():
    df_temp = df_cfc_gps_data_processed[df_cfc_gps_data_processed['player_id'] == player_id].copy()
    df_temp = df_temp.sort_values('date')
    df_temp['trimp_edwards_acute_load'] = df_temp.rolling(window='7d', on='date')['trimp_edwards'].sum()
    df_temp['trimp_edwards_chronic_load'] = df_temp.rolling(window='28d', on='date')['trimp_edwards'].sum() / 4
    df_temp = df_temp.reset_index(drop=True)
    dfs.append(df_temp)
df_cfc_gps_data_processed = pd.concat(dfs, ignore_index=True)

# 6) Compute ACWR (Acute:Chronic Workload Ratio)
df_cfc_gps_data_processed['acwr'] = (
    df_cfc_gps_data_processed['trimp_edwards_acute_load'] /
    df_cfc_gps_data_processed['trimp_edwards_chronic_load']
).fillna(0)

# 7) Merge with df_ref_teams to get opponent logo
df_cfc_gps_data_processed = df_cfc_gps_data_processed.merge(
    df_ref_teams[['team_name', 'url_picture']],
    left_on='opposition_full',
    right_on='team_name',
    how='left'
)
df_cfc_gps_data_processed = df_cfc_gps_data_processed.rename(columns={'url_picture': 'url_logo_opponent'})
df_cfc_gps_data_processed = df_cfc_gps_data_processed.drop(columns='team_name')

# 8) Conversions and label creation
df_cfc_gps_data_processed["distance_km"] = df_cfc_gps_data_processed["distance"] / 1000
df_cfc_gps_data_processed["opposition_text"] = df_cfc_gps_data_processed["opposition_full"].apply(
    lambda x: f"Opponent: {x}<br>" if pd.notna(x) and str(x).strip() != "" else ""
)
df_cfc_gps_data_processed["distance_label"] = df_cfc_gps_data_processed["opposition_full"].apply(
    lambda x: "Match distance (km): " if pd.notna(x) and str(x).strip() != "" else "Session distance (km): "
)
df_cfc_gps_data_processed["duration_label"] = df_cfc_gps_data_processed["opposition_full"].apply(
    lambda x: "Time played (minutes): " if pd.notna(x) and str(x).strip() != "" else "Session duration (minutes): "
)
df_cfc_gps_data_processed["load_label"] = df_cfc_gps_data_processed["opposition_full"].apply(
    lambda x: "Match load (TRIMP): " if pd.notna(x) and str(x).strip() != "" else "Session load (TRIMP): "
)
df_cfc_gps_data_processed["injury_label"] = df_cfc_gps_data_processed["is_injury_active"].apply(
    lambda x: "Status: INJURED<br>" if pd.notna(x) and str(x).strip() != "" else "Status: FIT<br>"
)
df_cfc_gps_data_processed["injury_date_label"] = df_cfc_gps_data_processed["injury_date"].apply(
    lambda d: f"From {d.strftime('%Y/%m/%d')}<br>" if pd.notna(d) else ""
)
df_cfc_gps_data_processed["return_date_label"] = df_cfc_gps_data_processed["return_date"].apply(
    lambda d: f"To {d.strftime('%Y/%m/%d')}<br>" if pd.notna(d) else ""
)
df_cfc_gps_data_processed["body_part_label"] = df_cfc_gps_data_processed["body_part"].apply(
    lambda x: f"Body part: {x}<br>" if pd.notna(x) and str(x).strip() != "" else ""
)
df_cfc_gps_data_processed["injury_name_label"] = df_cfc_gps_data_processed["injury_name"].apply(
    lambda x: f"Injury: {x}<br>" if pd.notna(x) and str(x).strip() != "" else ""
)

# 9) Cap match time at 90 minutes for consistency
mask = (
    df_cfc_gps_data_processed["opposition_full"].notna() &
    (df_cfc_gps_data_processed["opposition_full"].str.strip() != "") &
    (df_cfc_gps_data_processed["day_duration"] > 90)
)
df_cfc_gps_data_processed.loc[mask, "day_duration"] = 90

# =============================================================================
# Construct DataFrame for Recovery Data (Graph 1 - Daily Recovery)
# =============================================================================

if df_cfc_recovery_augmented['sessionDate'].dtype == 'object':
    df_cfc_recovery_augmented['sessionDate'] = pd.to_datetime(df_cfc_recovery_augmented['sessionDate'], format='%d/%m/%Y')
composite_metrics = [
    'subjective_baseline_composite',
    'sleep_baseline_composite',
    'soreness_baseline_composite'
]
completeness_metrics = [
    'subjective_baseline_completeness',
    'sleep_baseline_completeness',
    'soreness_baseline_completeness'
]
df_composite = df_cfc_recovery_augmented[df_cfc_recovery_augmented['metric'].isin(composite_metrics)].copy()
df_completeness = df_cfc_recovery_augmented[df_cfc_recovery_augmented['metric'].isin(completeness_metrics)].copy()
df_composite['metric_base'] = df_composite['metric'].str.replace('_baseline_composite', '')
df_completeness['metric_base'] = df_completeness['metric'].str.replace('_baseline_completeness', '')
df_merged = pd.merge(
    df_composite,
    df_completeness[['player_id', 'sessionDate', 'seasonName', 'category', 'value', 'metric_base']],
    on=['player_id', 'sessionDate', 'seasonName', 'category', 'metric_base'],
    how='left',
    suffixes=('_composite', '_completeness')
)
df_merged_filtered = df_merged[df_merged['value_completeness'] > 0.2]
df_cfc_recovery_data_processed_daily = df_merged_filtered.pivot_table(
    index=['player_id', 'sessionDate', 'seasonName'],
    columns='metric',
    values='value_composite'
).reset_index()

# =============================================================================
# Construct DataFrame for Recovery Data (Graph 2 - Heatmap)
# =============================================================================

if df_cfc_recovery_augmented['sessionDate'].dtype == 'object':
    df_cfc_recovery_augmented['sessionDate'] = pd.to_datetime(df_cfc_recovery_augmented['sessionDate'], format='%d/%m/%Y')
df_heatmap = df_cfc_recovery_augmented[df_cfc_recovery_augmented['metric'] == 'emboss_baseline_score'].dropna().copy()
df_heatmap['Month'] = df_heatmap['sessionDate'].dt.strftime('%B %Y')
df_heatmap['Day'] = df_heatmap['sessionDate'].dt.day
df_cfc_recovery_data_processed_heatmap = df_heatmap.pivot_table(
    index=['player_id', 'Month', 'seasonName'],
    columns='Day',
    values='value',
    aggfunc='mean'
).reset_index()

# =============================================================================
# Construct DataFrame for Recovery Data (Graph 3 - Weekly Recovery)
# =============================================================================

df = df_cfc_recovery_augmented.copy()
if df['sessionDate'].dtype == 'object':
    df['sessionDate'] = pd.to_datetime(df['sessionDate'], format='%d/%m/%Y')
desired_composite_metrics = [
    'bio_baseline_composite',
    'msk_joint_range_baseline_composite',
    'msk_load_tolerance_baseline_composite',
    'soreness_baseline_composite',
    'subjective_baseline_composite',
    'sleep_baseline_composite'
]
desired_completeness_metrics = [m.replace('composite', 'completeness') for m in desired_composite_metrics]
df_composite = df[df['metric'].isin(desired_composite_metrics)].copy()
df_completeness = df[df['metric'].isin(desired_completeness_metrics)].copy()
df_composite['metric_base'] = df_composite['metric'].str.replace('_baseline_composite', '')
df_completeness['metric_base'] = df_completeness['metric'].str.replace('_baseline_completeness', '')
df_merged = pd.merge(
    df_composite,
    df_completeness[['sessionDate', 'seasonName', 'category', 'value', 'metric_base']],
    on=['sessionDate', 'seasonName', 'category', 'metric_base'],
    how='left',
    suffixes=('_composite', '_completeness')
)
df_merged = df_merged[df_merged['value_completeness'] > 0.2].copy()
df_merged['iso_year'] = df_merged['sessionDate'].dt.isocalendar().year
df_merged['iso_week'] = df_merged['sessionDate'].dt.isocalendar().week
df_merged['year_week'] = df_merged['iso_year'].astype(str) + '-' + df_merged['iso_week'].astype(str).str.zfill(2)
df_weekly_agg = df_merged.groupby(['player_id', 'year_week', 'seasonName', 'metric'])['value_composite'].mean().reset_index()
df_cfc_recovery_data_processed_weekly = df_weekly_agg.sort_values(by='year_week', ascending=True)
df_cfc_recovery_data_processed_weekly['week_date'] = pd.to_datetime(df_weekly_agg['year_week'] + '-1', format='%G-%V-%u')

# =============================================================================
# Construct DataFrame for Recovery Data (Last 7 Days)
# =============================================================================

df = df_cfc_recovery_augmented.copy()
df['sessionDate'] = pd.to_datetime(df['sessionDate'], format='%d/%m/%Y')
end_date = pd.Timestamp('2025-03-13')
start_date = end_date - timedelta(days=6)
df_last7 = df[(df['sessionDate'] >= start_date) & (df['sessionDate'] <= end_date)].copy()

def extract_base_metric(metric):
    if metric.endswith("_composite"):
        return metric[:-len("_composite")]
    elif metric.endswith("_completeness"):
        return metric[:-len("_completeness")]
    else:
        return metric

def extract_metric_type(metric):
    if metric.endswith("_composite"):
        return "composite"
    elif metric.endswith("_completeness"):
        return "completeness"
    else:
        return "simple"

df_last7['base_metric'] = df_last7['metric'].apply(extract_base_metric)
df_last7['metric_type'] = df_last7['metric'].apply(extract_metric_type)
weighted_df = df_last7[df_last7['metric_type'].isin(["composite", "completeness"])].copy()
simple_df = df_last7[df_last7['metric_type'] == "simple"].copy()
weighted_pivot = weighted_df.pivot_table(
    index=['player_id', 'sessionDate', 'base_metric', 'category'],
    columns='metric_type',
    values='value'
).reset_index()

weighted_group = weighted_pivot.groupby(['player_id', 'base_metric'])
def compute_weighted_avg(group):
    group = group.dropna(subset=['completeness'])
    group = group[~((group['completeness'] == 0) & (group['composite'].isna()))]
    group['composite_filled'] = group['composite'].fillna(0)
    numerator = (group['composite_filled'] * group['completeness']).sum()
    denominator = group['completeness'].sum()
    return numerator / denominator if denominator != 0 else None

weighted_result = weighted_group.apply(compute_weighted_avg).reset_index(name='weighted_avg')
simple_group = simple_df.groupby(['player_id', 'base_metric']).agg(simple_avg=('value', 'mean')).reset_index()
weighted_result['avg_type'] = 'weighted'
simple_group['avg_type'] = 'simple'
weighted_result = weighted_result.rename(columns={'base_metric': 'metric'})
simple_group = simple_group.rename(columns={'base_metric': 'metric'})
df_cfc_recovery_last_7d = pd.concat([
    weighted_result[['player_id', 'metric', 'weighted_avg', 'avg_type']],
    simple_group[['player_id', 'metric', 'simple_avg', 'avg_type']]
], ignore_index=True)
def format_value(row):
    val = row['weighted_avg'] if row['avg_type'] == 'weighted' else row['simple_avg']
    return '/' if pd.isna(val) else f"{val:.2f}"
df_cfc_recovery_last_7d['avg'] = df_cfc_recovery_last_7d.apply(format_value, axis=1)
df_cfc_recovery_last_7d = df_cfc_recovery_last_7d.drop(columns=['weighted_avg', 'simple_avg'])

# =============================================================================
# End of Data Preparation
# =============================================================================