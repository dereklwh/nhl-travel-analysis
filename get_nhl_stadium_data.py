import numpy as np
import pandas as pd

'''
Takes in kaggle stadium data and filters for NHL stadiums. Also manually inserts row for Utah Mammoth stadium.
input: raw_data/stadiums.csv
output: processed_data/nhl_stadiums.csv
'''

def main():
    stadium_df = pd.read_csv('raw_data/stadiums.csv')
    abbrev_map_df = pd.read_csv('raw_data/team_abbrevs.csv')
    nhl_stadium_df = stadium_df[stadium_df['League'] == 'NHL'].reset_index(drop=True)
    
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
    nhl_stadium_df = nhl_stadium_df.rename(columns={"Team": "venue_team"})

    nhl_stadium_df.to_csv('processed_data/nhl_stadiums.csv', index=False)
    print("Successfully saved NHL stadium data with team abbreviations.")

if __name__ == "__main__":
    main()