import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

#Function that calculate the Root Mean Squared Logarithmic Error (RMSLE)
def score(test_soln, predictions):
    log_diff = np.log(predictions+1) - np.log(test_soln+1)
    return np.sqrt(np.mean(log_diff**2))

if __name__ == '__main__':

    #Imports train and test data
    df = pd.read_csv('train.csv')
    df2 = pd.read_csv('test.csv')

    #Converts saledate to year
    df['sale_year'] = pd.to_datetime(df['saledate']).apply(lambda x: x.year)
    df2['sale_year'] = pd.to_datetime(df2['saledate']).apply(lambda x: x.year)

    #Use RandomForestRegressor model on the train data.
    #The columns 'ModelID', 'YearMade', 'sale_year' were the most important
    #after we played with the data
    rfc = RandomForestRegressor(n_estimators=128, max_features='log2')
    X = np.array(df[['ModelID', 'YearMade', 'sale_year']])
    y = np.array(df['SalePrice'])
    rfc.fit(X,y)

    #Use the model to predict the Sale Price of the test data
    #The predictions have to be reshaped to matrix of ( _ , 1)
    pred = rfc.predict(df2[['ModelID', 'YearMade', 'sale_year']])
    pred2 = pred.reshape(11573,1)

    #Make numpy array reshaped to matrix of ( _ , 1) with SalesID and the
    #predicted Sales Price to export to csv file
    sales = np.array(df2['SalesID'])
    sales = sales.reshape(11573,1)
    answer = np.concatenate((sales, pred2), axis=1)
    np.savetxt('results.csv', answer, delimiter=',')
    #CSV does not have column names when it gets created,
    #first is SalesID, second is SalePrice


    #Import solutions to calculate RMSLE of predictions and print RMSLE
    test_solution = pd.read_csv('test_soln.csv')
    test_solution.set_index('SalesID')
    print score(test_solution.SalePrice, pred)
