import pickle
import streamlit as st
import requests
import time

API_KEY = "8265bd1679663a7ea12ac168da84d2e8"


def fetch_poster(movie_id, movie_title, retries=3):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    for attempt in range(retries):
        try:
            print(f"Requesting URL: {url}")
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            if data.get("poster_path"):
                return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
        except Exception as e:
            print(f"Error fetching data for movie: {movie_title}, attempt {attempt + 1}, Error: {e}")
            time.sleep(1)  # wait before retry

    # Fallback: search by title
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
    try:
        print(f"Fallback search: {movie_title}")
        search_response = requests.get(search_url, timeout=5)
        search_response.raise_for_status()
        results = search_response.json().get("results")
        if results and results[0].get("poster_path"):
            return f"https://image.tmdb.org/t/p/w500{results[0]['poster_path']}"
    except Exception as e:
        print(f"Fallback search failed for: {movie_title}, Error: {e}")

    # Final fallback placeholder
    return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        movie_title = movies.iloc[i[0]].title
        poster_url = fetch_poster(movie_id, movie_title)
        recommended_movie_posters.append(poster_url)
        recommended_movie_names.append(movie_title)

    return recommended_movie_names, recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)  # Updated here
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
