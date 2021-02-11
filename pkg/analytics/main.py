import sys
import goals
import points
import team_form
import last_season_points
import match_week
import streaks
import pandas as pd

sys.path.append("../../")
from pkg.data_fetching import fetcher
from pkg.preprocessor import (
    pipelines
)

SEASON_COL = "season_end_year"

def main():
    df = fetcher.fetch_csv_data("../../data/")
    df_analytics = pd.DataFrame()
    
    for i in df[SEASON_COL].unique():
        df_tr = df[df[SEASON_COL]==i]

        goals_scored = goals.get_goals_scored(df_tr)
        goals_conceded = goals.get_goals_conceded(df_tr)

        gss = goals.get_goals_statistics(df_tr)
        matches = points.get_matches(df_tr)
        agg_points = points.get_agg_points(df_tr)
        
        df_tr = team_form.add_form_df(df_tr)
        df_tr = match_week.get_match_week(df_tr)
        
        # compute form points
        df_tr = team_form.get_last_5_games_form_points(df_tr)

        # compute streak features
        df_tr = streaks.get_streak_features(df_tr)

        # append dfs into one
        df_analytics = df_analytics.append(df_tr)

    # add last season points to data
    df_analytics = last_season_points.add_points_last_season_to_data(df_analytics,SEASON_COL)
    df_analytics.to_csv("test.csv")
    

if __name__ == "__main__":
    main()
