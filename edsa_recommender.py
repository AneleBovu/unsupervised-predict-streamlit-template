"""

    Streamlit webserver-based Recommender Engine.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: !! Do not remove/modify the code delimited by dashes !!

    This application is intended to be partly marked in an automated manner.
    Altering delimited code may result in a mark of 0.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend certain aspects of this script
    and its dependencies as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st
from streamlit_option_menu import option_menu
import time

# Data handling dependencies
import pandas as pd
import requests
import base64

# Custom Libraries

from utils.data_loader import load_movie_titles
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model

#libraries
import googleapiclient.discovery

# Data Loading
df_links = pd.read_csv('resources/data/links.csv')
title_list = load_movie_titles('resources/data/movies.csv')
movies_df =  pd.read_csv('resources/data/movies.csv', index_col='movieId')
movies = movies_df.dropna()

#Loading page
with st.spinner('# CineSage Loading...'):
    # Simulate a long computation
    time.sleep(5) 

#trailer
def get_movie_trailer(movie_name):
    # Set up YouTube Data API client
    api_service_name = "youtube"
    api_version = "v3"
    api_key = "AIzaSyCxeFJnqlUpLw8vRA1jXLbq-a9FHhsOMi0"  # Replace with your own API key
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

    # Search for movie trailers
    request = youtube.search().list(
        q=movie_name + " trailer",
        part="snippet",
        maxResults=1,
        type="video"
    )
    response = request.execute()

    # Extract trailer video ID
    if 'items' in response:
        items = response['items']
        if items:
            trailer_id = items[0]['id']['videoId']
            trailer_url = f"https://www.youtube.com/watch?v={trailer_id}"
            return trailer_url
        else:
            return "No trailer found."
    else:
        return "Error fetching data."

#poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
    data=requests.get(url)
    data=data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path

#data
df_links.dropna(subset=['tmdbId'], inplace=True)
df_links['tmdbId'] = df_links['tmdbId'].astype(int)
movie_df = pd.merge(movies_df, df_links, on='movieId', how='inner')

#Get ID
def get_movie_id(movie_title):
    movie_id = movie_df.loc[movie_df['title'] == movie_title, 'tmdbId'].values
    if len(movie_id) > 0:
        return movie_id[0]
    else:
        return "Movie not found"

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"avif"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('resources/em.avif')  

def main():
    selected = option_menu(
        menu_title=None,  # required
        options=["Recom-Engine","Solution Overview"],  # required
        icons=["rewind-btn","easel"],  
        menu_icon="cast",  
        default_index=0, 
        orientation="horizontal",
    )
    
    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    
    if selected == "Recom-Engine":
        # Header contents
        st.image("resources/imgs/engine.jpg", width=700)
        
        columns = st.columns(len([299536, 429422, 240, 155, 572154]))
        for i, movie_id in enumerate([299536, 429422, 240, 155, 572154]):
            poster_url = fetch_poster(movie_id)
            columns[i].image(poster_url, width=150)
            # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('Fisrt Option',title_list[14930:15200])
        movie_2 = st.selectbox('Second Option',title_list[25055:25255])
        movie_3 = st.selectbox('Third Option',title_list[21100:21200])
        fav_movies = [ movie_1 , movie_2, movie_3]
        
        # Perform top-10 movie recommendation generation
        if st.button("Recommend"):
            try:
                with st.spinner('Crunching the numbers...'):
                    if sys == 'Content Based Filtering':
                        top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=10)
                    elif sys == 'Collaborative Based Filtering':
                        top_recommendations = collab_model(movie_list=fav_movies,
                                                           top_n=10)
                    
                # Display recommended movies with posters and trailer links
                st.title("We think you'll like:")
                for i, movie_name in enumerate(top_recommendations):
                    st.subheader(str(i+1) + '. ' + movie_name)
                    
                    # Display movie poster
                    #poster_url = fetch_poster(movie_df.loc[movie_df['title'] == movie_name, 'tmdbId'].values[0])
                    #st.image(poster_url, width=150)
                    
                    # Display trailer link
                    #trailer_url = get_movie_trailer(movie_name)
                    #if trailer_url != "No trailer found.":
                        #st.write(f"Trailer URL: [{movie_name} Trailer]({trailer_url})")
                    #else:
                    #    st.write("Trailer not available.")
            
            except:
                st.error("Oops! Looks like this algorithm doesn't work. We'll need to fix it!")
                    
    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    if selected == "Solution Overview":
        st.title("Solution Overview")
        st.write("Describe your winning approach on this page")

    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.


if __name__ == '__main__':
    main()
