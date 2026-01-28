import streamlit as streamlit
import pandas as pd
from helpers import formatar_duracao

streamlit.set_page_config(page_title="Movie Wrapped", layout="wide", page_icon="🎬")

# --- ESTILOS CSS ---
streamlit.markdown("""
    <style>
    .movie-card { border-radius: 10px; background-color: #1e1e1e; padding: 15px; margin-bottom: 20px; min-height: 580px; border: 1px solid #333;}
    .movie-title-main { font-size: 1.15rem; font-weight: 800; color: #FFFFFF !important; line-height: 1.2; margin-bottom: 2px;  }
    .poster-img { width: 100%; height: 380px; object-fit: cover; border-radius: 10px; transition: 0.3s;}
    .poster-img:hover { opacity: 0.8; transform: scale(1.02); }
    .badge {background: #333; color: white; padding: 2px 8px; border-radius: 12px; font-size: 10px; margin-right: 5px;}
    </style>
""", unsafe_allow_html=True)

@streamlit.cache_data
def load_data():
    return pd.read_csv("data/movies_enriched.csv")

dataframe = load_data()

# --- SIDEBAR / FILTROS ---
streamlit.sidebar.header("⚙️ Filtros")
busca = streamlit.sidebar.text_input("Buscar filme por titulo")
nota_minima = streamlit.slider("Nota minima", 0.0, 10.0, 7.0)

# Aplicando filtros
dataframe_filtered = dataframe[dataframe['personal_rating'] >= nota_minima]
if busca:
    dataframe_filtered = dataframe_filtered[dataframe_filtered['title_pt'].str.contains(busca, case=False) |
                                            dataframe_filtered['original_title'].str.contains(busca, case=False)]

# --- NOVO: BANNER HERÓI (Backdrop + Tagline) ---
top_movie = dataframe[dataframe['personal_rating'] == dataframe['personal_rating'].max()].iloc[-1]

streamlit.markdown(f"""
    <div style="position: relative; height: 350px; border-radius: 20px; overflow: hidden; background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{top_movie['backdrop_url']}'); background-size: cover; background-position: center; display: flex; align-items: center; justify-content: center; text-align: center; color: white; margin-bottom: 30px;">
        <div style="padding: 20px;">
            <h1 style="font-size: 3rem; margin-bottom: 0;">{top_movie['original_title']}</h1>
            <p style="font-size: 1.3rem; font-style: italic;">"{top_movie['tagline']}"</p>
            <div style="margin-top: 10px; font-size: 1.1rem;">🏆 Melhor do Ano</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- MÉTRICAS DE RECORDE (Runtime) ---

# --- NOVO: SEÇÃO DE ESTATÍSTICAS ---
coluna1, coluna2, coluna3, coluna4 = streamlit.columns(4)
coluna1.metric("Filmes", len(dataframe))
coluna2.metric("Média Geral", f"{dataframe['personal_rating'].mean():.1f}")

if 'runtime' in dataframe.columns:
    longo = dataframe.loc[dataframe['runtime'].idxmax()]
    curto = dataframe.loc[dataframe['runtime'].idxmin()]
    coluna3.metric("⌛ Maratona", f"{formatar_duracao(int(longo['runtime']))}", longo['original_title'])
    coluna4.metric("⏱️ Sessão Rápida", f"{formatar_duracao(int(curto['runtime']))}", curto['original_title'])

streamlit.write("---")
# Pega o filme de maior nota (se houver empate, pega o último da lista)

colunas = streamlit.columns(4)
for index, row in dataframe_filtered.reset_index().iterrows():
    with colunas[index % 4]:
        tmdb_url = f"https://www.themoviedb.org/movie/{row['tmdb_id']}"
        
        # Preparando Badges de Gênero
        badges_html = ""
        if pd.notna(row['genres']):
            for g in row['genres'].split(',')[:2]:
                badges_html += f'<span class="badge">{g.strip()}</span>'

        streamlit.markdown(f'''
            <div class="movie-card">
                <a href="{tmdb_url}" target="_blank">
                    <img src="{row['poster_url']}" class="poster-img">
                </a>
                <div style="height: 65px; margin-top: 10px; overflow: hidden;">
                    <div style="font-size: 1.1rem; font-weight: bold; line-height: 1.2;">{row['original_title']}</div>
                    <div style="color: #888; font-size: 0.85rem;">{row['title_pt']}</div>
                </div>
                <div style="margin-bottom: 10px;">{badges_html}</div>
                <div style="font-size: 0.85rem; color: #ccc;">🎬 {row['director']}</div>
                <div style="font-size: 1.2rem; margin-top: 5px;">⭐ <b>{row['personal_rating']}</b></div>
            </div>
        ''', unsafe_allow_html=True)

        streamlit.markdown("---")
streamlit.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Desenvolvido com Python & Streamlit por [Elias Maia] 🎬"
    "</div>", 
    unsafe_allow_html=True
)