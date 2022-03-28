# -*- coding: utf-8 -*-
import path
import os
import numpy as np

##################
setup_path = r"C:/Users/jwini/OneDrive/Documents/Python Scripts/hockey-analytics/Setup Files/"
output_path = r"C:/Users/jwini/OneDrive/Documents/Python Scripts/hockey-analytics/Outputs"

cred_fname = r"credentials.py"
matchup_fname = "DAHL Matchup Stats.py"
player_fname = "DAHL Player Stats.py"

matchup_csv = "/matchup_stats.csv"
player_csv = "/player_stats.csv"
player_season_csv = "/player_stats_season.csv"

matchup_path = os.path.join(output_path + matchup_csv)
player_path = os.path.join(output_path + player_csv)
player_season_path = os.path.join(output_path + player_season_csv)

#Run setup_files
setup_files = [cred_fname, matchup_fname, player_fname]
for f in setup_files:
    exec(open(os.path.join(setup_path, f)).read())
    


#####################
week = 20

matchup_stats = create_matchup_df(1,week) 
player_stats = season_player_stats(1,week)
matchup_stats_final = matchup_player_stats(matchup_stats, player_stats)






#Create a summary df that sums each player's weekly stats. Create FPPG columns
player_stats_season = player_stats.groupby(by=["Player Name", "Team Name", 'Position']).sum().reset_index()
player_stats_season['FPPG'] = np.where(player_stats_season['Position'] != 'Goalie', 
                                       player_stats_season['Points'] / player_stats_season['GP'],
                                       player_stats_season['Points'] / player_stats_season['GS'])
player_stats_season['Over 3 FPPG'] = np.where(player_stats_season['FPPG'] >= 3.0, True, False)
player_stats_season['Over 4 FPPG'] = np.where(player_stats_season['FPPG'] >= 4.0, True, False)

#next steps. In matchup


tda_trade = ['Nino Niederreiter', 'Ryan Johansen', 'Evan Rodrigues', 'Kyle Connor']
thomas_trade = []







###### Export to csv
matchup_stats.to_csv(matchup_path)
player_stats.to_csv(player_path)
player_stats_season.to_csv(player_season_path)
 