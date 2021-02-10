import pandas as pd
import utils

def get_points(result):
    if result == "W":
        return 3 
    elif result == "D":
        return 1
    else:
        return 0

def get_cuml_points(matches: pd.DataFrame):
    match_points = matches.applymap(get_points) 
    
    for i in range(2,matches.shape[1] + 1):   
        match_points[i] = match_points[i] + match_points[i-1]
    
    match_points.insert(column = 0, loc = 0, value = [0*i for i in range(matches.shape[0])])
    return match_points

def get_matches(X: pd.DataFrame):
    teams = utils.create_team_dictionary(X)

    for i in range(len(X)):
        if X.iloc[i].FTR == "H":
            teams[X.iloc[i].HomeTeam].append("W")
            teams[X.iloc[i].AwayTeam].append("L")
        elif X.iloc[i].FTR == "A":
            teams[X.iloc[i].AwayTeam].append("W")
            teams[X.iloc[i].HomeTeam].append("L")
        else:
            teams[X.iloc[i].HomeTeam].append("D")
            teams[X.iloc[i].AwayTeam].append("D")

    max_len = utils.get_max_number_of_games_played(teams)+1
    matches = utils.create_df_from_dict(teams)
    matches = matches.T
    # matches = pd.DataFrame(data=teams, index = [i for i in range(1,max_len)]).T
    return matches

def get_agg_points(X: pd.DataFrame):
    matches = get_matches(X)
    cum_pts = get_cuml_points(matches)

    HTP = []
    ATP = []
    j = 0

    for i in range(len(X)):
        ht = X.iloc[i].HomeTeam
        at = X.iloc[i].AwayTeam
        HTP.append(cum_pts.loc[ht][j])
        ATP.append(cum_pts.loc[at][j])
    
        if ((i + 1)% 10) == 0:
                j = j + 1

    X["HTP"] = HTP
    X["ATP"] = ATP
    return X