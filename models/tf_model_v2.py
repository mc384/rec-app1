import pandas as pd
import sys
import re
import tensorflow as tf
import tensorflow_recommenders as tfrs
import numpy as np
from typing import Dict, Text
from create_user_df import create_dataframe # this will not work if the file directories are not correct

animes = pd.read_csv('anime.csv')

# Convert id to type str
animes['anime_id'] = animes['anime_id'].astype(str)

unique_episodes = animes['episodes'].unique()

# Allow changes to be made to copy of df
pd.options.mode.chained_assignment = None

mean_episodes = animes[animes['episodes'] != 'Unknown']
mean_episodes['episodes'] = mean_episodes['episodes'].astype('float64')
mean_ep_count = mean_episodes['episodes'].mean()

animes = animes.replace('Unknown', '12.38')
unique_episodes = animes['episodes'].unique()

# Convert episodes to type float
animes['episodes'] = animes['episodes'].astype('float64')

# Replace missing ratings with mean value
animes['rating'].fillna((animes['rating'].mean()), inplace=True)

# Label missing genres and types as 'Unknown'
animes['genre'].fillna('Unknown', inplace=True)
animes['type'].fillna('Unknown', inplace=True)

# Cleaning special characters from strings
animes['name'] = animes['name'].str.replace(r'&#', '')
animes['name'] = animes['name'].str.replace(r';', '')
animes['name'] = animes['name'].apply(lambda x: re.sub(r'[^\x00-\x7F]+', '', x))
animes['name'] = animes['name'].str.replace('"', '') # remove quotations
animes['name'] = animes['name'].str.replace('&quot', '') # remove &quot
animes.head(20)

#ratings = pd.read_csv('rating.csv')
# NEW: Integrate user into the database
ratings = create_dataframe()
print(ratings)

# Replace -1 ratings with 0
ratings = ratings.replace(-1, 0)

# Rename column to avoid ambiguity
ratings.rename(columns={'rating': 'user_score'}, inplace=True)

# Convert id to type str
ratings['user_id'] = ratings['user_id'].astype(str)

# Join the ratings with anime df
ratings['anime_id'] = ratings['anime_id'].astype(str)
combined = ratings.merge(animes, left_on='anime_id', right_on = 'anime_id')

# Select columns
combined = combined[['user_id', 'name']]

# Unique fields
anime_ids = animes['anime_id'].unique().astype(str)
names = animes['name'].unique().astype(str)
genres = animes['genre'].unique().astype(str)
types = animes['type'].unique().astype(str)
episode_count = animes['episodes'].unique().astype(float)
ratings = animes['rating'].unique().astype(float)
member_count = animes['members'].unique().astype(float)

anime_dict = tf.data.Dataset.from_tensor_slices(dict(animes))
anime_dict = anime_dict.map(lambda x: x["name"])

  # Create tensorflow dataset for ratings. Keep the user id and anime name fields.
user_ratings = tf.data.Dataset.from_tensor_slices(dict(combined))
user_ratings  = user_ratings.map(lambda x: {
    "name": x["name"],
    "user_id": x["user_id"],
})

  # Train test split
tf.random.set_seed(42)
shuffled = user_ratings.shuffle(100_000, seed=42, reshuffle_each_iteration=False)

train = shuffled.take(80_000)
test = shuffled.skip(80_000).take(20_000)

anime_titles = anime_dict.batch(1_000)
user_ids = user_ratings.batch(1_000_000).map(lambda x: x["user_id"])

unique_anime_titles = np.unique(np.concatenate(list(anime_titles)))
unique_user_ids = np.unique(np.concatenate(list(user_ids)))

unique_anime_titles[:10]

embedding_dimension = 32

user_model = tf.keras.Sequential([
  tf.keras.layers.StringLookup(
      vocabulary=unique_user_ids, mask_token=None),
  # We add an additional embedding to account for unknown tokens.
  tf.keras.layers.Embedding(len(unique_user_ids) + 1, embedding_dimension)
])

anime_model = tf.keras.Sequential([
  tf.keras.layers.StringLookup(
      vocabulary=unique_anime_titles, mask_token=None),
  tf.keras.layers.Embedding(len(unique_anime_titles) + 1, embedding_dimension)
])

metrics = tfrs.metrics.FactorizedTopK(
  candidates=anime_dict.batch(128).map(anime_model)
)

task = tfrs.tasks.Retrieval(
  metrics=metrics
)

# Model boilerplate
class AnimeModel(tfrs.Model):

  def __init__(self, user_model, anime_model):
    super().__init__()
    self.anime_model: tf.keras.Model = anime_model
    self.user_model: tf.keras.Model = user_model
    self.task: tf.keras.layers.Layer = task

  def compute_loss(self, features: Dict[Text, tf.Tensor], training=False) -> tf.Tensor:
    # We pick out the user features and pass them into the user model.
    user_embeddings = self.user_model(features["user_id"])
    # And pick out the movie features and pass them into the movie model,
    # getting embeddings back.
    positive_anime_embeddings = self.anime_model(features["name"])

    # The task computes the loss and the metrics.
    return self.task(user_embeddings, positive_anime_embeddings)

model = AnimeModel(user_model, anime_model)
model.compile(optimizer=tf.keras.optimizers.Adagrad(learning_rate=0.1))

cached_train = train.shuffle(100_000).batch(8192).cache()
cached_test = test.batch(4096).cache()

model.fit(cached_train, epochs=3)

model.evaluate(cached_test, return_dict=True)

# Create a model that takes in raw query features, and
index = tfrs.layers.factorized_top_k.BruteForce(model.user_model)
# recommends animes out of the entire movies dataset.
index.index_from_dataset(
  tf.data.Dataset.zip((anime_dict.batch(100), anime_dict.batch(100).map(model.anime_model)))
)

# Get recommendations
_, titles = index(tf.constant(["73517"]))
print(f"Recommendations for user 73517: {titles[0, :3]}")
# Ex. Recommendations for user 73517: [b'Shuffle! Memories' b'_Summer' b'Girls Bravo: First Season']
# These recommendations are just not very good