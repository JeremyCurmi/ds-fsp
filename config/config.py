# remove data leakage features
season_col="season_end_year"
half_time_result=True
not_important_features=["FTHG","FTAG","HomeTeam","AwayTeam","Referee","Time","Date","MW"]
category_encoder_feature_list = ["HTR","HM1","AM1","HM2","AM2","HM3","AM3","HM4","AM4","HM5","AM5"]
category_orderer_feature_list = ["HTFormPtsStr", "ATFormPtsStr"]