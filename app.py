import streamlit as st
from app.get_user import create_dataframe
from models.sprs_model_prod import pred_shows 

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
    st.write('Based on your list, we think you\'d like these shows:')
    # Check that we are getting the dataframe
    if username:
        # Get user list
        df = create_dataframe(username)
        #dummy = df.iloc[0, 1]
        #st.write(str(dummy))
        # Get recommendations
        anime_rec = pred_shows(df) # looks like [0: "Sen to chihiro", 1: "kara no kyoukai", etc]
        for i in range(10):
            st.write(anime_rec[i])

# Run the Streamlit app
# Use the command `streamlit run app.py` in your terminal to start the app
