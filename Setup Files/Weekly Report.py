# -*- coding: utf-8 -*-
import path
import os
import numpy as np

##################
setup_path = r"C:\Users\jwini\Documents\Gtihub Repositories\hockey-analytics\Setup Files"
output_path = r"C:\Users\jwini\Documents\Gtihub Repositories\hockey-analytics\Outputs"

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
week = 24

matchup_stats = create_matchup_df(1,week) 
player_stats = season_player_stats(1,week)
matchup_stats_player_data = matchup_player_stats(matchup_stats, player_stats)



#yo = league.get_team_data(2)

#def player_info(name: str = None, playerId: int = None) -> "Mats Zuccarello"


###### Export to csv
matchup_stats.to_csv(matchup_path)
player_stats.to_csv(player_path)
matchup_stats_player_data.to_csv(player_season_path)
 