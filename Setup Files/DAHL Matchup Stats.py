# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 13:31:01 2021

@author: jwini
"""

cred_path = "C:/Users/jwini/OneDrive/Documents/Python Scripts/hockey-analytics/Setup Files/credentials.py"
exec(open(cred_path).read())
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

#swid = "30DF2666-5ECF-459C-9F26-665ECF859C12"
#espn_s2 = 'AEAhXtbnZRQrhvOl6ptgNuOHeTnNWtlXJqvvTXfNFf0BgOjnNETLvKHqClqcorEn4%2F5fiybN1WKvlp1p2e5V7fRdvP9b551wjw%2FvlgS%2FvhZmjlHIsAzXhyyRKH%2BWIYXxmngLLec7UtqT242MwFbKjqJ%2Fm6a4lCqWa2fflj7x2WVlUt85e8muVAwNugG6rDpwBsNi%2BrcdOJks9ikbUrsSXp7wU5u7EBJBf7ZPlk57NnojcDWyr23TpOPXnqtiuDNAsBM8GuXJ7gy8neJacKOlQC5DZrQ33W0BuOWGKl%2F2V9GxCQ%3D%3D'

league = League(league_id = league_id, year = 2022, espn_s2 = espn_s2, swid = swid)

def get_matchup_list(period):
    """

    Parameters
    ----------
    period : integer
        The input is what week you want stats for. 

    Returns
    -------
    week_df : Dataframe
    Returns a list of 5 matchup level stats

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


def matchup_list_to_df(matchup_list):
    """

    Parameters
    ----------
    matchup_list : 
        The input is the list of matchup dictionaries.

    Returns
    -------
    matchup_df : Dataframe
    Returns a dataframe with summary stats for each matchup

    """

    home_list = []
    away_list = []
    for i in range(len(matchup_list)):
        home_df = {}
        away_df = {}
        home = matchup_list[i]
        away = matchup_list[i]
        home_df['Team Name'] = home['Home Team Name']
        home_df['Week Number'] = home['Week Number']
        home_df['Home or Away'] = 'Home'
        home_df['Fantasy Points'] = home['Home Score']
        #home_df['Projected Points'] = home['Home Projected']
        home_df['Opponent Team Name'] = home['Away Team Name']
        home_df['Opponent Fantasy Points'] = home['Away Score']
        home_df['Opponent Projected Points'] = home['Away Projected']
        home_df['Winner'] = home['Winner']
        home_list.append(home_df)
        all_home_df = pd.DataFrame(home_list)   
        
        away_df['Team Name'] = away['Away Team Name']
        away_df['Week Number'] = away['Week Number']
        away_df['Home or Away'] = 'Away'
        away_df['Fantasy Points'] = away['Away Score']
        #away_df['Projected Points'] = away['Away Projected']
        away_df['Opponent Team Name'] = away['Home Team Name']
        away_df['Opponent Fantasy Points'] = away['Home Score']
        away_df['Opponent Projected Points'] = away['Home Projected']
        away_df['Winner'] = away['Winner']
        away_list.append(away_df)
        all_away_list = pd.DataFrame(away_list)
        #week_df = pd.concat(home_df, away_df)
        week_list = [all_home_df, all_away_list]
        matchup_df = pd.concat(week_list)
        matchup_df['Fantasy Points Rank'] = matchup_df['Fantasy Points'].rank(ascending=False)
    return matchup_df
    
def create_matchup_df(start, end):
    matchup_list = []
    matchup_list_clean = []
    for i in range(start, end+1):
        matchup_weeki = get_matchup_list(i)
        matchup_list.append(matchup_weeki)
    for j in matchup_list:
        clean_weeki = matchup_list_to_df(j)
        matchup_list_clean.append(clean_weeki)
    matchup_df = pd.concat(matchup_list_clean)
    return matchup_df












################## Matchup Plots #################

def plot_weekly_points(matchup_df, week):
    week_range = week + 1
    range_list = list(range(1,week_range))
    fig, ax = plt.subplots(figsize = (9,8))
    #df = df[df['Fantasy Points'] == aid_type]
    week_number = len(matchup_df)/10
    for key, grp in matchup_df.groupby(['Team Name']):
            ax.plot(grp['Week Number'], grp['Fantasy Points'], label=key)
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            ax.set_title('Weekly Fantasy Points Through Week ' + str(week_number))
            ax.set_ylabel('Total Fantasy Points')
            ax.set_xlabel('Week')
            plt.xlim(1,week)
            plt.setp(ax, xticks=range_list)


    

#points over time

def plot_week_bar(matchup_df, week):
    matchup_df = pd.melt(matchup_df,
                         id_vars=["Week Number", "Team Name", "Home or Away", "Winner"],
                         value_vars= ['Fantasy Points', "Opponent Fantasy Points"],
                         var_name="Points Type", value_name="Fantasy Points")
    fig_dims = (9,8)
    fig, ax = plt.subplots(figsize = fig_dims)
    sns.barplot(x="Team Name", y="Fantasy Points", hue='Points Type',
                data=matchup_df[matchup_df['Week Number']==week],
                ax=ax).set(title='Fantasy Points per Matchup: Week ' +str(week))
    #mean = matchup_df[matchup_df['Fantasy Points']].mean()
    #plt.axhline(y=.5, color='r', linestyle='-')
    plt.xticks(fontsize=10, rotation=-45)
    plt.legend(title="", loc='best', fontsize=20)
   


# weekly ranking table with average rank

def matchup_tables(matchup_df, values, boolean=False):
    matchup_df = matchup_df.pivot(index="Team Name", columns ="Week Number", values=str(values)).reset_index()
    matchup_df['Average'] = matchup_df.mean(axis=1)
    matchup_df['Total'] = matchup_df.sum(axis=1) - matchup_df['Average']
    matchup_df = matchup_df.sort_values('Total', ascending=boolean)  
    #matchup_df['Average'] = matchup_df['Average'].style.set_precision(5)
    matchup_df.loc['mean'] = matchup_df.mean()
    return matchup_df
    


