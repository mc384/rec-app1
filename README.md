The purpose of this project is to provide recommendations for users based on completed stats. The current build uses the MAL API to get user information.
This document provides an overview of the API: https://myanimelist.net/apiconfig/references/api/v2 <br />
Getting started with the API (from forum post): https://myanimelist.net/forum/?topicid=1973141 <br />
This thread explains how public user information is accessed: https://myanimelist.net/forum/?topicid=1973077 <br />

Files: <br />
app.py - Streamlit app
get_user.py - For the inputted user information, fetches their anime list as a JSON structure. <br />
sprs_model_prod.py - KNN model <br />
anime.csv - Database of animes with their ID. <br />
rating.csv - Contains user ratings. 

Resources used: <br />
Anime recommendations database - https://www.kaggle.com/datasets/CooperUnion/anime-recommendations-database?select=rating.csv <br />