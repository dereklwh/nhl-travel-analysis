# nhl-travel-analysis

## Project Overview
This project examines whether travel burden is associated with team performance in the NHL. Using schedule data and arena coordinates to compute leg-by-leg travel distance, and extracting features such as rest days, consecutive away games, and time zone jumps, I explore schedule equity and if the distance traveled correlates with win percentage. From my exploration of data between 2022-2025 (3 NHL season), there is no suggested correlation between win percentage and travel distance. However, a key finding is that home teams win more on average than away teams for all 3 seasons analyzed. While distance traveled doesn’t have a strong correlation, away teams are still more likely to lose. Travel distance could still be an attributing factor to that statistic.

### Approach
1. Gather schedule, standings, and arena data from the NHL API and Kaggle.
2. Clean and merge datasets, including manual adjustments for special venues.
3. Generate features such as:
    - Travel distance between games (Haversine formula)
    - Consecutive away games
    - Rest days between games
    - Goal differential
    - Home/away flags
4. Perform descriptive and statistical analysis, including win% comparisons, distance binning, and correlation tests.
5. Create visualizations to illustrate trends.

## Set Up Instructions
### Prerequisites
- Python 3.x
- pandas, numpy, matplotlib, seaborn, requests

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/dereklwh/nhl-travel-analysis.git
   cd nhl-travel-analysis
   ```

2. Run the project from scratch (for Mac):

   ```bash
   # Get data
   python3 get_nhl_schedule_data.py 20242025
   python3 get_nhl_stadium_data.py
   python3 get_nhl_standings_data.py

   # Clean and combine data
   python3 combine_data.py

   # Generate features
   python3 generate_features.py

   # Get visuals
   python3 get_visuals.py processed_data/team_games_features.csv
   ```

3. Run the project with the pre-preapred data (for Mac)
   ```bash
   # Get visuals
   python3 get_visuals.py processed_data/team_games_features.csv
   ```
