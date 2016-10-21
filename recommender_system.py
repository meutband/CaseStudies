import graphlab as gl
import pandas as pd

if __name__ == '__main__':

    #Import Data
    df = pd.read_table('ratings.dat')

    #Remove users that have rated less than 10 jokes.
    df2 = df.groupby('user_id').count().sort_values(by='joke_id')
    df2 = df2[df2.joke_id <= 10]
    users = list(df2.index.values)
    for user in users:
        df = df[df.user_id != user]

    #Build Recommender System
    sf = gl.SFrame(df)
    rec = gl.recommender.factorization_recommender.create(
            sf,
            user_id='user_id',
            item_id='joke_id',
            target='rating',
            solver='auto',
            side_data_factorization=False,
            num_factors=4
            )

    #Store test_ratings as predictions for sample_submissions as csv
    sample_sub = pd.read_csv("sample_submission.csv")
    for_prediction = gl.SFrame(sample_sub)
    sample_sub.rating = rec.predict(for_prediction)
    output_fname = "test_ratings.csv"
    sample_sub.to_csv(output_fname, index=False)
        
