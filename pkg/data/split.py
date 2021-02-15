import pandas as pd
from sklearn import model_selection

def split_df_into_x_y(df: pd.DataFrame,
                      target_feature_name: str= "target"):
    return df.drop(target_feature_name,axis=1),df[target_feature_name]

def split_data_into_train_test(X: pd.DataFrame,
                               y: pd.Series):
    return model_selection.train_test_split(X, y, random_state=1, test_size=0.3)
