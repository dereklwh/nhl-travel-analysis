import pandas as pd
import requests
'''
Scrape NHL standings data for the last three seasons.
Input: None
Output: nhl_standings_merged.csv in processed_data directory
'''
def scrapeStandings(date):
    url = f"https://api-web.nhle.com/v1/standings/{date}"

    response = requests.get(url).json()
    standings_df = pd.json_normalize(response["standings"])

    return standings_df

def main():
    standings25_df = scrapeStandings("2025-04-16") # end of 20242025 season
    standings24_df = scrapeStandings("2024-04-18") # end of 20232024 season
    standings23_df = scrapeStandings("2023-04-14") # end of 20222023 season
    standings_df = pd.concat([standings23_df, standings24_df, standings25_df], ignore_index=True)
    standings_df = standings_df.rename(columns={'seasonId': 'season', "teamAbbrev.default": "team"})
    standings_df.to_csv('processed_data/nhl_standings_merged.csv', index=False)

if __name__ == "__main__":
    main()