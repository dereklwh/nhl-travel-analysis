import numpy as np
import pandas as pd
import os

'''
This script combines all NHL raw game data files into a single DataFrame,
merges it with stadium data, and cleans up the venue information for neutral site games.

Input: all nhl raw files in raw_data directory
Output: merged_data.csv in processed_data directory
'''

def combine_raw_files() -> pd.DataFrame:
    # get all games that start with "nhl_games_raw..." in the raw_data directory
    raw_data_dir = 'raw_data'
    game_files = [f for f in os.listdir(raw_data_dir) if f.startswith('nhl_games_raw_') and f.endswith('.csv')]

    # concat them into a single dataframe
    games_list = []
    for file in game_files:
        file_path = os.path.join(raw_data_dir, file)
        df = pd.read_csv(file_path)
        games_list.append(df)

    all_games = pd.concat(games_list, ignore_index=True)
    return all_games
    # merge them with the stadiums data on home_team_abbrev

def main():
    games = combine_raw_files()
    stadiums = pd.read_csv('processed_data/nhl_stadiums.csv')

    # Rename columns for consistency
    stadiums = stadiums.rename(columns={"Abbrev": "home_team_abbrev", "Long": "venue_lon", "Lat": "venue_lat"})
    merged = games.merge(stadiums, on="home_team_abbrev", how="left")

    # manually update venue for neutral site games
    # O2 Czech Republic, Ohio Stadium, Nokia Arena, Wrigley Field
    # https://latitude.to/articles-by-country/cz/czech-republic/7388/o2-arena-prague
    # https://www.latlong.net/place/ohio-stadium-columbus-oh-usa-23020.html
    # https://nn.wikipedia.org/wiki/Nokia_Arena
    # https://www.latlong.net/place/wrigley-field-chicago-il-usa-10416.html
    
    # Clean data
    special_arenas_df = pd.DataFrame(
        {'venue': ['O2 Czech Republic', 'Ohio Stadium', 'Nokia Arena', 'Wrigley Field'],
        'venue_lat': [50.1029, 40.0016, 61.4936, 41.9484],
         'venue_lon': [14.4894, -83.0197, 23.77394, -87.6553]}
    )

    merged = merged.merge(special_arenas_df, on='venue', how='left', suffixes=('', '_special'))

    # prefer the _special prefix if it exists
    merged['venue_lat'] = merged['venue_lat_special'].combine_first(merged['venue_lat'])
    merged['venue_lon'] = merged['venue_lon_special'].combine_first(merged['venue_lon'])
    merged = merged.drop(columns=['venue_lat_special', 'venue_lon_special'])

    print("Merged DataFrame:")
    print(merged.head())

    df_len = len(merged)
    print("Total rows: ", df_len)
    print("Total seasons merged: ", df_len / 1312)
    merged.to_csv('processed_data/merged_schedule.csv', index=False)

if __name__ == "__main__":
    main()