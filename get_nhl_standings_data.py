import pandas as pd
import requests


def scrapeStandings(date):
    url = f"https://api-web.nhle.com/v1/standings/{date}"

    response = requests.get(url).json()
    standings_df = pd.json_normalize(response["standings"])

    return standings_df

def main():
    standings_df = scrapeStandings("2025-04-16") # end of 20242025 season
    standings_df.head()
    standings_df.to_csv('processed_data/nhl_standings_2025.csv', index=False)

if __name__ == "__main__":
    main()