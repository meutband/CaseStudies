import numpy as np
import pandas as pd
import cPickle
from sklearn.ensemble import RandomForestClassifier

#gets model from pkl file
def get_model(filename):
    with open(filename, 'rb') as f_un:
        return cPickle.load(f_un)

#gets X set from the dataframe to use later.
def get_data(dataframe):

    columns = dataframe.columns.values

    cols = []
    for col in columns:
       if dataframe[col].dtype != 'object':
           cols.append(col)

    X = dataframe.copy()[cols].fillna(0)

    return X

#combines the modules from above and predicts fraud and the probability of
#(not fraud, fraud)
def unit1(dataframe):

    model_file = "model.pkl"
    model = get_model(model_file)

    X = get_data(dataframe)

    pred = model.predict(X)
    prob = model.predict_proba(X)
    return pred, prob
