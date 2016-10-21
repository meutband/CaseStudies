import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score, precision_score, accuracy_score
from sklearn.metrics import confusion_matrix, mean_squared_error
import cPickle as pickle

if __name__ == '__main__':

    #Import data
    df = pd.read_json('data.json')

    #Clasify the event as fraud if the acct_type is 'fraudster', 'fraudster_att',
    #or 'fraudster_event'. Make new column of 'Fraud' in the dataframe
    fraud = ['fraudster', 'fraudster_att', 'fraudster_event']
    df['Fraud'] = -1
    df['Fraud'] = df['acct_type'].apply(lambda x: 1 if x in fraud else 0)

    #Makes a list of all columns in the dataframe that are not string types
    #(integer or floats)
    columns = df.columns.values
    cols = []
    for col in columns:
        if col != 'Fraud':
            if df[col].dtype != 'object':
                cols.append(col)

    #Makes X and y values where X is columns that are from the list above
    X = df.copy()[cols].fillna(0)
    y = df['Fraud']

    #Splits data into a training and test set, runs model.
    Xtrain, Xtest, ytrain, ytest = train_test_split(X,y, test_size = 0.3)
    rf = RandomForestClassifier(n_estimators=128, max_features=7)
    rf.fit(Xtrain, ytrain)

    #Predicts fraud in the test set
    ypred = rf.predict(Xtest)

    #Calculates and print Mean-Squared_Error, Accuracy_Score, Recall_Score,
    #Precision_Score, and prints a Confusion_Matrix
    print 'Mean-Squared = ', mse(ytest, ypred)
    print 'Accuracy = ',ac(ytest, ypred)
    print 'Recall = ', rs(ytest, ypred)
    print 'Precision = ', ps(ytest, ypred)

    print confusion_matrix(ytest, ypred)

    #sklearn.confusion_matrix is different than normal.
    '''
                        Predicted
                        F       T

                F       TN      FP
        Actual
                T       FN      TP
    '''

    #Exports the model into a pkl file
    with open("model.pkl", 'w') as f:
        pickle.dump(rf, f)
