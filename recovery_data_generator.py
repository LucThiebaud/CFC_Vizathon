import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# =============================================================================
# Helper Functions
# =============================================================================

def get_season(dt):
    """
    Determine the season name based on the date.
    
    Assumes season "2023/2024" runs from 01/07/2023 to 30/06/2024,
    and season "2024/2025" runs from 01/07/2024 to 13/03/2025.
    
    Args:
        dt: A pandas Timestamp.
    
    Returns:
        str: The season name.
    """
    return "2023/2024" if dt < pd.Timestamp("2024-07-01") else "2024/2025"

def generate_composite_value():
    """
    Generate a composite value from a normal distribution.
    
    Returns:
        float: A value drawn from a normal distribution (mean=0, std=0.2), clipped between -1 and 1.
    """
    val = np.random.normal(0, 0.2)
    return np.clip(val, -1, 1)

def generate_completeness_value():
    """
    Generate a completeness value uniformly between 0 and 1.
    
    Returns:
        float: A random value from a uniform distribution over [0, 1].
    """
    return np.random.uniform(0, 1)

# =============================================================================
# Generate Synthetic Recovery Data
# =============================================================================

def generate_synthetic_data(player_id, seed=42):
    """
    Generate synthetic recovery data for a given player.
    
    For each day in the date range, synthetic metrics are generated for various groups.
    Each group has its own composite and completeness metrics. For the 'emboss' metric,
    the composite value is calculated as a weighted average of the other groups' values.
    
    Args:
        player_id (int): The player's identifier.
        seed (int, optional): Random seed for reproducibility. Defaults to 42.
    
    Returns:
        pd.DataFrame: A DataFrame containing synthetic recovery data.
    """
    np.random.seed(seed)
    
    # Define the date range (621 days)
    start_date = pd.Timestamp("2023-07-02")
    end_date = pd.Timestamp("2025-03-13")
    date_range = pd.date_range(start_date, end_date, freq="D")
    
    # Synthetic parameters for each metric group.
    metrics_info = {
        "bio": {
             "composite_metric": "bio_baseline_composite",
             "completeness_metric": "bio_baseline_completeness",
             "p": 48/621,
             "category": "bio"
        },
        "emboss": {
             "composite_metric": "emboss_baseline_score",
             "p": 371/621,
             "category": "total"
        },
        "msk_joint_range": {
             "composite_metric": "msk_joint_range_baseline_composite",
             "completeness_metric": "msk_joint_range_baseline_completeness",
             "p": 2/7,
             "category": "msk_joint_range"
        },
        "msk_load_tolerance": {
             "composite_metric": "msk_load_tolerance_baseline_composite",
             "completeness_metric": "msk_load_tolerance_baseline_completeness",
             "p": 2/7,
             "category": "msk_load_tolerance"
        },
        "sleep": {
             "composite_metric": "sleep_baseline_composite",
             "completeness_metric": "sleep_baseline_completeness",
             "p": 9/10,
             "category": "sleep"
        },
        "soreness": {
             "composite_metric": "soreness_baseline_composite",
             "completeness_metric": "soreness_baseline_completeness",
             "p": 319/621,
             "category": "soreness"
        },
        "subjective": {
             "composite_metric": "subjective_baseline_composite",
             "completeness_metric": "subjective_baseline_completeness",
             "p": 9/12,
             "category": "subjective"
        }
    }
    
    rows = []
    for dt in date_range:
        season = get_season(dt)
        day_values = []  # List of tuples (composite, completeness) for later emboss calculation
        
        # Process each metric group (except emboss)
        for key, info in metrics_info.items():
            if key == "emboss":
                continue
            
            if np.random.rand() < info["p"]:
                comp_val = generate_composite_value()
                comp_complete = generate_completeness_value()
            else:
                comp_val = np.nan
                comp_complete = 0
            
            rows.append({
                "player_id": player_id,
                "sessionDate": dt,
                "seasonName": season,
                "metric": info["composite_metric"],
                "category": info["category"],
                "value": comp_val
            })
            rows.append({
                "player_id": player_id,
                "sessionDate": dt,
                "seasonName": season,
                "metric": info["completeness_metric"],
                "category": info["category"],
                "value": comp_complete
            })
            day_values.append((comp_val, comp_complete))
        
        # Calculate emboss as the weighted average of composites by their completeness
        numerator = 0
        denominator = 0
        for comp_val, comp_complete in day_values:
            if not np.isnan(comp_val):
                numerator += comp_val * comp_complete
            denominator += comp_complete
        emboss_value = numerator / denominator if denominator > 0 else np.nan
        
        rows.append({
            "player_id": player_id,
            "sessionDate": dt,
            "seasonName": season,
            "metric": metrics_info["emboss"]["composite_metric"],
            "category": metrics_info["emboss"]["category"],
            "value": emboss_value
        })
    
    df_synthetic = pd.DataFrame(rows)
    df_synthetic.sort_values(["sessionDate", "metric"], inplace=True)
    return df_synthetic

# =============================================================================
# Main Function to Generate Augmented Recovery Data
# =============================================================================

def main():
    # Read raw CSV data for player 1
    df_cfc_recovery_raw = pd.read_csv("data/cfc_recovery_status_data_raw.csv", sep=",")
    df_cfc_recovery_raw.insert(0, 'player_id', 1)
    
    # Generate synthetic data for players 2, 3, 4, and 5 (using seed=player_id)
    synth_dfs = []
    for player_id in [2, 3, 4, 5]:
        df_synth = generate_synthetic_data(player_id=player_id, seed=player_id)
        synth_dfs.append(df_synth)
    
    df_synthetic_all = pd.concat(synth_dfs, ignore_index=True)
    # Format date as DD/MM/YYYY
    df_synthetic_all['sessionDate'] = pd.to_datetime(df_synthetic_all['sessionDate']).dt.strftime('%d/%m/%Y')
    
    # Concatenate real data (player 1) with synthetic data
    df_cfc_recovery_augmented = pd.concat([df_cfc_recovery_raw, df_synthetic_all], ignore_index=True)
    
    # Save the final augmented DataFrame as CSV
    df_cfc_recovery_augmented.to_csv("data/cfc_recovery_status_data_augmented.csv", index=False)

if __name__ == "__main__":
    main()
