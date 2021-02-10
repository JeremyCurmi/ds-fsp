import sys
import goals
import points

from matplotlib import pyplot


sys.path.append("../../")
from pkg.data_fetching import fetcher
from pkg.preprocessor import (
    pipelines
)
def main():
    df = fetcher.fetch_csv_data("../../data/")

    for i in df["index"].unique():
        df_tr = df[df["index"]==i]

        goals_scored = goals.get_goals_scored(df_tr)
        goals_conceded = goals.get_goals_conceded(df_tr)

        gss = goals.get_goals_statistics(df_tr)
        matches = points.get_matches(df_tr)
        agg_points = points.get_agg_points(df_tr)
        print(agg_points)

if __name__ == "__main__":
    main()
