import sys
import traceback
sys.path.append("../")
from config import config
from pkg.ml import (
    trainer
)
from pkg.data import (
    fetcher,
    split
)
from pkg.preprocessor import (
    pipelines
)
import logging

def main():
    # Fetch data
    logging.info(f"Fetching data ...")
    df = fetcher.fetch_csv_data()
    
    # Enrich and Prepare data for ML 
    logging.info(f"Enriching data ...")
    df = Pipelines.data_pipeline.fit_transform(df)
    
    # Split data
    logging.info(f"Splitting data ...")
    X,y = split.split_df_into_x_y(df,config.target)
    X_train,X_test,y_train,y_test = split.split_data_into_train_test(X,y)
    
    
    # Fitting ml pipeline
    logging.info(f"Fitting model ...")
    trained_model = trainer.train_model(Pipelines.ml_pipeline,X_train,y_train)

    # save model
    logging.info(f"Saving Model ...")
    trainer.save_model(trained_model, config.model_path)
    trainer.save_model(trained_model, config.model_swagger_path)
    

if __name__ == "__main__":
    # Instanciate Pipeline Struct and get required pipelines
    Pipelines = pipelines.DataPipelines()
    Pipelines.get_data_enrich_pipeline(season_col=config.season_col,
                                       half_time_result=config.half_time_result,
                                       remove_feature_list=config.not_important_features,
                                       category_encoder_feature_list=config.category_encoder_feature_list,
                                       category_orderer_feature_list=config.category_orderer_feature_list,
                                       ml_feature_list=config.ml_feature_list)
    Pipelines.get_ml_pipeline()
    
    
    # Execute Main function of this Project
    try:
        main()
        sys.exit(0)
    except Exception as err:
        trc = traceback.format_exc()
        print('Exception during training: ' + str(err) + '\n' + trc, file=sys.stderr)
        sys.exit(255)




