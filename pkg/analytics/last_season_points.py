import pandas as pd

def get_points_by_season_dataframe(X: pd.DataFrame,
                                   season_col: str):
    HT = X[[season_col,"HomeTeam","HTP"]].groupby(["HomeTeam",season_col])["HTP"].max()
    AT = X[[season_col,"AwayTeam","ATP"]].groupby(["AwayTeam",season_col])["ATP"].max()
    X_points = pd.concat([HT,AT],axis=1)
    X_points["TP"] = X_points.max(axis=1)
    del X_points["HTP"]
    del X_points["ATP"]
    return X_points.reset_index()

def add_points_last_season_to_data(X: pd.DataFrame,
                                   season_col: str):
    X_points = get_points_by_season_dataframe(X, season_col)
    X_points[season_col] = X_points[season_col]+1
    X_points = X_points.rename(columns={"level_0":"HomeTeam"})
    X = X.merge(X_points[["HomeTeam",season_col,"TP"]],on=["HomeTeam",season_col], how="left")
    X = X.rename(columns = {"TP":"HTPLS"})
    X_points = X_points.rename(columns={"HomeTeam":"AwayTeam"})
    X = X.merge(X_points[["AwayTeam",season_col,"TP"]],on=["AwayTeam",season_col], how="left")
    X = X.rename(columns = {"TP":"ATPLS"})
    return X

def get_last_season_points_difference(X: pd.DataFrame):
    X["DiffPLS"] = X["HTPLS"] - X["ATPLS"]
    return X