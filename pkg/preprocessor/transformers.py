import re
import warnings
import logging
import numpy as np
import pandas as pd
from datetime import datetime as dt

from sklearn import (
    base,
    compose,
    impute,
    preprocessing,
    decomposition,
    feature_selection
)

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

class DfTransformer(base.BaseEstimator, base.TransformerMixin):
    """
        Base Class for all transfomers, which outputs the data back to a dataframe object
    """
    def __init__(self, validate_features = True):
        self.columns = []
        self.validate_features = validate_features
     
    def get_feature_names(self):
        return self.columns
    
    
    def match_features(self, X):
        
        features_missing_from_train = list(set(X.columns) - set(self.columns))
        features_missing_from_test = list(set(self.columns) - set(X.columns))

        missing_features = False
        
        if len(features_missing_from_test) > 0:
            for feature in features_missing_from_test:
                if X[feature].dtype ==object:
                    X[feature] = '0'
                else:
                    X[feature] = 0
                missing_features = True
                
        if len(features_missing_from_train) > 0:
            for feature in features_missing_from_train:
                del X[feature]
                missing_features = True

        if missing_features:
            warnings.warn('Notice: Certain features in the test data do not match the ones in the training data. This issue has been resolved.',UserWarning)
        
        return X
    
    
    def feature_validator(self, X):
        if len(self.columns) > 0:
            if self.validate_features:
                X = self.match_features(X)
        return X
    
class FeatureTransformer(DfTransformer):
    '''
        The Role of this Transformer is to apply transformations to specific features only.
        params:
        1. transformers -> a list of tuples in the form (name,transformer,features), specifying 
        transformer objects to be applied to subsets of the data
            a. features -> can be either a list or a Callable make_column_selector to select specific
            columns by name or type
        2. remainder -> {'drop','passthrough'}, if drop then return only defined features, if passthrough
        then the remaining features are concatendated with the output transformed features (to get all of the data).
    '''
    def __init__(self, transformers, n_jobs=1, sparse_threshold=0.3, transformer_weights = None, verbose = False, remainder="passthrough"):
        self.transformers = transformers
        self.remainder = remainder
        self.n_jobs = n_jobs
        self.sparse_threshold = sparse_threshold
        self.columns = []
        self.column_types = None
        
        self.feature_transformer = compose.ColumnTransformer(
            transformers = self.transformers,
            remainder = self.remainder,
            n_jobs = self.n_jobs,
            sparse_threshold = self.sparse_threshold
        )
        
    
    def fit(self, X, y=None):
        self.get_available_features(X)
        self.feature_transformer.fit(X)
        return self
    
    def transform(self, X, y=None):
        X_tr = self.feature_transformer.transform(X)
        self.columns = self.feature_transformer.get_feature_names()
        self.adjust_feature_names()

        X_tr = pd.DataFrame(X_tr, index = X.index, columns = self.columns)
        X_tr = self.redefine_feature_types(X_tr)
        return X_tr
    
    def adjust_feature_names(self):
        for i, col in enumerate(self.columns):
            self.columns[i] = col.split(sep="__")[-1]
    
    def redefine_feature_types(self, X):

        for col in X:
            X[col] = X[col].convert_dtypes(convert_string=False)
        return X
    
    def get_params(self, deep=True):
        return self.feature_transformer.get_params(deep=deep)
          
    def get_available_features(self,X):
        for i,transformer in enumerate(self.transformers):
            transformer_columns = [col for col in transformer[-1] if col in X.columns.tolist()]
            self.transformers[i] = list(self.transformers[i])
            self.transformers[i][-1] = transformer_columns
            self.transformers[i] = tuple(self.transformers[i])
            
            removed_feature_list = list(set(transformer[-1])-set(self.transformers[i][-1]))
            if len(removed_feature_list) > 0:
                logging.info(f"The following features: {removed_feature_list} were removed because they were no longer present in the data")

class InputCleaner(DfTransformer):
    def __init__(self, 
                 null_pct_threshold: float = 0.9,
                 validate_features: bool = True):
        
        self.null_pct_threshold = null_pct_threshold
        self.validate_features = validate_features
        self.columns = []
                
        
    def fit(self, X, y=None):
       return self
   
    def transform(self, X, y=None):
        X_tr = X.copy()
        
        # remove mostly empty features
        X_tr = self.drop_mostly_empty_features(X_tr)
        
        # remove uni-valued features
        X_tr = self.drop_only_one_value_features(X_tr)

        # fix date feature
        X_tr["year"] = self.get_year_from_date_col(X_tr["Date"])
        X_tr["month"] = self.get_month_from_date_col(X_tr["Date"])
        X_tr["day"] = self.get_day_from_date_col(X_tr["Date"])

        # remove Date feature
        del X_tr["Date"]

        # validate that test data and train data have the same features
        X_tr = super().feature_validator(X_tr)
        self.columns = X_tr.columns
        return X_tr
    
    def drop_mostly_empty_features(self, X):
        
        not_null_feature_list = X.columns[X.isnull().mean() < self.null_pct_threshold]
        null_feature_list = [feat for feat in X.columns if feat not in not_null_feature_list]
        
        if len(null_feature_list) > 0:
            warnings.warn(f'The following features: {null_feature_list} were removed because they exceeded the null % threshold: {self.null_pct_threshold}')
            
        return X[not_null_feature_list]
        
    def drop_only_one_value_features(self, X):
        
        not_one_value_feature_list = X.columns[X.nunique()!=1]
        one_value_feature_list = [feat for feat in X.columns if feat not in not_one_value_feature_list]
        
        if len(one_value_feature_list) > 0:
            warnings.warn(f'The following features: {one_value_feature_list} were removed because they contain only one value')
            
        return X[not_one_value_feature_list]
    
    def get_year_from_date_col(self,col):
        return pd.DatetimeIndex(col).year  

    def get_month_from_date_col(self,col):
        return pd.DatetimeIndex(col).month

    def get_day_from_date_col(self,col):
        return pd.DatetimeIndex(col).day

    def get_feature_names(self):
        return self.columns


