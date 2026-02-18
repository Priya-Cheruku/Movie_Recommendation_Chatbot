import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("TeluguMovies_dataset.csv")

df = df.drop(columns=['Unnamed: 0'])
df['Overview'] = df['Overview'].fillna("")

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['Overview'])

similarity = cosine_similarity(tfidf_matrix)

def recommend_by_genre(genre, top_n=5):
    filtered = df[df['Genre'].fillna("").str.lower().str.contains(genre.lower(), na=False)]
    return filtered.sort_values(by='Rating', ascending=False).head(top_n)

def recommend_by_story(movie_name, top_n=5):
    if movie_name not in df['Movie'].values:
        return "Movie not found raa"

    idx = df[df['Movie'] == movie_name].index[0]
    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    movie_indices = [i[0] for i in sim_scores]

    return df.iloc[movie_indices][['Movie', 'Rating', 'Genre']]
