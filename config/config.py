# remove data leakage features
season_col="season_end_year"
target="FTR"
half_time_result=True
not_important_features=["FTHG","FTAG","HomeTeam","AwayTeam","Referee","Time","Date","MW","HTFormPtsStr","ATFormPtsStr"]
category_encoder_feature_list = ["HTR","HM1","AM1","HM2","AM2","HM3","AM3","HM4","AM4","HM5","AM5"]
category_orderer_feature_list = []
ml_feature_list = ["FTR","DiffPts","HTHG","B365H","B365D","HTLossStreak3","HTR_H","HTP","DiffFormPts","ATFormPts"]
model_path = "app/models/model.pkl"
model_swagger_path = "app-swagger/models/model.pkl"

model_name = "model"


