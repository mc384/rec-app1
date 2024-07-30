import streamlit as st
from app.get_user import create_dataframe
from models.sprs_model_prod import pred_shows 

# Set the title
st.title('Questionable Suggestions')

# Create two columns
col1, col2 = st.columns([1, 2])

with col1:
    # Aesthetic image
    st.image('girl-adventurer-anime-character-1714887648fkR.jpg')

with col2:
    # Input box for username
    username = st.text_input('Please input username:')
    # Header for recommendations
    st.subheader('Recommendations')
    st.write('Based on your list, we\'ll look for shows that best fit you.')
    # Check that we are getting the dataframe
    if username:
        # Get user list
        df = create_dataframe(username)
        # Get recommendations
        with st.spinner("Loading"):
            anime_rec = pred_shows(df)
            st.write('We think you\'d like these shows:')
        for i in range(10):
            st.write(anime_rec[i])

# Run the Streamlit app
# Use the command `streamlit run app.py` in your terminal to start the app
