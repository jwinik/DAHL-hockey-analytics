# -*- coding: utf-8 -*-
import path
import os
import numpy as np

##################
setup_path = r"C:/Python Scripts/hockey-analytics/Setup Files/"
output_path = r"C:/Python Scripts/hockey-analytics/Outputs"

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
week = 22

matchup_stats = create_matchup_df(1,week) 
player_stats = season_player_stats(1,week)
matchup_stats_final = matchup_player_stats(matchup_stats, player_stats)






#Create a summary df that sums each player's weekly stats. Create FPPG columns
#player_stats_season = player_stats.groupby(by=["Player Name", "Team Name", 'Position']).sum().reset_index()
#player_stats_season['FPPG'] = np.where(player_stats_season['Position'] != 'Goalie', 
#                                       player_stats_season['Points'] / player_stats_season['GP'],
#                                       player_stats_season['Points'] / player_stats_season['GS'])
#player_stats_season['Over 3 FPPG'] = np.where(player_stats_season['FPPG'] >= 3.0, True, False)
#player_stats_season['Over 4 FPPG'] = np.where(player_stats_season['FPPG'] >= 4.0, True, False)

#next steps. In matchup


#tda_trade = ['Nino Niederreiter', 'Ryan Johansen', 'Evan Rodrigues', 'Kyle Connor']
#thomas_trade = []
ew_path = r"C:\Python Scripts\hockey-analytics\Data\Evolving Hockey"
ew_csv = "EH_std_sk_stats_all_regular_no_adj_2022-04-02.csv"
ew_stats = pd.read_csv(os.path.join(ew_path, ew_csv))



def merge_pstats(player_stats, player_info):
    merge_cols = ['Player', 'Shoots', 'Birthday', 'Age', 'Draft Yr', 'Draft Rd', 'Draft Ov']
    player_info = player_info[[col for col in player_info.columns if col in merge_cols]]
    df = pd.merge(player_stats, player_info,
                  how = "left",
                  left_on = "Player Name", 
                  right_on = "Player")
    return df

test = merge_pstats(player_stats, ew_stats)

age_df = test.groupby(['Team Name', "Week Number", 'Age']).sum().reset_index()

age_count_df = test.groupby(['Team Name', "Week Number", 'Age']).count()
    
test2 =  test.groupby(['Team Name', 'Age']).sum().reset_index()
test2 = test2[test2['Team Name'] == 'Carolina Tony'] 


def plot_age_bar(data, week = 0, team = 0):
    if week == 0:
        data = data.groupby(['Team Name', 'Age']).sum().reset_index()
        label = "2021-22 Season"
    else:
        data = data[data['Week Number'] == week]
        label = "Week " + str(week)
    if team == 0:
       data = data.groupby(['Age']).sum().reset_index()
    else:
       data = data[data['Team Name'] == team]   
    fig_dims = (9,8)
    fig, ax = plt.subplots(figsize = fig_dims)
    sns.barplot(x="Age", y="Points",
                data=data,
                ax=ax).set(title=str(team) + ' Fantasy Points by Age Group: ' +str(label))
    plt.xticks(fontsize=10, rotation=-45)
    plt.legend(title="", loc='best', fontsize=20)


plot_age_bar(age_df, week = 9, team = 'Carolina Tony')





###### Export to csv
matchup_stats.to_csv(matchup_path)
player_stats.to_csv(player_path)
player_stats_season.to_csv(player_season_path)
 