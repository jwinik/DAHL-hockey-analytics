# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 12:10:15 2021

@author: jwini
"""
from espn_api.hockey import League
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


player_map = league.player_map
team_list = league.teams


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
    Returns a dataframe with stats for each matchup.      

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
#Breaks the matchup from # of matchup into number of teams            
def player_stats_by_matchup(week_number, matchup_number):
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

#combines all 5 matchup dfs into one list    
def weekly_player_points(week):
    week_0 = player_stats_by_matchup(week,0)
    week_1 = player_stats_by_matchup(week,1)
    week_2 = player_stats_by_matchup(week,2)
    week_3 = player_stats_by_matchup(week,3)
    week_4 = player_stats_by_matchup(week,4)
    week_list = [week_0, week_1, week_2, week_3, week_4]
    week_df = pd.concat(week_list, sort=True).reset_index(drop=True)
    return week_df
             
#main function to get final dataframe


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
    df = all_weeks[new_cols]
    
    df["W"] = df.W.fillna(999)
    df.loc[df.W != 999, "Position"] = "Goalie"
    df.loc[df.W == 999, "W"] = None

    keep_cols = ['Player Name', 'Team Name', 'Position', 'Week Number','Points',
        '+/-', 'A', 'ATOI',
        'BLK', 'DEF', 'FOL', 'FOW', 'G', 'GA', 'GAA', 'GP', 'GS', 'GWG', 
        'HAT', 'HIT', 'L', 'MIN ?', 'OTL', 'PIM', 'PPG', 'PPP', 
        'SA', 'SHA', 'SHG', 'SHP', 'SO', 'SOG', 'SV',
        'SV%', 'TTOI ?', 'W']

    df = df.drop(columns =[col for col in df if col not in keep_cols])
    df = df[keep_cols]
    return df

def matchup_player_stats(matchup_stats, player_stats):
    player_stats = player_stats.groupby(by=["Team Name", "Week Number"]).sum()
    merged = matchup_stats.merge(player_stats, on=["Team Name", "Week Number"])
    merged['Fantasy Points Rank, Whole Season'] = merged['Fantasy Points'].rank(ascending=False)
    return merged

######################## Plots ########################

x_stats = ['Points', '+/-',
       'A', 'ATOI', 'BLK',
       'DEF', 'FOL', 'FOW', 'G', 'GA', 'GAA', 'GP', 'GS', 'GWG', 'HAT', 'HIT',
       'L', 'MIN ?', 'OTL', 'PIM', 'PPG', 'PPP', 'SA', 'SHA', 'SHG', 'SHP',
       'SO', 'SOG', 'SV', 'SV%', 'TTOI ?', 'W']
y_stats = ['Points', '+/-',
       'A', 'ATOI', 'BLK',
       'DEF', 'FOL', 'FOW', 'G', 'GA', 'GAA', 'GP', 'GS', 'GWG', 'HAT', 'HIT',
       'L', 'MIN ?', 'OTL', 'PIM', 'PPG', 'PPP', 'SA', 'SHA', 'SHG', 'SHP',
       'SO', 'SOG', 'SV', 'SV%', 'TTOI ?', 'W']

def plot_player_scatter(week_start, week_end, data, x_stat, y_stat):
    fig, ax = plt.subplots(figsize = (9,8))
    #data = data.loc[team]
    for team, group in data.groupby('Team Name'):
        ax.scatter(group[x_stat], group[y_stat], label = team)
    ax.legend(loc='best')
    ax.set_ylabel(str(y_stat) + ' per Player')
    ax.set_xlabel(str(x_stat) + ' per Player')
    ax.set_title(str(x_stat) + ' and ' + str(y_stat) + ' per Player: Week ' + str(week_start) + " to " + str(week_end))
    
    
def plot_player_lines(df, team, x_stat, y_stat, week = 0):
    if week == 0:
        fig, ax = plt.subplots(figsize = (10,10))
        df = df[df['Team Name'] == team]
        for key, grp in df.groupby(['Player Name']):
                ax.scatter(grp[x_stat], grp[y_stat], label=key)
                plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax.set_ylabel(str(y_stat) + ' per Player')
        ax.set_xlabel(str(x_stat) + ' per Player')
        ax.set_title(str(x_stat) + ' and ' + str(y_stat) + ' per Player: Season, ' + team)
    else:
        fig, ax = plt.subplots(figsize = (10,10))
        df = df[df['Team Name'] == team]
        df = df[df['Week Number'] == week]
        for key, grp in df.groupby(['Player Name']):
                ax.scatter(grp[x_stat], grp[y_stat], label=key)
                plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax.set_ylabel(str(y_stat) + ' per Player')
        ax.set_xlabel(str(x_stat) + ' per Player')
        ax.set_title(str(x_stat) + ' and ' + str(y_stat) + ' per Player: Week ' + str(week) + ": " + team)
        ax.get_legend().remove()
        df[[x_stat,y_stat,'Player Name']].apply(lambda x: ax.text(*x),axis=1)
        




































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

#tony_stats = unpack_stats(team_df, 'Jason Winik')


#
