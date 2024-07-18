import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

# Load the client id
CLIENT_ID = os.getenv('CLIENT_ID')

def create_dataframe(user):
    urlLeft = 'https://api.myanimelist.net/v2/users/'
    urlRight = '/animelist?fields=list_status&status=completed&limit=999'

    url = urlLeft + user + urlRight

    response = requests.get(url, headers = {
    'X-MAL-CLIENT-ID': CLIENT_ID
    })

    response.raise_for_status()
    data = response.json()
    response.close()

    # JSON to pd
    df = pd.json_normalize(data['data'])

    # Keep id and score
    df = df[['node.id', 'list_status.score']]

    # Rename columns to 'anime_id' and 'rating'
    df = df.rename(columns={'node.id': 'anime_id', 'list_status.score': 'rating'})

    # Assign a user id
    df['user_id'] = 73517

    # Rearrange columns
    df = df[['user_id', 'anime_id', 'rating']]

    # Anime database
    anime_db = pd.read_csv('anime.csv')

    df3 = df[df['anime_id'].isin(anime_db['anime_id'])]

    ratings = pd.read_csv('rating.csv')
    df4 = pd.concat([ratings, df3])
    return df4