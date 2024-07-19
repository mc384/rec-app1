import pandas as pd
from surprise import Dataset
from surprise import Reader
from surprise import KNNWithMeans
import heapq

def pred_shows(df):
    # Watched shows
    watched_shows = df[df['user_id'] == 73517]
    watched_shows = watched_shows['anime_id'].to_numpy()
    # User id to string
    df['user_id'] = df['user_id'].astype(str)
    #print(df.shape)
    #print(df.head(10))
    df_filtered = df[df['rating'] != -1]
    #df_first_100000 = df_filtered.tail(100000)
    #df1 = df_filtered.head(7000000)
    #df1 = df1.sample(n=49000)
    #df2 = df_filtered.tail(1000)
    df2 = df_filtered[df_filtered['id']== 73517]
    num_user = df2.shape[0]
    num_left = 1000 - num_user
    df1 = df_filtered.head(2000)
    df1 = df1.sample(n=num_left)
    df_first_50000 = pd.concat([df1, df2], axis=0)

    reader = Reader(rating_scale=(1, 10))
    data = Dataset.load_from_df(df_first_50000[["user_id", "anime_id", "rating"]], reader)

    # User based cosine similarity
    sim_options = {
        "name": "cosine",
        "user_based": True,  # Compute  similarities between users
    }
    algo = KNNWithMeans(min_k=10, sim_options=sim_options) # Keep min_k higher than 1, this has a significant effect on recommendations

    trainingSet = data.build_full_trainset()

    algo.fit(trainingSet)

    # Predictions
    animes = pd.read_csv('anime.csv')

    # Remove explicit genres
    animes = animes[~animes['genre'].isin(['Ecchi', 'Hentai'])]

    anime_id = animes['anime_id'].to_numpy()

    predicted_scores = {}

    for id in anime_id:
        pred = algo.predict('73517', id) # By default, if prediction is impossible, it returns the average of all ratings in the trainset
        predicted_scores[id] = pred.est

    for show in watched_shows:
        predicted_scores.pop(show)

    # predicted_scores.sort()
    sorted_dict = {k: v for k, v in sorted(predicted_scores.items(), key=lambda item: item[1])}
    print(sorted_dict) 

    # Get the ids of the 10 highest predicted scores
    rec_id = heapq.nlargest(10, sorted_dict, key=sorted_dict.get)
    print(rec_id)

    rec_names = animes[animes['anime_id'].isin(rec_id)]

    # Extract the names
    names = rec_names['name'].tolist()

    return names