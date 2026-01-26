import streamlit as streamlit
import pandas as pandas

streamlit.set_page_config(page_title="Movie Wrapped", layout="wide", page_icon="🎬")

streamlit.markdown("""
    <style>
    .movie-card { border-radius: 10px; background-color: #1e1e1e; padding: 10px; margin-bottom: 20px; }
    .movie-title { font-size: 1.1rem; font-weight: bold; color: white; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

@streamlit.cache_data
def load_data():
    return pandas.read_csv("data/movies_enriched.csv")

dataframe = load_data()

streamlit.title("🎬Meu Ano em Filmes")
streamlit.sidebar.header("⚙️ Filtros")
nota_minima = streamlit.slider("Nnota minima", 0.0, 10.0, 7.0)

# --- NOVO: SEÇÃO DE ESTATÍSTICAS ---
coluna1, coluna2, coluna3 = streamlit.columns(3)
coluna1.metric("Filmes Assistidos", len(dataframe))
coluna2.metric("Média Geral", f"{dataframe['personal_rating'].mean():.1f}")
coluna3.metric("Favoritos (Nota 10)", len(dataframe[dataframe['personal_rating'] == 10]))

dataframe_filtered = dataframe[dataframe['personal_rating'] >= nota_minima]


colunas = streamlit.columns(4)
for index, row in dataframe_filtered.reset_index().iterrows():
    with colunas[index % 4]:
        tmdb_url = f"https://www.themoviedb.org/movie/{row['tmdb_id']}"

        streamlit.markdown(f'''
            <a href="{tmdb_url}" target="_blank">
                <img src="{row['poster_url']}" style="width=100%; border-radius:10px; hover: opacity: 0.8;">
            </a>
        ''', unsafe_allow_html=True)

        streamlit.markdown(f"**{row['title']}**")
        streamlit.caption(f"_{row['original_title']}_ ({int(row['launching_year'])})")
        streamlit.markdown(f"🎥 {row['director']}")
        streamlit.write(f"⭐ Minha Nota: **{row['personal_rating']}**")