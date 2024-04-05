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

# Data handling dependencies
import pandas as pd
import numpy as np
import os

# Custom Libraries
from utils.data_loader import load_movie_titles
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model

# Data Loading
title_list = load_movie_titles('resources/data/movies.csv')

def display_team_member(image_path, name, title, description):
    st.image(image_path, width=150, caption=name, use_column_width='auto', output_format='PNG')
    st.markdown(f"**{title}**")
    st.write(description)
    st.write("")

# App declaration
def main():

    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ["Recommender System","Solution Overview"]

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    page_selection = st.sidebar.selectbox("Choose Option", page_options)
    if page_selection == "Recommender System":
        # Header contents
        st.write('# Movie Recommender Engine')
        st.write('### EXPLORE Data Science Academy Unsupervised Predict')
        st.image('resources/imgs/Image_header.png',use_column_width=True)
        # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('Fisrt Option',title_list[14930:15200])
        movie_2 = st.selectbox('Second Option',title_list[25055:25255])
        movie_3 = st.selectbox('Third Option',title_list[21100:21200])
        fav_movies = [movie_1,movie_2,movie_3]

        # Perform top-10 movie recommendation generation
        if sys == 'Content Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


        if sys == 'Collaborative Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = collab_model(movie_list=fav_movies,
                                                           top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    if page_selection == "Solution Overview":
        st.title("Solution Overview")
        st.write("Describe your winning approach on this page")

    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.
        
        
    if page_selection == "About Us":

        st.title('Welcome to InfoSmart')

        st.subheader('About Us')
        
        
        company_description = """
    At InfoSmart, we're on a mission to revolutionize the way you discover and enjoy movies. Founded on the principles of innovation and personalization, we're dedicated to providing you with an unparalleled cinematic experience tailored to your unique tastes.

    Driven by a team of passionate experts in collaborative and content-based filtering methods, we leverage cutting-edge algorithms to predict your preferences with unmatched accuracy. Whether you're a cinephile searching for hidden gems or a casual moviegoer in need of recommendations, InfoSmart is here to elevate your movie-watching journey.

    
    """
        st.markdown(company_description)



        


        # Team members data
    team_members = [
        {
            "name": "Kamogelo",
            "image_path": "resources/imgs/kamo.jpg",
            "title": "Machine Learning Engineer",
            "description": "Kamogelo specializes in developing machine learning algorithms for InfoSmart's recommendation system."
        },
        {
            "name": "Sibusiso",
            "image_path": "resources/imgs/sbu.jpg",
            "title": "Data Scientist",
            "description": "Sibusiso analyzes data and creates insights to improve the performance of InfoSmart's recommendation system."
        },
        {
            "name": "Onneile",
            "image_path": "resources/imgs/onneile.jpg",
            "title": "Software Engineer",
            "description": "Onneile is responsible for developing and maintaining the software infrastructure of InfoSmart's recommendation system."
        },
        {
            "name": "Felicia",
            "image_path": "resources/imgs/felicia.jpg",
            "title": "UI/UX Designer",
            "description": "Felicia designs intuitive and visually appealing user interfaces for InfoSmart's recommendation system."
        },
        {
            "name": "Anele",
            "image_path": "resources/imgs/anele.jpg",
            "title": "Product Manager",
            "description": "Anele oversees the development and implementation of new features for InfoSmart's recommendation system."
        },
        {
            "name": "Amukelani",
            "image_path": "resources/imgs/amukelani.jpg",
            "title": "Quality Assurance Engineer",
            "description": "Amukelani ensures the quality and reliability of InfoSmart's recommendation system through rigorous testing."
        }
    ]

    # Display team members
    for member in team_members:
        image_path = os.path.join(os.getcwd(), member["image_path"])
        display_team_member(image_path, member["name"], member["title"], member["description"])



        
                   
        
                      
                      


if __name__ == '__main__':
    main()
