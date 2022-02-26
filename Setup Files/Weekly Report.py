# -*- coding: utf-8 -*-
import path
import os
from espn_api.hockey import League
from ipywidgets import interact, interact_manual

##################
setup_path = "C:/Users/jwini/OneDrive/Documents/Python Scripts/hockey-analytics/Setup Files/"
cred_fname = "credentials.py"
matchup_fname = "DAHL Matchup Stats.py"
player_fname = "DAHL Player Stats.py"

setup_files = [cred_fname, matchup_fname, player_fname]
    
for f in setup_files:
    exec(open(os.path.join(setup_path, f)).read())
    


#####################
week = 18

matchup_stats = create_matchup_df(1,week) 
player_stats = season_player_stats(1,week)



# Matchup Tables
matchup_tables(matchup_stats, "Fantasy Points", False)

matchup_tables(matchup_stats, "Opponent Fantasy Points", False)   

matchup_tables(matchup_stats, "Fantasy Points Rank", True) 



player_stats = season_player_stats(1,week)


 