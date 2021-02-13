import pandas as pd

def create_team_dictionary(X: pd.DataFrame):
    # create a dictionary with team names as keys
    teams_keys = X["HomeTeam"].unique()
    teams_values = [[] for x in range(len(teams_keys))]
    teams = dict(zip(teams_keys,teams_values))
    return teams

def get_list_with_len_of_values_of_dict(teams: dict):
    return [len(v) for _,v in teams.items()]

def get_max_number_of_games_played(teams: dict):
    return max(get_list_with_len_of_values_of_dict(teams))

def create_df_from_dict(teams: dict):
    # check length of values of dict
    list_len = get_list_with_len_of_values_of_dict(teams)
    list_len_max = max(list_len)
    
    all_values_equal = True
    
    for elm in list_len:
        if elm != list_len_max:
            all_values_equal = False
            continue

    if all_values_equal:
        df = pd.DataFrame(data = teams)
        df.index += 1
    else:
        df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in teams.items()]))
        df.index += 1
    
    return df


def scale_features_by_a_specific_feature(X: pd.DataFrame, list_of_features, feature_scaler):
    X[feature_scaler] = X[feature_scaler].astype(float)

    for col in list_of_features:
        X[col] = X[col]/X[feature_scaler]
    
    return X