# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 12:10:15 2021

@author: jwini
"""
from espn_api.hockey import League
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

swid = "30DF2666-5ECF-459C-9F26-665ECF859C12"
espn_s2 = 'AEAhXtbnZRQrhvOl6ptgNuOHeTnNWtlXJqvvTXfNFf0BgOjnNETLvKHqClqcorEn4%2F5fiybN1WKvlp1p2e5V7fRdvP9b551wjw%2FvlgS%2FvhZmjlHIsAzXhyyRKH%2BWIYXxmngLLec7UtqT242MwFbKjqJ%2Fm6a4lCqWa2fflj7x2WVlUt85e8muVAwNugG6rDpwBsNi%2BrcdOJks9ikbUrsSXp7wU5u7EBJBf7ZPlk57NnojcDWyr23TpOPXnqtiuDNAsBM8GuXJ7gy8neJacKOlQC5DZrQ33W0BuOWGKl%2F2V9GxCQ%3D%3D'

#league is how we access the entire year's data
league = League(league_id = 1140371907, year = 2022, espn_s2 = espn_s2, swid = swid)
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

#player
stats_kane = allrosteredplayers[4].stats['Last 7 2022']
#stats_kane['Player Name'] = allrosteredplayers[4].name
kane_last7 = stats_kane['total']
kane_last7['Player Name'] = allrosteredplayers[4].name





stats_point = allrosteredplayers[0].stats['Last 7 2022'] #keyerror 'Last 7 2022
point_last7 = stats_point['total']

total_22 = []
for p in range(len(allrosteredplayers)):
    try:
        stats = allrosteredplayers[p].stats['Last 7 2022']
        last7 = stats['total']
        last7['Player Name'] = allrosteredplayers[p].name
        total_22.append(last7)
    except KeyError:
        print("Player did not have any games this week")
        
    

def get_matchup_stats_to_df(period):
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
        #matchup_list.loc[matchup_list['Winner'] == 'AWAY', 'Winning Team'] = matchup_list['Away Team Name'] 
    return matchup_list



'''
Get a dataframe of the periods player points
'''
#Extract last 7 2022
                
def player_stats_from_matchup(week_number, matchup_number):
    week = get_matchup_stats_to_df(week_number)
    matchup = week[matchup_number]
    home_lineup = matchup['Home Lineup']
    home_name = matchup['Home Team Name']
    home_stats = []
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
    
    away_lineup = matchup['Away Lineup']
    away_name = matchup['Away Team Name']
    away_stats = []
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
    
    
test = player_stats_from_matchup(8,1)   
             

        
'''
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

player_stats_list = get_player_stats(allrosteredplayers)
player_stats_df = pd.DataFrame(player_stats_list)


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

all_team_info = get_team_info(team_list)

team_df = pd.DataFrame(all_team_info)


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

tony_stats = unpack_stats(team_df, 'Jason Winik')


#
