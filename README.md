The purpose of this project is to provide recommendations for users based on completed stats. The current build intends to use the MAL API to get user information.
This document provides an overview of the API: https://myanimelist.net/apiconfig/references/api/v2 <br />
This thread has very useful information about getting user information: https://myanimelist.net/forum/?topicid=1973077 <br />
The ID for an anime can be found in the URL. For example, the id for https://myanimelist.net/anime/10357Jinrui_wa_Suitai_Shimashita is 10357.

Files: <br />
app.py - Streamlit app
get_user.py - For the inputted user information, fetches their anime list as a JSON structure. <br />
sprs_model_prod.py - KNN model <br />
anime.csv - Database of animes with their ID. <br />
rating.csv - Contains user ratings. 

Resources used: <br />
Anime recommendations database - https://www.kaggle.com/datasets/CooperUnion/anime-recommendations-database?select=rating.csv <br />

On streamlit <br />
Requirements can be found in the requirements.txt file. Due to memory restrictions on streamlit cloud, a only a subset of the data is used.