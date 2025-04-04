import pandas as pd
from datetime import datetime
import numpy as np
import random

# =============================================================================
# Normal Distribution Parameters for Distance (in meters)
# =============================================================================

mean_distance = 8000
std_distance = 2500
min_val_distance = 1000
max_val_distance = 16000

# =============================================================================
# Utility Functions
# =============================================================================

def seconds_to_hms(sec: float) -> str:
    """
    Convert seconds into HH:MM:SS format.
    
    Args:
        sec (float): The number of seconds.
    
    Returns:
        str: Time formatted as HH:MM:SS.
    """
    sec = int(round(sec))
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

# =============================================================================
# Function to Fill DataFrame with Random GPS Data
# =============================================================================

def fill_random_gps_data(df_empty: pd.DataFrame, player_id: int, seed: int = None) -> pd.DataFrame:
    """
    Randomly fill a DataFrame (based on df_empty) for a given player_id.
    
    For each row, with a probability of 1/7, all columns (except for specific columns)
    are set to 0. Otherwise, columns are filled with random values as follows:
      - distance: random number from a normal distribution (truncated between 1000 and 16000)
      - distance_over_21: between 0 and 5% of distance
      - distance_over_24: between 0 and 3% of distance
      - distance_over_27: between 0 and 2% of distance
      - accel_decel_over_2_5: between 0 and 325
      - accel_decel_over_3_5: between 0 and 120
      - accel_decel_over_4_5: between 0 and 45
      - day_duration (in minutes): if opposition_full is non-empty, between 0.5% and 1.5% of distance;
                                      otherwise, between 1% and 3% of distance
      - peak_speed: between 25 and 35
      - hr_zone_1_hms: between 15% and 25% of day_duration (converted to seconds) formatted as HH:MM:SS
      - hr_zone_2_hms: between 15% and 35% of day_duration (converted to seconds) formatted as HH:MM:SS
      - hr_zone_3_hms: between 17% and 20% of day_duration (converted to seconds) formatted as HH:MM:SS
      - hr_zone_4_hms: between 12% and 15% of day_duration (converted to seconds) formatted as HH:MM:SS
      - hr_zone_5_hms: between 0 and 120 seconds, formatted as HH:MM:SS

    Args:
        df_empty (pd.DataFrame): Base DataFrame with columns to keep.
        player_id (int): The player's identifier.
        seed (int, optional): Seed for random generation. Defaults to None.
    
    Returns:
        pd.DataFrame: DataFrame filled with random values.
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    df = df_empty.copy()
    df["player_id"] = player_id
    # Columns to keep (will not be modified)
    cols_keep = {"date", "opposition_code", "opposition_full", "player_id", "md_plus_code", "md_minus_code", "season"}

    def fill_row(row: pd.Series) -> pd.Series:
        # With a probability of 1/7, fill non-kept columns with 0
        if random.random() < 1 / 7:
            for col in row.index:
                if col not in cols_keep:
                    row[col] = 0
            return row

        # Otherwise, fill the row with random values
        
        # Generate a random distance based on a normal distribution
        distance = np.random.normal(loc=mean_distance, scale=std_distance, size=1)[0]
        # Truncate the value between min_val and max_val
        distance = max(min_val_distance, min(distance, max_val_distance))
        
        row["distance"] = distance
        row["distance_over_21"] = random.uniform(0, 0.05) * distance
        row["distance_over_24"] = random.uniform(0, 0.03) * distance
        row["distance_over_27"] = random.uniform(0, 0.02) * distance

        row["accel_decel_over_2_5"] = random.uniform(0, 325)
        row["accel_decel_over_3_5"] = random.uniform(0, 120)
        row["accel_decel_over_4_5"] = random.uniform(0, 45)

        # Calculate day_duration in minutes based on presence of opponent name
        opponent = str(row["opposition_full"]).strip()
        if opponent:
            day_duration = random.uniform(0.005, 0.015) * distance
        else:
            day_duration = random.uniform(0.01, 0.03) * distance
        row["day_duration"] = day_duration

        row["peak_speed"] = random.uniform(25, 35)

        # Convert day_duration (in minutes) to seconds for heart rate zone calculations
        day_duration_sec = day_duration * 60
        row["hr_zone_1_hms"] = seconds_to_hms(random.uniform(0.15, 0.25) * day_duration_sec)
        row["hr_zone_2_hms"] = seconds_to_hms(random.uniform(0.15, 0.35) * day_duration_sec)
        row["hr_zone_3_hms"] = seconds_to_hms(random.uniform(0.17, 0.20) * day_duration_sec)
        row["hr_zone_4_hms"] = seconds_to_hms(random.uniform(0.12, 0.15) * day_duration_sec)
        row["hr_zone_5_hms"] = seconds_to_hms(random.uniform(0, 120))
        return row

    df_filled = df.apply(fill_row, axis=1)

    # Reorder columns as desired
    final_cols = [
        "player_id", "date", "opposition_code", "opposition_full", "md_plus_code",
        "md_minus_code", "season", "distance", "distance_over_21", "distance_over_24",
        "distance_over_27", "accel_decel_over_2_5", "accel_decel_over_3_5", "accel_decel_over_4_5",
        "day_duration", "peak_speed", "hr_zone_1_hms", "hr_zone_2_hms", "hr_zone_3_hms",
        "hr_zone_4_hms", "hr_zone_5_hms"
    ]
    return df_filled[final_cols]

# =============================================================================
# Main Function: Generate Augmented GPS Data
# =============================================================================

def main():
    # Read raw CSV data
    df_cfc_gps_data_raw = pd.read_csv("data/cfc_gps_data_raw.csv", sep=",")

    final_cols = [
        "player_id", "date", "opposition_code", "opposition_full", "md_plus_code",
        "md_minus_code", "season", "distance", "distance_over_21", "distance_over_24",
        "distance_over_27", "accel_decel_over_2_5", "accel_decel_over_3_5", "accel_decel_over_4_5",
        "day_duration", "peak_speed", "hr_zone_1_hms", "hr_zone_2_hms", "hr_zone_3_hms",
        "hr_zone_4_hms", "hr_zone_5_hms"
    ]

    # Assign player_id = 1 for the original dataset
    df_cfc_gps_data_raw["player_id"] = 1
    df_cfc_gps_data_raw = df_cfc_gps_data_raw[final_cols]

    # Create an empty DataFrame for synthetic data generation
    cols_to_keep = ["date", "opposition_code", "opposition_full", "md_plus_code", "md_minus_code", "season"]
    df_cfc_gps_data_empty = df_cfc_gps_data_raw.copy()
    for col in df_cfc_gps_data_raw.columns:
        if col not in cols_to_keep:
            df_cfc_gps_data_empty[col] = ""

    # Generate synthetic data for player IDs 2 to 5
    random_dfs = []
    for player_id in range(2, 6):
        df_temp = fill_random_gps_data(df_cfc_gps_data_empty, player_id, seed=player_id)
        random_dfs.append(df_temp)

    df_cfc_gps_data_random = pd.concat(random_dfs, ignore_index=True)
    df_cfc_gps_data_augmented = pd.concat([df_cfc_gps_data_raw, df_cfc_gps_data_random], ignore_index=True)

    # Save the augmented DataFrame as CSV
    df_cfc_gps_data_augmented.to_csv("data/cfc_gps_data_augmented.csv", index=False)

if __name__ == "__main__":
    main()
