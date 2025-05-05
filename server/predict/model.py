import lightgbm as lgb

loaded_model = lgb.Booster(model_file="model.txt")

y_pred = loaded_model.predict(data)