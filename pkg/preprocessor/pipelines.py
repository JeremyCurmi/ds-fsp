from sklearn import pipeline
from pkg.preprocessor import (
    transformers
)


class DataPipelines:
    def __init__(self):
        data_pipeline           = None
        preprocessing_pipeline  = None

    def get_data_enrich_pipeline(self, 
                                 season_col: str,
                                 remove_feature_list: list = []):
        """
            This pipeline enriches the data input and removes 2nd half features, since the
            goal of this project is to predict FT score using data till the end of the first half.
        """
        self.data_pipeline = pipeline.Pipeline(
            steps = [
                ("analytics",transformers.Analytics(season_col)),
                ("remover",transformers.Remover(remove_feature_list)),
            ]
        )

    def get_preprocess_pipeline(self):
        """
            Build preprocess pipeline which will be the first part of the prediction pipeline
        """
        self.preprocessing_pipeline = pipeline.Pipeline(
            steps = [
                ("inputcleaner", transformers.InputCleaner()),
            ]
        )



        