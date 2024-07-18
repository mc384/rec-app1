The purpose of this project is to provide recommendations for users based on completed stats. The current build intends to use the MAL API to get user information.
This document provides an overview of the API: https://myanimelist.net/apiconfig/references/api/v2 <br />
Getting started with the API (from forum post): https://myanimelist.net/forum/?topicid=1973141 <br />
This thread has very useful information about getting user information: https://myanimelist.net/forum/?topicid=1973077 <br />
The first step is to create a Client ID. The OAuth step can be skipped when accessing only public information. <br />
If generating access tokens is needed, details can be found here: https://gitlab.com/-/snippets/2039434 <br />
The ID for an anime can be found in the URL. For example, the id for https://myanimelist.net/anime/10357Jinrui_wa_Suitai_Shimashita is 10357.

Files: <br />
app.py - Streamlit app
get_user.py - For the inputted user information, fetches their anime list as a JSON structure. <br />
sprs_model_prod.py - KNN model <br />
anime.csv - Database of animes with their ID. <br />
rating.csv - Contains user ratings. 

Resources used: <br />
Anime recommendations database - https://www.kaggle.com/datasets/CooperUnion/anime-recommendations-database?select=rating.csv <br />

Additional resources: <br />
Intro to collaborative filtering - https://realpython.com/build-recommendation-engine-collaborative-filtering/ <br />
Streamlit - https://docs.streamlit.io/get-started# 