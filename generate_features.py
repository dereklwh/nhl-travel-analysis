import pandas as pd
import numpy as np

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
'''

# join tables to be able to compute havarsine distance
# need to have previous game venue to compute distance

def havarsine_distance(df):
    r = 6371 # Radius of the Earth in km
    lat1 = np.radians(df['venue_lat_prev'])
    lon1 = np.radians(df['venue_lon_prev'])
    lat2 = np.radians(df['venue_lat'])
    lon2 = np.radians(df['venue_lon'])

    df['distance'] = r * np.arccos(
        np.sin(lat1) * np.sin(lat2) +
        np.cos(lat1) * np.cos(lat2) * np.cos(lon2 - lon1)
    )
    
    return df

    


def main():

if __name__ == "__main__":
    main()