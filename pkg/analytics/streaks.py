import pandas as pd

def get_3_game_ws(game_string: str):
    if game_string[-3:] == "WWW":
        return 1
    else:
        return 0

def get_5_game_ws(game_string: str):
    if game_string[-5:] == "WWWWW":
        return 1
    else:
        return 0

def get_3_game_ls(game_string: str):
    if game_string[-3:] == "LLL":
        return 1
    else:
        return 0

def get_5_game_ls(game_string: str):
    if game_string[-5:] == "LLLLL":
        return 1
    else:
        return 0

def no_draws_in_last_3_games(game_string: str):
    draw = 1
    for letter in game_string[-3:]:
        if letter == "D":
            draw = 0
    return draw

def no_draws_in_last_5_games(game_string: str):
    draw = 1
    for letter in game_string[-5:]:
        if letter == "D":
            draw = 0
    return draw

def get_streak_features(X: pd.DataFrame):
    X["HTWinStreak3"] = X["HTFormPtsStr"].apply(get_3_game_ws)
    X["HTWinStreak5"] = X["HTFormPtsStr"].apply(get_5_game_ws)
    X["HTLossStreak3"] = X["HTFormPtsStr"].apply(get_3_game_ls)
    X["HTLossStreak5"] = X["HTFormPtsStr"].apply(get_5_game_ls)
    X["HTNoDrawInLast3Games"] = X["HTFormPtsStr"].apply(no_draws_in_last_3_games)
    X["HTNoDrawInLast5Games"] = X["HTFormPtsStr"].apply(no_draws_in_last_5_games)


    X["ATWinStreak3"] = X["ATFormPtsStr"].apply(get_3_game_ws)
    X["ATWinStreak5"] = X["ATFormPtsStr"].apply(get_5_game_ws)
    X["ATLossStreak3"] = X["ATFormPtsStr"].apply(get_3_game_ls)
    X["ATLossStreak5"] = X["ATFormPtsStr"].apply(get_5_game_ls)
    X["ATNoDrawInLast3Games"] = X["ATFormPtsStr"].apply(no_draws_in_last_3_games)
    X["ATNoDrawInLast5Games"] = X["ATFormPtsStr"].apply(no_draws_in_last_5_games)
    
    return X