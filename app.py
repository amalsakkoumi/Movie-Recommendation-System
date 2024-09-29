import streamlit as st
import pickle
import requests

# Set Streamlit to wide mode for maximum content width
st.set_page_config(layout="wide")
# Movie Recommendation System title centered
st.markdown("<h1 style='text-align: center;'>MOVIE RECOMMENDATION SYSTEM</h1>", unsafe_allow_html=True)

# Custom CSS for styling
css_style = """
<style>
    .sample-header {
        height: 45vh;
        background-image: url("https://www.notebookcheck.net/fileadmin/Notebooks/News/_nc3/netflixteaser.png");
        background-size: cover;
        background-position: center;
        color: white;
        text-align: center;
    }
    h1 {
        font-weight: 700;
        color: #9a031e;
    }
</style>
"""

# HTML content for the header
html_code = """
<div class="sample-header"></div>
"""

# Render the CSS and HTML for the custom header
st.markdown(css_style, unsafe_allow_html=True)
st.markdown(html_code, unsafe_allow_html=True)



# Function to fetch movie poster from The Movie Database API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Load movie data and similarity model
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))

# Get list of movie titles for the dropdown
movies_list = movies['title'].values

# Dropdown menu for movie selection
selectvalue = st.selectbox("Select movie from dropdown", movies_list)

# Function to recommend movies based on similarity
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:11]:
        movie_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
    return recommend_movie, recommend_poster

# Show recommendations when button is clicked
if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(selectvalue)
    
    # Display recommended movies in a 5x2 grid
    cols = st.columns(5)  # First row of 5 columns
    for i in range(5):
        with cols[i]:
            st.text(movie_name[i])
            st.image(movie_poster[i])

    cols = st.columns(5)  # Second row of 5 columns
    for i in range(5, 10):
        with cols[i-5]:
            st.text(movie_name[i])
            st.image(movie_poster[i])
