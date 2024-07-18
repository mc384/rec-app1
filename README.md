The purpose of this project is to provide recommendations for users based on completed stats.
The current build intends to use the MAL API to get user information. The MAL API is supposedly rate limited to around 5 requests for some time period (per minute?). <br />
This document provides an overview of the API: https://myanimelist.net/apiconfig/references/api/v2 <br />
Getting started with the API (from forum post): https://myanimelist.net/forum/?topicid=1973141 <br />
This thread has very useful information about getting user information: https://myanimelist.net/forum/?topicid=1973077 <br />
The first step is to create a Client ID. The OAuth step can be skipped when accessing only public information. <br />
If generating access tokens is needed, details can be found here: https://gitlab.com/-/snippets/2039434 <br />
An important detail: the ID for an anime can be found in the URL. For example, the id for https://myanimelist.net/anime/10357Jinrui_wa_Suitai_Shimashita is 10357.

Files: <br />
get_user.py - For the inputted user information, fetches their anime list as a JSON structure. <br />
json_to_df.py - Converts JSON structure to tabular form. <br />
model.py - Configures and trains a ranking and retrieving model using tensorflow_recommenders. <br />
anime.csv - Database of animes with their ID. <br />
rating.csv - Contains user ratings. 

Resources used: <br />
Anime recommendations database - https://www.kaggle.com/datasets/CooperUnion/anime-recommendations-database?select=rating.csv <br />

Additional resources: <br />
Intro to collaborative filtering - https://realpython.com/build-recommendation-engine-collaborative-filtering/ <br />
Note that scikit-surprise requires Microsoft C++ Build Tools - https://visualstudio.microsoft.com/visual-cpp-build-tools/ <br />
Streamlit - https://docs.streamlit.io/get-started# 