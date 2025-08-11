import numpy as np
import pandas as pd

# Load the abbreviations for NHL teams

def main():
    stadium_df = pd.read_csv('raw_data/stadiums.csv')
    abbrev_map_df = pd.read_csv('raw_data/team_abbrevs.csv')
    nhl_stadium_df = stadium_df[stadium_df['League'] == 'NHL'].reset_index(drop=True)
    
    # TODO: need to get the abbreviation for each team and merge on full team name

    # HARD CODE: UTAH ARENA
    # https://www.latlong.net/place/vivint-arena-ut-usa-32358.html
    utah_row = pd.DataFrame({
        "Team": ["Utah Mammoth"],
        "League": ["NHL"],
        "Division": ["Central"],
        "Lat": [40.7684],
        "Long": [-111.9016],
    })
    nhl_stadium_df = pd.concat([nhl_stadium_df, utah_row], ignore_index=True)
    nhl_stadium_df = nhl_stadium_df.merge(abbrev_map_df, on="Team", how="left")

    # rename Team column to venue_team
    nhl_stadium_df = nhl_stadium_df.rename(columns={"Team": "venue_team"})

    nhl_stadium_df.to_csv('processed_data/nhl_stadiums.csv', index=False)
    print("Successfully saved NHL stadium data with team abbreviations.")

if __name__ == "__main__":
    main()