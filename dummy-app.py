import streamlit as st
import pandas as pd
from app.get_user import create_dataframe
from models.sprs_model_prod import pred_shows 

# Get client ID
CLIENT_ID = st.secrets["CLIENT_ID"]

# Can this load without crashing?
ratings = pd.read_csv('rating.csv')

# Set the title
st.title('Questionable Suggestions')

# Create two columns
col1, col2 = st.columns([1, 2])

with col1:
    # Display a generic portrait-sized image
    st.image('girl-adventurer-anime-character-1714887648fkR.jpg')

with col2:
    # Input box for username
    username = st.text_input('Please input username:')
    # Header for recommendations
    st.header('Recommendations')
    # Placeholder for recommendations content
    st.write('Recommendations will appear here.')
    # Check that we are getting the dataframe
    if username:
        st.write("Hello")

# Run the Streamlit app
# Use the command `streamlit run app.py` in your terminal to start the app