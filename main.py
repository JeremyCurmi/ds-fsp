import sys
sys.path.append("../")

from pkg.data_fetching import fetcher
from pkg.preprocessor import (
    pipelines
)

def main():
    df = fetcher.fetch_csv_data()

    df_clean = pipelines.preprocessing_pipe.fit_transform(df)

if __name__ == '__main__':
    main()




