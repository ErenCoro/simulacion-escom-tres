from sklearn import linear_model 
import pandas as pd 
import numpy as np

def dataframe(url_csv,  labels = 'prediction') :
    name = url_csv
    df = pd.read_csv(name)
    df_features = df.drop([labels], axis=1)
    df_label = df[labels]
    return df_features, df_label


def train_SGDR(data_url,learning_rate, iterations):

    features, label = dataframe(data_url)
    sgdr = linear_model.SGDRegressor(max_iter = iterations, eta0 = learning_rate, tol = 0)
    sgdr.fit (features, label)
    weight = sgdr.coef_
    bias = sgdr.intercept_
    weights = weight.tolist()
    weights.insert(0, bias[0])
    output = {"model_weights":[]}
    output["model_weights"] += weights
    return  output


def test_SGDR(model_weights, input_data):
    y_pred =[]
    for i in range(len(input_data)):
        y_pred.append(model_weights[0] + np.matmul(np.array(model_weights[1:]), np.array(input_data[i])))
    
    output = {"prediction":[]}
    output["prediction"] += y_pred
    return  output
    
    
  
