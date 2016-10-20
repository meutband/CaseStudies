import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score, recall_score, precision_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier

def scores(ytest, ypred):
    mse = mean_squared_error(ytest, ypred)
    acs = accuracy_score(ytest, ypred)
    rs = recall_score(ytest, ypred)
    ps = precision_score(ytest, ypred)
    return mse, acs, rs, ps

if __name__ == '__main__':

    df = pd.read_csv('churn.csv', parse_dates=['last_trip_date','signup_date'])

    #Cleaining data
    df['num_days'] = pd.to_datetime('07-01-2014')-df['last_trip_date']
    days = pd.to_datetime('07-01-2014')-df['last_trip_date']
    day_diff = days.astype('timedelta64[D]')>30
    df['churn'] = day_diff
    df['churn'] = df['churn'].astype(int)

    #Filling empty values, all True/False and Yes/No to 1/0
    df.replace({'False.': 0, 'True.': 1, 'yes': 1, 'no': 0}, inplace=True)
    df = df.fillna(df.mean())

    #Getting X, y for the model. Choose the columns based on personal though
    df['luxury_car_user'] = df['luxury_car_user'].astype(int)
    X = df[['luxury_car_user', 'trips_in_first_30_days', 'weekday_pct']]
    y = df['churn']

    #Split the data into training set and test set (70%, 30%)
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.30)
    RF = RandomForestClassifier(n_estimators=128, random_state=1)
    RF.fit(X_train, y_train)

    #Use model to predict churn (1/0). Calculate mean_squared_error, accuracy_score,
    #recall_score, precision_score and print confusion_matrix
    y_pred = RF.predict(X_test)
    mse, acs, rs, ps = scores(y_test, y_pred)
    print 'Mean_Sqaured_Error', mse
    print 'Accuracy_Score', acs
    print 'Recall_Score', rs
    print 'Precision_Score', ps
    print confusion_matrix(y_test, y_pred)

    #sklearn.confusion_matrix is different than normal.
    '''
                    Predicted
                    F       T

            F       TN      FP
    Actual
            T       FN      TP

    '''
