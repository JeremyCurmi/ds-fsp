import pandas as pd
try:
    import pkg.analytics.utils as utils
    import pkg.analytics.points as points
except:
    import utils
    import points

def get_form(X: pd.DataFrame, 
             num: int):
    form = points.get_matches(X)
    form_final =  form.copy()

    for i in range(num,form.shape[1]+1):
        form_final[i] = ""
        j = 0
        while j < num:
            form_final[i] += form[i-j]
            j += 1
    return form_final

def add_form(X: pd.DataFrame,
             num: int):
    form = get_form(X,num)
    h = ["M" for i in range(num * 10)]
    a = ["M" for i in range(num * 10)]

    j = num
    for i in range((num*10),len(X)):
        ht = X.iloc[i].HomeTeam
        at = X.iloc[i].AwayTeam

        past = form.loc[ht][j]
        h.append(past[num-1])

        past = form.loc[at][j]               # get past n results.
        a.append(past[num-1])                   # 0 index is most recent
        
        if ((i + 1)% 10) == 0:
            j = j + 1

    X["HM" + str(num)] = h                 
    X["AM" + str(num)] = a

    return X

def add_form_df(X: pd.DataFrame):
    for i in range(1,6):
        X = add_form(X,i)
    return X

def get_form_points(form_string: str):
    sum = 0
    for letter in form_string:
        sum += points.get_points(letter)
    return sum 

def get_last_5_games_form_points(X: pd.DataFrame):
    """
        Calculate points of last 5 games i.e. WWWWWW -> 15 for both HT and AT
    """
    X["HTFormPtsStr"] = X["HM1"] + X["HM2"] + X["HM3"] + X["HM4"] + X["HM5"]
    X["ATFormPtsStr"] = X["AM1"] + X["AM2"] + X["AM3"] + X["AM4"] + X["AM5"]

    X["HTFormPts"] = X["HTFormPtsStr"].apply(get_form_points)
    X["ATFormPts"] = X["ATFormPtsStr"].apply(get_form_points)

    return X