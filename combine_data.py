import numpy as np
import pandas as pd

def main():
    games = pd.read_csv('raw_data/nhl_games_raw.csv')
    stadiums = pd.read_csv('processed_data/nhl_stadiums.csv')

    # Rename columns for consistency
    stadiums = stadiums.rename(columns={"Abbrev": "home_team_abbrev", "Long": "venue_lon", "Lat": "venue_lat"})
    merged = games.merge(stadiums, on="home_team_abbrev", how="left")

    print("Merged DataFrame:")
    print(merged.head())
    merged.to_csv('processed_data/merged_schedule.csv', index=False)

if __name__ == "__main__":
    main()