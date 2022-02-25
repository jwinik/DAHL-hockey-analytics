# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 16:26:49 2022

@author: jwini
"""

"""
Created on Sat Jul 17 12:10:15 2021

@author: jwini
"""
from espn_api.hockey import League
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import os

#swid = "30DF2666-5ECF-459C-9F26-665ECF859C12"
#espn_s2 = 'AEAhXtbnZRQrhvOl6ptgNuOHeTnNWtlXJqvvTXfNFf0BgOjnNETLvKHqClqcorEn4%2F5fiybN1WKvlp1p2e5V7fRdvP9b551wjw%2FvlgS%2FvhZmjlHIsAzXhyyRKH%2BWIYXxmngLLec7UtqT242MwFbKjqJ%2Fm6a4lCqWa2fflj7x2WVlUt85e8muVAwNugG6rDpwBsNi%2BrcdOJks9ikbUrsSXp7wU5u7EBJBf7ZPlk57NnojcDWyr23TpOPXnqtiuDNAsBM8GuXJ7gy8neJacKOlQC5DZrQ33W0BuOWGKl%2F2V9GxCQ%3D%3D'

#league is how we access the entire year's data
#league = League(league_id = 1140371907, year = 2022, espn_s2 = espn_s2, swid = swid)
player_map = league.player_map
team_list = league.teams

# player of the week
# team of the week
# matchup table
# matchup graph
# Team with the most forward points
# Team with the most d points
# team with the most goalie points
# Rolling graph of each week's team points, and thick line for average points

# Get a list of all the rostered players
allrosteredplayers = []
for team in league.teams:
    for player in team.roster:
        allrosteredplayers.append(player)

team_names = []
for team in league.teams:
    name = team.team_name
    team_names.append(name)
   

def get_matchup_stats_to_dict(period):
    """

    Parameters
    ----------
    period : integer
        The input is what week you want stats for. 

    Returns
    -------
    week_df : Dataframe
    Returns a dataframe of matchup winners, losers, weekly rosters, and total points       

    """
    box_scores = league.box_scores(matchup_period = period)
    matchup_list = []
    for i in range(len(box_scores)):
        matchup_dicts = {}
        week = box_scores[i]
        matchup_dicts['Away Lineup'] = week.away_lineup
        matchup_dicts['Away Projected'] = week.away_projected       
        matchup_dicts['Away Score'] = week.away_score
        matchup_dicts['Away Team'] = week.away_team
        matchup_dicts['Home Lineup'] = week.home_lineup
        matchup_dicts['Home Projected'] = week.home_projected
        matchup_dicts['Home Score'] = week.home_score
        matchup_dicts['Winner'] = week.winner
        matchup_dicts['Home Team Name'] = week.home_team.team_name
        matchup_dicts['Away Team Name'] = week.away_team.team_name
        matchup_dicts['Winning Team'] = matchup_dicts['Home Team Name']
        matchup_dicts['Week Number'] = period        
        matchup_list.append(matchup_dicts) 
    return matchup_list



'''
Get a dataframe of the periods player points
'''
#Extract last 7 2022
                
def player_stats_from_matchup(week_number, matchup_number):
    week = get_matchup_stats_to_dict(week_number)
    matchup = week[matchup_number]
    home_lineup = matchup['Home Lineup']
    home_name = matchup['Home Team Name']
    home_stats = []
    away_lineup = matchup['Away Lineup']
    away_name = matchup['Away Team Name']
    away_stats = []
    for p in range(len(home_lineup)):
        player = {}
        stats = {}
        player['Team Name'] = home_name
        player['Player Name'] = home_lineup[p].name
        player['Position'] = home_lineup[p].position
        player['Points'] = home_lineup[p].points
        stats = home_lineup[p].stats['05null']['total']
        merged = {**player, **stats}
        home_stats.append(merged)
        #df = pd.DataFrame.from_dict(home_stats)
        home = pd.DataFrame.from_dict(home_stats)
    
    for p in range(len(away_lineup)):
        player = {}
        stats = {}
        player['Team Name'] = away_name
        player['Player Name'] = away_lineup[p].name
        player['Position'] = away_lineup[p].position
        player['Points'] = away_lineup[p].points
        stats = away_lineup[p].stats['05null']['total']
        merged = {**player, **stats}
        away_stats.append(merged)
        away = pd.DataFrame.from_dict(away_stats)
    both = [home,away]
    combined = pd.concat(both, sort=True)
    combined['Week Number'] = week_number
    return combined
    
def weekly_player_points(week):
    week_0 = player_stats_from_matchup(week,0)
    week_1 = player_stats_from_matchup(week,1)
    week_2 = player_stats_from_matchup(week,2)
    week_3 = player_stats_from_matchup(week,3)
    week_4 = player_stats_from_matchup(week,4)
    week_list = [week_0, week_1, week_2, week_3, week_4]
    week_df = pd.concat(week_list, sort=True).reset_index(drop=True)
    return week_df
             

def season_player_stats(week_start, week_end):
    week_end = week_end + 1
    weeks = range(week_start, week_end)
    week_list = []
    for w in weeks:
        df = weekly_player_points(w)
        week_list.append(df)
    all_weeks = pd.concat(week_list, sort=True)
    new_cols = ['Player Name', 'Team Name', 'Position', 'Week Number','Points',
            '+/-', '12', '16', '19', '25', '30', '35', '36', '37', 'A', 'ATOI',
            'BLK', 'DEF', 'FOL', 'FOW', 'G', 'GA', 'GAA', 'GP', 'GS', 'GWG', 
            'HAT', 'HIT', 'L', 'MIN ?', 'OTL', 'PIM', 'PPG', 'PPP', 
            'SA', 'SHA', 'SHG', 'SHP', 'SO', 'SOG', 'SV',
            'SV%', 'TTOI ?', 'W']
    all_weeks = all_weeks[new_cols]
    return all_weeks

#test = season_player_stats(1,9)

 

'''
Below here is useless currently
'''

 
def get_player_stats(player_list):
    new_list = []
    for player in player_list:
        player_dict = {}
        player_dict['Name'] = player.name
        player_dict['Injury Status'] = player.injuryStatus
        player_dict['Injured'] = player.injured
        player_dict['Eligible Slots'] = player.eligibleSlots
        player_dict['PlayerID'] = player.playerId
        player_dict['Acquisition Type'] = player.acquisitionType
        player_dict['Lineup Slot'] = player.lineupSlot
        player_dict['Pro Team'] = player.proTeam
        player_dict['Stats'] = player.stats
        if 'Last 7 2022' in player_dict['Stats']:    
            player_dict['Last 7'] = player_dict['Stats']['Last 7 2022']
        else:
            player_dict['Last 7'] = 0
        new_list.append(player_dict)
    return new_list

#player_stats_list = get_player_stats(allrosteredplayers)
#player_stats_df = pd.DataFrame(player_stats_list)


def get_team_info(team_list):
    blank_list = []
    for i in range(len(team_list)):
        team_dict = {}
        one = team_list[i]
        team_dict['Team Name'] = one.team_name
        team_dict['Owner'] = one.owner
        team_dict['Abbreviation'] = one.team_abbrev
        team_dict['Roster'] = one.roster
        team_dict['Stats'] = one.stats 
        team_dict['Wins'] = one.wins
        team_dict['Losses'] = one.losses
        blank_list.append(team_dict)
    return blank_list

#all_team_info = get_team_info(team_list)

#team_df = pd.DataFrame(all_team_info)


#def get_team_players(all_team_info):
#    for t in range(len(all_team_info)):
#        players = [t.get('Roster')]
#    return players
#    
#test = get_team_players(all_team_info)


def unpack_stats(df, owner_name):
    team =  df[df['Owner'] == str(owner_name)].reset_index(drop = True)
    #team = [get_player_stats(p) for p in team['Roster']]
    #team = [item for sublist in team for item in sublist]
    team_df = pd.DataFrame(team)
    unpacked = team_df.Stats.apply(pd.Series)
    unpacked.columns = unpacked.columns.str.replace(' ', '_')
    last15_2022 = unpacked.Last_15_2022.apply(pd.Series)
    last15_2022 = last15_2022.total.apply(pd.Series)
    last7_2022 = unpacked.Last_7_2022.apply(pd.Series)
    last7_2022 = last7_2022.total.apply(pd.Series)
    total_2021 = unpacked.Total_2021.apply(pd.Series)
    total_2021 = total_2021.total.apply(pd.Series)
    total_2022 = unpacked.Total_2022.apply(pd.Series)
    total_2022 = total_2022.total.apply(pd.Series)
    last30_2022 = unpacked.Last_30_2022.apply(pd.Series)
    last30_2022 = last30_2022.total.apply(pd.Series)
    proj_2021 = unpacked.Projected_2022.apply(pd.Series)
    proj_2021 = proj_2021.total.apply(pd.Series)
    proj_2022 = unpacked.Projected_2022.apply(pd.Series)
    proj_2022 = proj_2022.total.apply(pd.Series)
    unpacked_all = [last15_2022, last7_2022, total_2021, total_2022, last30_2022, proj_2021, proj_2022]
    return unpacked_all


################################################

setup_path = "C:/Users/jwini/OneDrive/Documents/Python Scripts/hockey-analytics/Setup Files/"
cred_fname = "credentials.py"
matchup_fname = "DAHL Matchup Stats.py"
player_fname = "DAHL Player Stats.py"

setup_files = [cred_fname, matchup_fname, player_fname]
for f in setup_files:
    exec(open(os.path.join(setup_path, f)).read())

matchup_week1 = get_matchup_stats_to_df(1)
matchup_week2 = get_matchup_stats_to_df(2)
matchup_week3 = get_matchup_stats_to_df(3)
matchup_week4 = get_matchup_stats_to_df(4)
matchup_week5 = get_matchup_stats_to_df(5)
matchup_week6 = get_matchup_stats_to_df(6)
matchup_week7 = get_matchup_stats_to_df(7)
matchup_week8 = get_matchup_stats_to_df(8)
matchup_week9 = get_matchup_stats_to_df(9)
matchup_week10 = get_matchup_stats_to_df(10)
matchup_week11 = get_matchup_stats_to_df(11)
matchup_week12 = get_matchup_stats_to_df(12)
matchup_week13 = get_matchup_stats_to_df(13)
matchup_week14 = get_matchup_stats_to_df(14)
matchup_week15 = get_matchup_stats_to_df(15)
matchup_week16 = get_matchup_stats_to_df(16)
matchup_week17 = get_matchup_stats_to_df(17)

week1 = clean_matchup_df(matchup_week1)
week2 = clean_matchup_df(matchup_week2)
week3 = clean_matchup_df(matchup_week3)        
week4 = clean_matchup_df(matchup_week4)        
week5 = clean_matchup_df(matchup_week5)
week6 = clean_matchup_df(matchup_week6)
week7 = clean_matchup_df(matchup_week7)
week8 = clean_matchup_df(matchup_week8)
week9 = clean_matchup_df(matchup_week9)
week10 = clean_matchup_df(matchup_week10)
week11 = clean_matchup_df(matchup_week11)
week12 = clean_matchup_df(matchup_week12)
week13 = clean_matchup_df(matchup_week13)
week14 = clean_matchup_df(matchup_week14)
week15 = clean_matchup_df(matchup_week15)
week16 = clean_matchup_df(matchup_week16)
week17 = clean_matchup_df(matchup_week17)
matchup_weeks = [week1, week2, week3, week4, 
                 week5, week6, week7,week8, 
                 week9, week10, week11, week12, 
                 week13, week14, week15, week16,
                week17]

matchup_df_clean = clean_matchup_dfs(matchup_weeks)


def create_matchup_df(start, end):
    matchup_list = []
    matchup_list_clean = []
    for i in range(start, end+1):
        matchup_weeki = get_matchup_stats_to_df(i)
        matchup_list.append(matchup_weeki)
    for j in matchup_list:
        clean_weeki = clean_matchup_df(j)
        matchup_list_clean.append(clean_weeki)
    matchup_df = pd.concat(matchup_list_clean)
    return matchup_df
    
        
test = create_matchup_df(1,17)    
        
    
        
        
    
    
    