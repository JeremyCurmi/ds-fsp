import pandas as pd

def get_match_week(X: pd.DataFrame):
    j = 1
    match_week = []
    for i in range(len(X)):
        match_week.append(j)

        if ((i+1)%10)==0:
            j+=1
    X["MW"] = match_week
    return X
