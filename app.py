import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = (f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=215c2c2fdb8b541db53e82b0d149e09e")
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjZDgwMmMxNTY5Mzc3ZWU2MzhiNjIzODEzNTcwNjMyOCIsIm5iZiI6MTcyODgzNDM5My45NDkyOTksInN1YiI6IjY3MGJlYWEyYmJiMWE5ZTgxYzYyMWI2MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ"
    }

    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        fetch_poster(movie_id)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie recommender system')

selected_movie_name = st.selectbox(
    'Select a movie',
    movies['title'].values
)

if st.button('Recommend'):
    recommendations, recommended_movies_poster = recommend(selected_movie_name)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(recommendations[i])
            st.image(recommended_movies_poster[i])
