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
import os

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
    time.sleep(6) 

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
add_bg_from_local('resources/imgs/back.jpg')  

def main():
    selected = option_menu(
        menu_title=None,  # required
        options=["Recom-Engine","Solution Overview","About Us"],  # required
        icons=["bag-heart","easel","stack"],  
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
                    movie_id = movie_df.loc[movie_df['title'] == movie_name, 'tmdbId'].values[0]
                    poster_url = fetch_poster(movie_id)
                    st.image(poster_url, width=150)

                    # Display trailer link
                    ##if trailer_url != "No trailer found.":
                       #st.markdown(f"Trailer URL: [{movie_name} Trailer]({trailer_url})")
                    #else:
                     #  st.write("Trailer not available.")
                    

            except:
                st.error("Oops! Looks like this algorithm doesn't work. We'll need to fix it!")


                    
    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    if selected == "Solution Overview":
        # You may want to add more sections here for aspects such as an EDA,
        # or to provide your business pitch.
        st.title("Recommender System Used")
        
        rating_image = "resources/imgs/ratings2.jpg"
        st.image(rating_image, caption='Stars', use_column_width=True)


        st.write('• Collaborative Filtering: Think of collaborative filtering as a method that taps into the collective wisdom of users. It works by analyzing the preferences and behaviors of many users to make recommendations. Essentially, it looks at patterns in how users interact with movies and finds similarities between users who liked similar movies in the past. Then, it suggests movies that similar users enjoyed but haven’t been watched by the current user yet. It’s like when your friends recommend movies to you because they know your tastes and what you’ve enjoyed in the past. Collaborative filtering is great for discovering new movies based on what other users with similar tastes have enjoyed.')
        st.write('• Content-Based Filtering: Content-based filtering, on the other hand, focuses on the characteristics of the movies themselves. It looks at the attributes of each movie, such as genre, actors, director, plot keywords, and more. Then, it matches these attributes with the user’s preferences. For example, if a user has previously enjoyed action movies starring a specific actor, the content-based filtering system will recommend similar action movies featuring that actor. Its like having a personal movie critic who knows your favorite genres, actors, and themes and suggests movies that fit your tastes based on those preferences.')
        st.markdown(f'''<div style="color:black; font-size:80px;"><p>• <strong>Content-Based Filtering:</strong> Content-based filtering, on the other hand, focuses on the characteristics of the movies themselves. It looks at the attributes of each movie, such as genre, actors, director, plot keywords, and more. Then, it matches these attributes with the user’s preferences. For example, if a user has previously enjoyed action movies starring a specific actor, the content-based filtering system will recommend similar action movies featuring that actor. It's like having a personal movie critic who knows your favorite genres, actors, and themes and suggests movies that fit your tastes based on those preferences.</p></div>''', unsafe_allow_html=True)

        st.title('Resources')
        data_image = "resources/imgs/overview.jpg"
        st.image(data_image, caption='Data', use_column_width=True)
        st.subheader('MovieLens')
        st.write('Imagine a vast collection of movie ratings, each adorned with five stars by fellow movie enthusiasts just like you. That\'s precisely what our MovieLens dataset offers—a rich tapestry of cinematic opinions that powers our recommendation system within our App, CineSage. Enhanced with additional data and meticulously resampled for fairness, this dataset serves as the cornerstone of our quest to provide you with the most accurate and personalized movie recommendations possible. So, rest assured, your movie journey with CineSage is backed by the collective wisdom of millions of fellow movie lovers.')

        st.subheader('Datasets')
        st.write('These are the datasets used to build the recommender system:')
        
        data_description= """ 
        The file named "movies.csv" contains information about various movies. Each line within the file represents a single movie.
        Let's break down what each part of the file means:
        
        ♦ movieId: This is a unique identifier for each movie. It helps to distinguish one movie from another. For example, if there are multiple movies with the same title, each will have a different movieId.

        ♦ title: This is the name of the movie. You might see something like "The Lion King (1994)" which tells you the title of the movie and the year it was released in parentheses. Sometimes, there might be errors or inconsistencies in the titles.

        ♦ genres: This part tells you what kind of movie it is. It could be Action, Comedy, Drama, or a mix of different genres. Genres are separated by a vertical bar (|). For example, a movie might be tagged as "Action|Adventure|Sci-Fi", which means it's an action movie with elements of adventure and science fiction.

        Now, let's imagine you want to know about a specific movie. You can look it up in this file using its movieId or title, and you'll find information about what genre it belongs to and when it was released.

        So, in simpler terms, this file is like a big catalog of movies. It tells you their names, unique identifiers, what type of movies they are (like action, comedy, etc.), and sometimes when they were released. It's a handy reference for anyone who loves movies and wants to explore different genres.ovieId: This is a unique identifier for each movie. It helps to distinguish one movie from another. For example, if there are multiple movies with the same title, each will have a different movieId.
        """
        
        st.markdown(data_description)
        
        st.write('Imagine you have another file called "train.csv". This file contains information about how users have rated movies. Each line in the file represents one rating given by a user to a movie. Here\'s what each part of the file means:')

        st.write('➢ userId: This is a unique identifier for each user who has rated movies. It helps to distinguish one user from another. For example, if there are multiple users, each will have a different userId.')

        st.write('➢ movieId: This is the unique identifier for each movie that has been rated. It helps to identify which movie the user has rated.')

        st.write('➢ rating: This is the score that the user has given to the movie. Ratings are made on a scale of 0.5 stars to 5 stars, with increments of 0.5 stars. For example, a user might give a movie 4 stars or 3.5 stars.')

        st.write('➢ timestamp: This represents when the rating was made. It’s recorded in seconds since midnight Coordinated Universal Time (UTC) of January 1, 1970. This might not be relevant for every user, but it helps to track when the rating was given.')

        st.write('So, in simpler terms, this file is like a log of how users have rated different movies. It tells you who rated the movie, which movie they rated, what score they gave it, and when they rated it. This information can be used to analyze user preferences, recommend movies, or understand which movies are popular among users.')

    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.

    if selected == "About Us":

        st.title('Welcome to InfoSmart')

        st.subheader('About Us')

        company_description = """
        **At InfoSmart, we're on a mission to revolutionize the way you discover and enjoy movies. Founded on the principles of innovation and personalization, we're dedicated to providing you with an unparalleled cinematic experience tailored to your unique tastes.**

        **Driven by a team of passionate experts in collaborative and content-based filtering methods, we leverage cutting-edge algorithms to predict your preferences with unmatched accuracy. Whether you're a cinephile searching for hidden gems or a casual moviegoer in need of recommendations, InfoSmart is here to elevate your movie-watching journey.**
        """
        st.markdown(company_description)

            
        # Team members data
        team_members = [
            {
                "image_path": "resources/imgs/kamo.jpg",
                "name": "Kamogelo",
                "title": "Machine Learning Engineer",
                "description": "Kamogelo specializes in developing machine learning algorithms for InfoSmart's recommendation system."
            },
            {
                "image_path": "resources/imgs/sbu.jpg",
                "name": "Sibusiso",
                "title": "Data Scientist",
                "description": "Sibusiso analyzes data and creates insights to improve the performance of InfoSmart's recommendation system."
            },
            {
                "image_path": "resources/imgs/onneile.jpg",
                "name": "Onneile",
                "title": "Software Engineer",
                "description": "Onneile is responsible for developing and maintaining the software infrastructure of InfoSmart's recommendation system."
            },
            {
                "image_path": "resources/imgs/felicia.jpg",
                "name": "Felicia",
                "title": "UI/UX Designer",
                "description": "Felicia designs intuitive and visually appealing user interfaces for InfoSmart's recommendation system."
            },
            {
                "image_path": "resources/imgs/anele.jpg",
                "name": "Anele",
                "title": "Product Manager",
                "description": "Anele oversees the development and implementation of new features for InfoSmart's recommendation system."
            },
            {
                "image_path": "resources/imgs/amukelani.jpg",
                "name": "Amukelani",
                "title": "Quality Assurance Engineer",
                "description": "Amukelani ensures the quality and reliability of InfoSmart's recommendation system through rigorous testing."
            }
        ]

        # Display team members
        for member in team_members:
            image_path = os.path.join(os.getcwd(), member["image_path"])
            st.image(image_path, use_column_width=True, output_format='JPEG', width=200, clamp=True)
            st.markdown(f"**{member['name']}**")
            st.markdown(f"**{member['title']}**")
            st.markdown(member['description'])

        
        #using this code to allow users to leave a message 
        st.title("Leave a Message")

        name = st.text_input("Name")
        number = st.text_input("Number")
        email = st.text_input("Email")
        message = st.text_area("Message")

        if st.button("Send Message"):
            if name and number and email and message:
                # Here you can add your logic to send the message
                st.success("Message sent successfully!")
            else:
                st.error("Please fill in all the fields.")

if __name__ == '__main__':
    main()
