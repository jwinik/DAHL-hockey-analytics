# -*- coding: utf-8 -*-
import path
import os
from espn_api.hockey import League
import pandas as pd
import numpy as np

##################
setup_path = r"C:/Users/jwini/OneDrive/Documents/Python Scripts/hockey-analytics/Setup Files/"
output_path = r"C:/Users/jwini/OneDrive/Documents/Python Scripts/hockey-analytics/Outputs"

cred_fname = r"credentials.py"
matchup_fname = "DAHL Matchup Stats.py"
player_fname = "DAHL Player Stats.py"

matchup_csv = "/matchup_stats.csv"
player_csv = "/player_stats.csv"

matchup_path = os.path.join(output_path + matchup_csv)
player_path = os.path.join(output_path + player_csv)


#Run setup_files
setup_files = [cred_fname, matchup_fname, player_fname]
for f in setup_files:
    exec(open(os.path.join(setup_path, f)).read())
    


#####################
week = 20

matchup_stats = create_matchup_df(1,week) 
player_stats = season_player_stats(1,week)

matchup_stats = matchup_player_stats(matchup_stats, player_stats)


###### Export to csv
matchup_stats.to_csv(matchup_path)
player_stats.to_csv(player_path)
 