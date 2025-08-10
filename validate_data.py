import pandas as pd

def main():
    # Load the games data
    try:
        games_df = pd.read_csv('raw_data/nhl_games_raw.csv')
        print("Games data loaded successfully.")
    except Exception as e:
        print(f"Error loading games data: {e}")
        return
    
    # check each column for missing values
    missing_columns = games_df.columns[games_df.isnull().any()].tolist()
    if missing_columns:
        print("Missing values found in the following columns:")
        for col in missing_columns:
            print(f"- {col}")
    else:
        print("No missing values found in any column.")

if __name__ == "__main__":
    main()