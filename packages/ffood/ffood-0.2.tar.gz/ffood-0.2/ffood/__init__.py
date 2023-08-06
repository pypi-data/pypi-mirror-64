import pandas as pd
import numpy as np
import lightgbm as lgb
import shap


def norm(series):
  max_value = series.max()
  min_value = series.min()
  result = (series - min_value) / (max_value - min_value)
  return result 

def outlier_observation(X_pr, target, itters):

  X_pr.index.name = 'index'

  #X_pr = X_pr.sample(500)   

  da =0
  leng = itters
  for r in range(leng):
    da += 1
    first = X_pr.sample(int(len(X_pr)/2))
    second = X_pr[~X_pr.isin(first)].dropna()

    d_train = lgb.Dataset(first.drop(columns=[target]), label=first[target])
    d_valid = lgb.Dataset(second.drop(columns=[target]), label=second[target])

    params = {
        'boosting_type': 'gbdt',
        'objective': 'regression',
        'bagging_fraction': 0.2,
        'metric': 'rmsle',
        'max_depth': 6, 
        'learning_rate': 0.1,
        'verbose': 0,
      'num_threads':16}
    n_estimators = 100

    model = lgb.train(params, d_train, 100, verbose_eval=1)

    preds = model.predict(second)

    #predictions = np.clip(preds, df[target].min(), df[target].max())

    second[target+ "_prediction"] = norm(preds) # predictions
    second["real_"+target] = norm(second[target])

    second[target+ "_prediction"] = norm(preds) # predictions
    second["real_"+target] = norm(second[target])

    second["over_prediction_percentage"] = second[target+ "_prediction"] -  second["real_"+target]


    model = lgb.train(params, d_valid, 100, verbose_eval=1)

    preds = model.predict(first)

    #predictions = np.clip(preds, df[target].min(), df[target].max())


    first[target+ "_prediction"] = norm(preds) # predictions
    first["real_"+target] = norm(first[target])

    first["over_prediction_percentage"] = first[target+ "_prediction"] -  first["real_"+target]


    final = pd.concat((first, second), axis=0)

    if da==1:
      framed = final.sort_index()
    else:
      framed = framed.sort_index() + final.sort_index()

  framed = framed.sort_values("over_prediction_percentage",ascending=False)

  ## remove items with no residuals, should only be a few. 
  framed = framed.replace([np.inf, -np.inf], np.nan).dropna(subset=["over_prediction_percentage"], how="all") # not needed but safe

  #print(second.reset_index())

  framed = framed/leng
  high = framed.reset_index().head()[["index","over_prediction_percentage",target+ "_prediction","real_"+target]]
  high.columns = ["Overprediction Index", "Overpredict Percentage", "Predicted (O)", "Actual (O)"]
  high["Overpredict Percentage"] = (high["Overpredict Percentage"]*100).astype(int)

  low = framed.iloc[::-1].reset_index().head()[["index","over_prediction_percentage",target+ "_prediction","real_"+target]]
  low.columns = ["Underprediction Index", "Underpredict Percentage","Predicted (U)", "Actual (U)"]
  low["Underpredict Percentage"] = (low["Underpredict Percentage"]*100).astype(int)


  observations = pd.merge(high, low,left_index=True, right_index=True,how="left") 

  return observations, framed, framed.index



def feature_calcs(framed, target, original):

  overpred_target = "over_prediction_percentage"

  if original:
    cols_drop = [ overpred_target, target+ "_prediction", "real_"+target,target ]
    d_framed = lgb.Dataset(framed.drop(columns=cols_drop), label=framed[target])           ## here I disolve the log1p for features
  else:
    cols_drop = [overpred_target,  target+ "_prediction", "real_"+target]
    d_framed = lgb.Dataset(framed.drop(columns=cols_drop), label=framed[overpred_target])  ## here I disolve the log1p for features

  shap_drop = [overpred_target,  target+ "_prediction", "real_"+target, target]
  d_shap = lgb.Dataset(framed.drop(columns=shap_drop), label=framed[overpred_target])


  #cols_drop = [overpred_target, target+ "_prediction", "real_"+target]

  f = -1
  seeder  = [15,1,6,7,2]
  for seeds in seeder:
      f = f +1
      print("Training Iteration: "+ str(f+1)+"/"+str(5))

      params = {
        'boosting_type': 'gbdt',
        'objective': 'regression',
        'metric': 'rmsle',
        'max_depth': 6, 
        'learning_rate': 0.1,
        'verbose': 0,
      'num_threads':16}
      n_estimators = 100

      params["feature_fraction_seed"] = seeds
      
      params["random_seed"] = seeds + 1


      # Table values
      model = lgb.train(params, d_framed, verbose_eval=1000)

      explainer = shap.TreeExplainer(model)

      shap_values = explainer.shap_values(framed.drop(cols_drop, axis=1))

      shap_fram = pd.DataFrame(shap_values[:,:], columns=list(framed.drop(cols_drop, axis=1).columns))

      shap_new = shap_fram.sum().sort_values().to_frame()

      shap_new.columns = ["SHAP"]
      if original:
        shap_new["SHAP_abs"] = shap_new["SHAP"].abs()

      ## Shap visuals
      model_shap = lgb.train(params, d_shap, verbose_eval=1000)

      explainer_shap = shap.TreeExplainer(model_shap)

      shap_values_sans = explainer_shap.shap_values(framed.drop(shap_drop, axis=1))

      
      if f==0:
          shap_fin = shap_new
          shap_val = shap_values_sans
      else:
          shap_fin = shap_fin + shap_new
          shap_val = shap_val + shap_values_sans

  shap_val = shap_val/len(seeder)

  shap_fin = shap_fin.sort_values("SHAP", ascending=False)

  return shap_fin, shap_val, explainer_shap


def feature_frame(framed, target):
 
  print("Overprediction Importance")
  feature_over, shap_val, explainer = feature_calcs(framed,target,False)

  feature_over = feature_over[~feature_over.index.isin([target])]
  feature_over = feature_over.reset_index()

  high = feature_over.reset_index(drop=True).head()
  high.columns = ["Larger Feature Leads to Overprediction (FLO)", "FLO Value"]
  high["FLO Value"] = high["FLO Value"].abs()

  print("...........")

  low = feature_over.iloc[::-1].reset_index(drop=True).head() 
  low.columns = ["Larger Feature Leads to Underprediction (FLU)", "FLU Value"]
  low["FLU Value"] = low["FLU Value"].abs()

  print("Original Importance")
  feature_org , _, _ = feature_calcs(framed,target,True)
  top = feature_org.sort_values("SHAP_abs",ascending=False).drop(columns=["SHAP"]).reset_index().head()
  top.columns = ["Top Feature", "ABS SHAP Value"]

  over_under = pd.merge(top, high,left_index=True, right_index=True,how="left")
  over_under = pd.merge(over_under, low,left_index=True, right_index=True,how="left")

  return over_under, shap_val, explainer


def outliers(X_pr, columns=None):
  targets = ["number_of_reviews","price"]

  shap_val_dict = {}
  shap_exp_dict = {}
  if columns==None:
    targets = list(X_pr.columns)
  else:
    targets = columns
  print(targets)
  ka = 0 
  
  for target in targets:
    ka += 1

    print("Start " + target + " ("+str(ka)+"/"+str(len(targets))+")")

    try:
      observations, framed, ind = outlier_observation(X_pr, target, 5)
      observations.insert(loc=0, column="Predicted Feature", value=target)
      cols_preserve = list(observations.columns)

    except ValueError:
      print("The dataset is too small, or the feature " + target + " doesn't change in value enough")
      continue

    feature,shap_values, explainer  = feature_frame(framed,target) ### features of observations

    try:
      feature,shap_values, explainer  = feature_frame(framed,target) ### features of observations
      print("success")
    except:
      print(framed.head())
      print("Bad Feature")
      continue
    #unit = pd.merge(observations, frame,left_index=True, right_index=True,how="left")
    feature.insert(loc=0, column="Predicted Feature", value=target)

    shap_val_dict[target] = shap_values 
    shap_exp_dict[target] = explainer

    if ka==1:
      full_feature = feature
      full_observation = observations
    else:
      full_feature = pd.concat((full_feature, feature),axis=0)

      full_observation = pd.concat((full_observation, observations),axis=0)
    
    print(full_observation.columns)
    print(cols_preserve)
    full_observation.columns = cols_preserve

    print(" ")
    print("Completed " + target + " ("+str(ka)+"/"+str(len(targets))+")")
    print("=================== ")


  return full_observation, full_feature, shap_val_dict, shap_exp_dict, ind

