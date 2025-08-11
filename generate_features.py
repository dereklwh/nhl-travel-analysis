import pandas as pd
import numpy as np
from math import pi

'''
Inputs
- games_raw.csv
- nhl_stadiums.csv

Outputs
- team_games_features.csv : long format, one row per game per team

features: 
- distance: the distance traveled by the team
- consecutive away games: number of consecutive away games (0 if at home)
- rest days: number of rest days before the game
- Can add more features here
'''

# Build the schedule for each team because two teams play the same game
# Make sure they "own" a row of their own game
def build_schedule_per_team(df) -> pd.DataFrame:
    home = df.copy()
    away = df.copy()

    home['team'] = home['home_team_abbrev']
    home['goals_for'] = home['home_team_score']
    home['goals_against'] = home['away_team_score']
    home['is_away'] = False
    home['game_result'] = np.where(home['winner_abbrev'] == home['team'], 'win', 'loss')

    away['team'] = away['away_team_abbrev']
    away['goals_for'] = away['away_team_score']
    away['goals_against'] = away['home_team_score']
    away['is_away'] = True
    away['game_result'] = np.where(away['winner_abbrev'] == away['team'], 'win', 'loss')

    combined = pd.concat([home, away], ignore_index=True)
    combined = combined.sort_values(by=['team', 'game_date', 'start_time_utc'])
    return combined

# From assignment 3 
# inspired by the implementation from:
# https://stackoverflow.com/a/21623206

def distance(df) -> pd.DataFrame:

    r = 6371
    p = pi / 180
    
    a = (
        0.5 - np.cos((df['venue_lat_prev'] - df['venue_lat']) * p) / 2 +
        np.cos(df['venue_lat'] * p) * np.cos(df['venue_lat_prev'] * p) *
        (1 - np.cos((df['venue_lon_prev'] - df['venue_lon']) * p)) / 2
    )
    df['distance'] = 2 * r * np.arcsin(np.sqrt(a))

    return df

def generate_travel_features(games) -> pd.DataFrame:
    # 1: Distance Travelled
    # shift previous venue information for havarsine calculation
    games['venue_lat_prev'] = games.groupby('team')['venue_lat'].shift(1)
    games['venue_lon_prev'] = games.groupby('team')['venue_lon'].shift(1)

    # if there is a nan value for prev longitude and longitude that means it is start of season, assume that their prev lat and lon is same
    games['venue_lat_prev'] = games['venue_lat_prev'].fillna(games['venue_lat'])
    games['venue_lon_prev'] = games['venue_lon_prev'].fillna(games['venue_lon'])

    games = distance(games)

    # 2: Consecutive away games
    games['consecutive_away_games'] = games.groupby('team')['is_away'].cumsum()
    games['consecutive_away_games'] = games['consecutive_away_games'].where(games['is_away'], 0)

    # 3: Rest days
    games['game_date'] = pd.to_datetime(games['game_date'])
    games['rest_days'] = games.groupby('team')['game_date'].diff().dt.days - 1 # eg: games between 01-01 and 01-02 should be considered 0 rest days
    games['rest_days'] = games['rest_days'].fillna(0)

    # 4: back to back flag
    games['back_to_back'] = (games['rest_days'] == 0)
    return games


def main():
    # in order to use the havarsine distance function, need to get previous venue information
    games = pd.read_csv('processed_data/merged_schedule.csv')

    # join tables to be able to compute havarsine distance
    # need to have previous game venue to compute distance
    games = build_schedule_per_team(games)
    games = generate_travel_features(games)

    games.to_csv('processed_data/team_games_features.csv')


if __name__ == "__main__":
    main()