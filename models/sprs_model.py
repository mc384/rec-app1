import pandas as pd
from surprise import Dataset
from surprise import Reader
from create_user_df import create_dataframe
from surprise import KNNWithMeans
from surprise.model_selection import GridSearchCV
from surprise import PredictionImpossible
import heapq

movielens = Dataset.load_builtin('ml-100k')
raw_ratings = movielens.raw_ratings
print(raw_ratings[:10])

df = create_dataframe() # 7,813,788 rows
# User id to string
df['user_id'] = df['user_id'].astype(str)
#print(df.shape)
#print(df.head(10))
df_filtered = df[df['rating'] != -1]
# How many rows can be included before running out of memory?
df_first_100000 = df_filtered.tail(100000)

reader = Reader(rating_scale=(1, 10))
data = Dataset.load_from_df(df_first_100000[["user_id", "anime_id", "rating"]], reader)

# User based cosine similarity
sim_options = {
    "name": "cosine",
    "user_based": True,  # Compute  similarities between users
}
algo = KNNWithMeans(min_k=10, sim_options=sim_options) # Keep min_k higher than 1, this has a big (positive) effect on recommendations

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

# predicted_scores.sort()
sorted_dict = {k: v for k, v in sorted(predicted_scores.items(), key=lambda item: item[1])}
print(sorted_dict) # ought to be selective about who gets a prediction, and about the # of members for a show (more = better generally)

# Get the ids of the 10 highest predicted scores
rec_id = heapq.nlargest(10, sorted_dict, key=sorted_dict.get)
print(rec_id)

rec_names = animes[animes['anime_id'].isin(rec_id)]

# Extract the names
names = rec_names['name'].tolist()

print(names)