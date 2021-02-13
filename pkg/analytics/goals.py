import pandas as pd
try:    
    import pkg.analytics.utils as utils
except:
    import utils

pd.options.mode.chained_assignment = None  # default="warn"

def get_goals_scored(X: pd.DataFrame):
    """ get goals scored aggregated by teams and matchweek """
    
    
    teams = utils.create_team_dictionary(X)
    
    # get the value corresponding to keys in a list containing the match location
    for i in range(len(X)):
        HTGS = X.iloc[i]["FTHG"]
        ATGS = X.iloc[i]["FTAG"]
        teams[X.iloc[i].HomeTeam].append(HTGS)
        teams[X.iloc[i].AwayTeam].append(ATGS)
    
    max_len = utils.get_max_number_of_games_played(teams)
    GoalsScored = utils.create_df_from_dict(teams)
    GoalsScored = GoalsScored.T
    # Aggregate to get until that point
    
    for i in range(2,max_len):
        GoalsScored[i] = GoalsScored[i] + GoalsScored[i-1]

    return GoalsScored

def get_goals_conceded(X: pd.DataFrame):
    """ get goals conceded aggregated by teams and matchweek """
    teams = utils.create_team_dictionary(X)

    for i in range(len(X)):
        ATGC = X.iloc[i]["FTHG"]
        HTGC = X.iloc[i]["FTAG"]
        teams[X.iloc[i].HomeTeam].append(HTGC)
        teams[X.iloc[i].AwayTeam].append(ATGC)

    max_len = utils.get_max_number_of_games_played(teams)
    GoalsConceded = utils.create_df_from_dict(teams)
    GoalsConceded = GoalsConceded.T
    # Aggregate to get uptil that point
    
    for i in range(2,max_len):
        GoalsConceded[i] = GoalsConceded[i] + GoalsConceded[i-1]

    return GoalsConceded
    
def get_goals_statistics(X: pd.DataFrame):
    GC = get_goals_conceded(X)
    GS = get_goals_scored(X)

    j = 1
    HTGS = []
    ATGS = []
    HTGC = []
    ATGC = []


    for i in range(len(X)):
        ht = X.iloc[i].HomeTeam
        at = X.iloc[i].AwayTeam
        HTGS.append(GS.loc[ht][j])
        ATGS.append(GS.loc[at][j])
        HTGC.append(GC.loc[ht][j])
        ATGC.append(GC.loc[at][j])
        
        if ((i + 1)% 10) == 0:
            j = j + 1
        
    X["HTGS"] = HTGS
    X["ATGS"] = ATGS
    X["HTGC"] = HTGC
    X["ATGC"] = ATGC
    
    return X

def get_goal_difference(X: pd.DataFrame):
    X["HTGD"] = X["HTGS"] - X["HTGC"]
    X["ATGD"] = X["ATGS"] - X["ATGC"]
    return X
