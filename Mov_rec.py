import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    data = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=bfdda845c2635c7a7fb7f3e642762d10&language=en-US'.format(movie_id))
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    
    return full_path
    
similarity_mat = pickle.load(open('siml.pkl','rb'))    
movies = pickle.load(open('movies.pkl', 'rb'))

movies_list = movies['title'].values
st.title('Movie Recommender System')
selected_movie = st.selectbox('Search for movies',
                      movies_list)

def recommend(movie):
    recommended_movies =[]
    recommended_posters = []
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity_mat[movie_index]
    rec_movies = sorted(list(enumerate(distances)),reverse = True, key = lambda x:x[1])[1:6]

    for i in rec_movies:
        mov_id = movies.iloc[i[0]].id
        recommended_movies.append((movies.iloc[i[0]].title))  
        recommended_posters.append(fetch_poster(mov_id)) 
    return recommended_movies, recommended_posters

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommendations[0])
        st.image(posters[0])

    with col2:
        st.text(recommendations[1])
        st.image(posters[1])

    with col3:
        st.text(recommendations[2])
        st.image(posters[2])

    with col4:
        st.text(recommendations[3])
        st.image(posters[3])

    with col5:
        st.text(recommendations[4])
        st.image(posters[4])
