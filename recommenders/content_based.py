"""

    Content-based filtering for item recommendation.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: You are required to extend this baseline algorithm to enable more
    efficient and accurate computation of recommendations.

    !! You must not change the name and signature (arguments) of the
    prediction function, `content_model` !!

    You must however change its contents (i.e. add your own content-based
    filtering algorithm), as well as altering/adding any other functions
    as part of your improvement.

    ---------------------------------------------------------------------

    Description: Provided within this file is a baseline content-based
    filtering algorithm for rating predictions on Movie data.

"""

import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# Importing data
movies = pd.read_csv('resources/data/movies.csv', sep=',')
ratings = pd.read_csv('resources/data/ratings.csv')
movies.dropna(inplace=True)

def data_preprocessing(subset_size=None):
    """Prepare data for use within Content filtering algorithm.
    
    Parameters
    ----------
    subset_size : int, optional
        Number of movies to use within the algorithm. If None, all movies are used.
        
    Returns
    -------
    Pandas DataFrame
        Subset of movies selected for content-based filtering.
    """
    # Split genre data into individual words.
    movies['keyWords'] = movies['genres'].str.replace('|', ' ')
    # Subset of the data
    if subset_size:
        movies_subset = movies[:subset_size]
    else:
        movies_subset = movies
    return movies_subset

def content_model(movie_list, top_n=10):
    """Performs Content filtering based upon a list of movies supplied by the app user.
    
    Parameters
    ----------
    movie_list : list of str
        List of movie titles.
    top_n : int, optional
        Number of recommended movies to return.
        
    Returns
    -------
    list of str
        Titles of recommended movies.
    """
    # Initializing the empty list of recommended movies
    data = data_preprocessing()
    # Instantiating and generating the count matrix
    count_vec = CountVectorizer()
    count_matrix = count_vec.fit_transform(data['keyWords'])
    indices = pd.Series(data.index, index=data['title'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    cosine_sim = pd.DataFrame(cosine_sim, index=data.index, columns=data.index)
    # Getting the index of the movie that matches the title
    movie_indexes = [indices[movie] for movie in movie_list if movie in indices]
    if len(movie_indexes) != len(movie_list):
        raise ValueError("Some movies are not found in the dataset.")
    # Creating a Series with the similarity scores in descending order
    rank = [cosine_sim[idx] for idx in movie_indexes]
    score_series = [pd.Series(r).sort_values(ascending=False) for r in rank]
    # Concatenating the similarity scores
    listings = pd.concat(score_series).sort_values(ascending=False)
    # Store movie names
    recommended_movies = []
    # Appending the names of movies
    top_50_indexes = list(listings.iloc[1:50].index)
    # Removing chosen movies
    top_indexes = np.setdiff1d(top_50_indexes, movie_indexes)
    for i in top_indexes[:top_n]:
        recommended_movies.append(data.loc[i, 'title'])
    return recommended_movies

# Example usage
movie_list = ['The Dark Knight', 'Inception', 'The Matrix']
recommended_movies = content_model(movie_list)
print("Recommended Movies:", recommended_movies)
