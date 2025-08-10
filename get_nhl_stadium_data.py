import numpy as np
import pandas as pd

# Load the abbreviations for NHL teams

def main():
    stadium_df = pd.read_csv('raw_data/stadiums.csv')
    abbrev_map_df = pd.read_csv('raw_data/team_abbrevs.csv')
    nhl_stadium_df = stadium_df[stadium_df['League'] == 'NHL'].reset_index(drop=True)
    
    # TODO: need to get the abbreviation for each team and merge on full team name

    nhl_stadium_df = nhl_stadium_df.merge(abbrev_map_df, on="Team", how="left")
    nhl_stadium_df.to_csv('processed_data/nhl_stadiums.csv', index=False)
    print("Successfully saved NHL stadium data with team abbreviations.")

if __name__ == "__main__":
    main()