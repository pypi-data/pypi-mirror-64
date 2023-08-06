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

  framed_old = framed.copy()
  
  high = framed.reset_index().head()[["index","over_prediction_percentage",target+ "_prediction","real_"+target]]
  high.columns = ["Overprediction Index", "Overpredict Percentage", "Predicted (O)", "Actual (O)"]
  high["Overpredict Percentage"] = (high["Overpredict Percentage"]*100).astype(int)

  low = framed.iloc[::-1].reset_index().head()[["index","over_prediction_percentage",target+ "_prediction","real_"+target]]
  low.columns = ["Underprediction Index", "Underpredict Percentage","Predicted (U)", "Actual (U)"]
  low["Underpredict Percentage"] = (low["Underpredict Percentage"]*100).astype(int)


  observations = pd.merge(high, low,left_index=True, right_index=True,how="left") 

  return observations, framed, framed.index, framed_old


def feature_calcs(second, target, original):

  overpred_target = "over_prediction_percentage"

  if original:
    cols_drop = [ overpred_target, target+ "_prediction", "real_"+target,target ]
    d_second = lgb.Dataset(second.drop(columns=cols_drop), label=second[target])
  else:
    cols_drop = [overpred_target,  target+ "_prediction", "real_"+target]
    d_second = lgb.Dataset(second.drop(columns=cols_drop), label=second[overpred_target])


  #cols_drop = [overpred_target, target+ "_prediction", "real_"+target]

  f = -1
  #for seeds in [15,1,6,7,2]:
  for seeds in [15]:
      f = f +1
      print("Training Iteration: "+ str(f+1)+"/"+str(5))

      params = {
        'boosting_type': 'gbdt',
        'objective': 'regression',
        'metric': 'rmsle',
        'bagging_fraction': 0.2,
        'max_depth': 6, 
        'learning_rate': 0.1,
        'verbose': 0,
      'num_threads':16}
      n_estimators = 100

      params["feature_fraction_seed"] = seeds
      
      params["random_seed"] = seeds + 1
      model = lgb.train(params, d_second, verbose_eval=1000)


      explainer = shap.TreeExplainer(model)
      shap_values = explainer.shap_values(second.drop(cols_drop, axis=1))

      shap_fram = pd.DataFrame(shap_values[:,:], columns=list(second.drop(cols_drop, axis=1).columns))

      # here you actually care about direction. 
      shap_new = shap_fram.mean().sort_values().to_frame()


      shap_new.columns = ["SHAP"]
      if original:
        shap_new["SHAP_abs"] = norm(shap_fram.abs().mean().sort_values().to_frame()) # here you actually care about size. 
      
      if f==0:
          shap_fin = shap_new
          shap_val = shap_values
      else:
          shap_fin = shap_fin + shap_new
          shap_val = shap_val + shap_values


  shap_fin = shap_fin.sort_values("SHAP", ascending=False)

  return shap_fin, shap_val, explainer

def feature_frame(second, target):
 
  print("First Half")
  feature_over, shap_val_res, explainer_res = feature_calcs(second,target,False)

  feature_over = feature_over[~feature_over.index.isin([target])]
  feature_over = feature_over.reset_index()

  high = feature_over.reset_index(drop=True).head()
  high.columns = ["Causes Overprediction (CO)", "Effect Size (CO)"]
  high["Effect Size (CO)"] = high["Effect Size (CO)"].abs()

  print("...........")

  low = feature_over.iloc[::-1].reset_index(drop=True).head() 
  low.columns = ["Causes Underprediction (CU)", "Effect Size (CU)"]
  low["Effect Size (CU)"] = low["Effect Size (CU)"].abs()

  print("Second Half")
  feature_org, shap_val, explainer = feature_calcs(second,target,True)
  top = feature_org.sort_values("SHAP_abs",ascending=False).drop(columns=["SHAP"]).reset_index().head()
  top.columns = ["Top Feature", "REL SHAP Value"]

  new = pd.merge(top, high,left_index=True, right_index=True,how="left")
  new = pd.merge(new, low,left_index=True, right_index=True,how="left")

  return new, shap_val_res, explainer_res

def tables(X_pr, columns=None):

  shap_val_dict = {}
  shap_exp_dict = {}

  if columns==None:
    targets = list(X_pr.columns)
  else:
    targets = columns

  print(targets)
  ka = 0 
  ind_dict = {}
  framed_dict = {}
  for target in targets:
    ka += 1

    print("Start " + target + " ("+str(ka)+"/"+str(len(targets))+")")

    try:
      observations, framed, ind, framed_old = outlier_observation(X_pr, target, 5)
      ind_dict[target] = ind
      framed_dict[target] = framed_old
      observations.insert(loc=0, column="Predicted Feature", value=target)
      cols_preserve = list(observations.columns)

    except ValueError:
      print("The dataset is too small, or the feature " + target + " doesn't change in value enough")
      continue

    try:
      feature,shap_values, explainer  = feature_frame(framed,target) ### features of observations
      print("success")
    except:
      #print(framed.head())
      print("Bad Feature")
      continue
    # unit = pd.merge(observations, framed,left_index=True, right_index=True,how="left")
    feature.insert(loc=0, column="Predicted Feature", value=target)

    shap_val_dict[target] = shap_values 
    shap_exp_dict[target] = explainer

    if ka==1:
      full_feature = feature
      full_observation = observations
    else:
      full_feature = pd.concat((full_feature, feature),axis=0)

      full_observation = pd.concat((full_observation, observations),axis=0)
    
    ## Doesn't seem like I am using full_observations
    full_observation.columns = cols_preserve

    print(" ")
    print("Completed " + target + " ("+str(ka)+"/"+str(len(targets))+")")
    print("=================== ")

  try:
    full_feature = full_feature
  except:
    full_feature = feature


  #### Feature Creation

  des = full_feature.groupby("Predicted Feature")["Predicted Feature"].count().to_frame().rename(columns={'Predicted Feature':'count'}); des.head()
  des.index.names = ["Features"]

  predictability = full_feature.groupby("Predicted Feature")["REL SHAP Value"].mean().sort_values(ascending=False); predictability
  des = pd.merge(des,predictability, left_index=True, right_index=True, how="left" ).rename(columns={'REL SHAP Value':'concentration'}); des.head()

  informativeness = full_feature.groupby("Top Feature")["REL SHAP Value"].mean().sort_values(ascending=False)
  des = pd.merge(des,informativeness, left_index=True, right_index=True, how="left" ).rename(columns={'REL SHAP Value':'informativeness'}); des.head()

  #observation_overprediction_errors = full_feature.groupby("Overprediction Index")["Overprediction Index"].count().sort_values(ascending=False);observation_overprediction_errors

  #observation_underprediction_errors = full_feature.groupby("Underprediction Index")["Underprediction Index"].count().sort_values(ascending=False)


  deceptive_overpredicting = full_feature.groupby("Causes Overprediction (CO)")["Effect Size (CO)"].mean().sort_values(ascending=False)*100; deceptive_overpredicting
  des = pd.merge(des,deceptive_overpredicting, left_index=True, right_index=True, how="left" ).rename(columns={'Effect Size (CO)':'overpredictor'}); des.head()


  deceptive_underpredicting = full_feature.groupby("Causes Underprediction (CU)")["Effect Size (CU)"].mean().sort_values(ascending=False)*100; deceptive_underpredicting
  des = pd.merge(des,deceptive_underpredicting, left_index=True, right_index=True, how="left" ).rename(columns={'Effect Size (CU)':'underpredictor'}); des.head()

  prediction_volatility = full_observation.groupby("Predicted Feature")[["Overpredict Percentage","Underpredict Percentage"]].mean(); prediction_volatility
  prediction_volatility = prediction_volatility["Overpredict Percentage"].abs() + prediction_volatility["Underpredict Percentage"].abs()

  prediction_volatility = prediction_volatility.sort_values(ascending=False); prediction_volatility.head()

  des = pd.merge(des,prediction_volatility.to_frame().rename(columns={0:'misprediction'}), left_index=True, right_index=True, how="left" ); des.head()

  del des["count"]
  des.fillna(value=0, inplace=True)
  add = pd.DataFrame(index=range(len(des)))
  for col in des.columns:
    here = des.sort_values(col,ascending=False)[col]
    add[col + " Feature"] = here.index
    add[col + " Value"] = here.values

  return full_observation, full_feature, add, shap_val_dict, shap_exp_dict, ind_dict, framed_dict

