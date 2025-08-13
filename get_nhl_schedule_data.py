import numpy as np
import pandas as pd
import requests
import sys

BASE_URL = "https://api-web.nhle.com/v1/"

TEAM_ABBREVS_2425 = [
    "ANA","BOS","BUF","CAR","CBJ","CGY","CHI","COL","DAL","DET","EDM","FLA",
    "LAK","MIN","MTL","NJD","NSH","NYI","NYR","OTT","PHI","PIT","SEA","SJS",
    "STL","TBL","TOR","UTA","VAN","VGK","WPG","WSH"
]
# Previous season team abbreviations (before UTA was added)
TEAM_ABBREVS_PREVIOUS = [
    "ANA", "ARI", "BOS", "BUF","CAR","CBJ","CGY","CHI","COL","DAL","DET","EDM","FLA",
    "LAK","MIN","MTL","NJD","NSH","NYI","NYR","OTT","PHI","PIT","SEA","SJS",
    "STL","TBL","TOR","VAN","VGK","WPG","WSH"
]

# use requests to get nhl api data
def get_nhl_data_test(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # print(data)
        return 'Sucess!'
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")


def get_team_schedule_data(team_abbrev, season) -> dict:
    #/v1/club-schedule-season/{team}/{season}
    url = BASE_URL + 'club-schedule-season/' + team_abbrev + '/' + season
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

# Normalize the schedule games data into a pandas DataFrame.
def normalize_schedule_games(games_json) -> pd.DataFrame:
    games = games_json.get('games', [])
    normalized_data = []
    for g in games:
        row = {
            'game_id': g.get('id'),
            'season': g.get('season'),
            'game_date': g.get('gameDate'),
            'game_type': g.get('gameType'),
            'venue': g.get('venue').get('default'),
            'venue_utc_offest': g.get('venueUTCOffset'),
            'home_team_id': g.get('homeTeam').get('id'),
            'away_team_id': g.get('awayTeam').get('id'),
            'home_team_abbrev': g.get('homeTeam').get('abbrev'),
            'away_team_abbrev': g.get('awayTeam').get('abbrev'),
            'home_team_score': g.get('homeTeam').get('score'),
            'away_team_score': g.get('awayTeam').get('score'),
            'start_time_utc': g.get('startTimeUTC')
        }
        normalized_data.append(row)
    return pd.DataFrame(normalized_data)

def winner_cols(df: pd.DataFrame) -> pd.DataFrame:
    # Add game result columns to the DataFrame.
    # [winner_abbrev, loser_abbrev, goal_diff]

    # logic: home_team_score > away_team_score -> home team wins
    df = df.copy()
    df['winner_abbrev'] = np.where(df['home_team_score'] > df['away_team_score'], 
                                   df['home_team_abbrev'], df['away_team_abbrev'])
    df['loser_abbrev'] = np.where(df['home_team_score'] < df['away_team_score'],
                                   df['home_team_abbrev'], df['away_team_abbrev'])
    df['goal_diff'] = np.abs(df['home_team_score'] - df['away_team_score'])
    return df

def get_all_games(season: str) -> pd.DataFrame:
    """Get all games for the given season."""
    all_games = []
    for team in TEAM_ABBREVS_2425:
        team_schedule = get_team_schedule_data(team, season)
        normalized_schedule = normalize_schedule_games(team_schedule)
        all_games.append(normalized_schedule)
    return pd.concat(all_games, ignore_index=True)


    
def main(season):
    # base_url = 'https://api-web.nhle.com/v1/'
    # end_point = 'roster/VAN/current'
    # test_url = base_url + end_point
    # print(get_nhl_data_test(test_url))
    # van_json = get_team_schedule_data('VAN', '20242025')
    # print(van_json)

    # # process the json further
    # van_schedule_df = pd.json_normalize(van_json['games'])
    # print(van_schedule_df)

    # van_sched_df = normalize_schedule_games(van_json)
    # print(van_sched_df.head())
    # van_sched_df.to_csv('van_schedule_20242025.csv', index=False)

    ## Check season format:
    all_games = get_all_games(season)
    
    all_games = winner_cols(all_games)
    # Save the DataFrame to a CSV file

    # keep all regular season games and remove duplicates
    all_games = all_games[all_games['game_type'] == 2].reset_index(drop=True)
    all_games = all_games.drop_duplicates(subset=['game_id']).reset_index(drop=True)
    print(f"Total games collected: {len(all_games)}") # should be 1312

    filename = 'raw_data/nhl_games_raw_' + season + '.csv'
    all_games.to_csv(filename, index=False)

if __name__ == '__main__':
    main(sys.argv[1])
