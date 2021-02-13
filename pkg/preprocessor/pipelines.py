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
                                 half_time_result: bool = False,
                                 remove_feature_list: list = [],
                                 category_encoder_feature_list: list = [],
                                 category_orderer_feature_list: list = []):
        """
            This pipeline enriches the data input and removes 2nd half features, since the
            goal of this project is to predict FT score using data till the end of the first half.
        """
        category_pipeline = transformers.FeatureTransformer(
            [("subprocess_categoricalencoder",transformers.CategoricalEncoder(method="nominal",drop_first="first"),category_encoder_feature_list),
             ("subprocess_categoricalorderer",transformers.CategoricalEncoder(method="ordinal"),category_orderer_feature_list),]
        )
        self.data_pipeline = pipeline.Pipeline(
            steps = [
                ("analytics", transformers.Analytics(season_col,half_time_result)),
                ("remover", transformers.Remover(remove_feature_list)),
                ("inputcleaner", transformers.InputCleaner()),
                ("categoricalencoder", category_pipeline)
            ]
        )

    def get_preprocess_pipeline(self,
                                remove_feature_list: list = []):
        """
            Build preprocess pipeline which will be the first part of the prediction pipeline
        """

        self.preprocessing_pipeline = pipeline.Pipeline(
            steps = [
                ("inputcleaner", transformers.InputCleaner()),
            ]
        )



        