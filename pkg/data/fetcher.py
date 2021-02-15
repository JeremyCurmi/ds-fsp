import glob
import pandas as pd 
from datetime import datetime as dt

def fetch_csv_data(path = "data/"):
    all_files = glob.glob(path + "/*.csv")
    
    df_big = pd.DataFrame()
    
    for i,filename in enumerate(all_files):
        df = pd.read_csv(filename, index_col=None)
        df["season_end_year"] = pd.DatetimeIndex(df["Date"]).year.max()
        df_big = df_big.append(df)
    
    return df_big


        
        
