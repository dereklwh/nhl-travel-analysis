import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import sys

'''
This file produces all the visuals for the report.

input: team_games_features.csv
output: pngs in figures directory
'''

def prepare_data_for_analysis(df) -> pd.DataFrame:
    df = df[df['season'] != 20252026]
    # df = df[df['is_away']]
    dist_bins = [0, 250, 500, 750, 1000, 1250, 1500, 2000, 3000, 5000, np.inf]

    df['dist_bin'] = pd.cut(df['distance'], bins=dist_bins, right=False)
    df['dist_bin_midpoint'] = df['dist_bin'].apply(lambda x: (x.left + x.right) / 2)
    return df

def plot_1(df):
    g = df.copy()
    g = g[g['season'] == 20242025]

    # Totals
    total_km = g.groupby('team')['distance'].sum().rename('total_km')
    away_km  = g[g['is_away']].groupby('team')['distance'].sum().rename('away_km')
    home_km  = g[~g['is_away']].groupby('team')['distance'].sum().rename('home_km')

    summary = pd.concat([total_km, away_km, home_km], axis=1).fillna(0)
    summary['away_share']   = (summary['away_km'] / summary['total_km']).replace([np.inf, np.nan], 0)
    summary['games']        = g.groupby('team')['game_id'].nunique()
    summary['km_per_game']  = summary['total_km'] / summary['games']

    # Sort by total travel (or pick 'away_km' to focus on road legs)
    summary = summary.sort_values('total_km', ascending=False)

    # Stacked bar: home vs away contributions to total
    ax = summary[['away_km', 'home_km']].plot(kind='bar', stacked=True, figsize=(12,6))
    ax.set_title('Team Travel: Home- vs Away-Leg Kilometres')
    ax.set_ylabel('Kilometres')
    ax.set_xlabel('Team')
    ax.legend(title='Leg type')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('figures/fig1.png')

    print('Figure 1 saved to png.')

def plot_2(df):
    g = df.copy()
    g = g[g['is_away']]
    distance_grouped = g.groupby('dist_bin_midpoint')['game_result'].apply(lambda s: (s == 'win').mean()).reset_index()
    distance_counts = g['dist_bin_midpoint'].value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    plt.plot(distance_grouped['dist_bin_midpoint'], distance_grouped['game_result'], marker='o')
    plt.title('Distance Traveled vs. Points Percentage')
    plt.xlabel('Travel Distance Since Previous Game (km)')
    plt.ylabel('Win %')
    plt.ylim(0.4, 0.55)
    plt.savefig('figures/fig2.png')

    print('Figure 2 saved to png.')

def plot_3(df):
    g = df.copy()
    g = g[g['is_away']]
    g['rest_clipped'] = g['rest_days'].clip(0,5) # exclude super long breaks (all-star week)
    win_pct = g.groupby('rest_clipped')['game_result'].apply(lambda s:(s=='win').mean()) # gets the win percentage for each group

    counts = g['rest_clipped'].value_counts().sort_index()

    # plot
    fig, ax1 = plt.subplots(figsize=(12, 6))
    sns.barplot(x=win_pct.index, y=win_pct.values, ax=ax1)
    plt.title('Distribution of Rest Days (Clipped)')
    plt.xlabel('Rest Days (Clipped)')
    plt.ylabel('Win %')
    ax2 = ax1.twinx()
    sns.lineplot(x=counts.index, y=counts.values, color='red', label='Game Count', ax=ax2)
    ax2.set_ylabel('Game Count')
    plt.savefig('figures/fig3.png')

    print('Figure 3 saved to png.')

def plot_4(df):
    g = df.copy()
    g = g[g['is_away']]
    def dist_class(d):
        if pd.isna(d): return np.nan
        if d < 1000: return "Short (<1000)"
        if d < 3000: return "Medium (1k–3k)"
        return "Long (≥3k)"
    g['dist_class'] = g['distance'].apply(dist_class)
    g['consec_bin'] = pd.cut(
        g['consecutive_away_games'],
        bins=[0, 1, 2, 3, 4, np.inf],
        labels=['1', '2', '3', '4', '5+'],
    )
    grouped = g.groupby(['consec_bin', 'dist_class'])['game_result'].apply(lambda s: (s == 'win').mean()).reset_index()

    # Plot the triple line plot
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=grouped, x='consec_bin', y='game_result', hue='dist_class', marker='o', palette='viridis')

    # Add labels and title
    plt.title('Win Percentage by Consecutive Away Games and Travel Distance')
    plt.xlabel('Consecutive Away Games')
    plt.ylabel('Win Percentage')
    plt.legend(title='Distance Class')
    plt.ylim(0, 1)
    plt.tight_layout()

    # Show the plot
    plt.savefig('figures/fig4.png')
    print('Figure 4 saved to png.')


def main(file):
    df = pd.read_csv(file)
    df = prepare_data_for_analysis(df)
    plot_1(df)
    plot_2(df)
    plot_3(df)
    plot_4(df)


if __name__ == "__main__":
    file1 = sys.argv[1]
    main(file1)