import sys
import traceback
sys.path.append("../")
from config import config
from pkg.data_fetching import fetcher
from pkg.preprocessor import (
    pipelines
)

def main():
    # Fetch data
    df = fetcher.fetch_csv_data()
    
    # Enrich and Prepare data for ML 
    df = Pipelines.data_pipeline.fit_transform(df)

    # preprocessing pipe ... this should be leading to the model pipeline
    # df = Pipelines.preprocessing_pipeline.fit_transform(df)


    df.to_csv("analytics.csv")


if __name__ == "__main__":
    # Instanciate Pipeline Struct and get required pipelines
    Pipelines = pipelines.DataPipelines()
    Pipelines.get_data_enrich_pipeline(season_col=config.season_col,
                                       half_time_result=config.half_time_result,
                                       remove_feature_list=config.not_important_features,
                                       category_encoder_feature_list=config.category_encoder_feature_list,
                                       category_orderer_feature_list=config.category_orderer_feature_list)
    Pipelines.get_preprocess_pipeline()
    
    
    # Execute Main function of this Project
    try:
        main()
        sys.exit(0)
    except Exception as err:
        trc = traceback.format_exc()
        print('Exception during training: ' + str(err) + '\n' + trc, file=sys.stderr)
        sys.exit(255)




