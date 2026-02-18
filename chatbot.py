import pandas as pd
import urllib.parse

# Load dataset
movies = pd.read_csv("TeluguMovies_dataset.csv")
movies.columns = movies.columns.str.strip()

# Generate YouTube search link
def generate_link(movie_name):
    base = "https://www.youtube.com/results?search_query="
    query = urllib.parse.quote(movie_name + " movie trailer")
    return base + query


def get_movies_by_genre(genre_name):

    if "Genre" not in movies.columns:
        return "Dataset lo Genre column ledu 😢"

    filtered = movies[
        movies["Genre"].fillna("").str.contains(genre_name, case=False)
    ].head(5)

    if filtered.empty:
        return "Movies dorakaledu 😢"

    result = []

    for _, row in filtered.iterrows():
        movie_name = row.get("Movie", "Unknown")

        result.append({
            "Movie": movie_name,
            "Rating": row.get("Rating", "N/A"),
            "Link": generate_link(movie_name)
        })

    return result


def chatbot_response(user_input):

    text = user_input.lower()

    # Greeting
    if any(word in text for word in ["hi", "hello", "hey"]):
        return "Hey 😊 Ela unnaru? Day ela undhi?"

    # Sad mood
    if any(word in text for word in ["sad", "low", "upset"]):
        return "Koncham happy avvadam kosam comedy try cheddama? 😄"

    # Happy mood
    if any(word in text for word in ["happy", "good", "fine"]):
        return "Super 😄 Comedy, Action, Romance, Thriller lo edhi chudali?"

    # OK / YES → default Comedy
    if any(word in text for word in ["ok", "okay", "yes", "sure"]):
        return get_movies_by_genre("Comedy")

    # Genre detection
    genre_map = {
        "comedy": "Comedy",
        "action": "Action",
        "romance": "Romance",
        "thriller": "Thriller"
    }

    for key, value in genre_map.items():
        if key in text:
            return get_movies_by_genre(value)

    return "Ardham kaaledu 😅 Mood or genre cheppandi"
