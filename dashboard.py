import streamlit as streamlit
import pandas as pd
from helpers import formatar_duracao

streamlit.set_page_config(page_title="Movies Wrapped", layout="wide", page_icon="🎬")

streamlit.markdown("""
    <style>
    .movie-card { border-radius: 10px; background-color: #1e1e1e; padding: 15px; margin-bottom: 20px; min-height: 580px; border: 1px solid #333;}
    .movie-title-main { font-size: 1.15rem; font-weight: 800; color: #FFFFFF !important; line-height: 1.2; margin-bottom: 2px;  }
    .poster-img { width: 100%; height: 380px; object-fit: cover; border-radius: 10px; transition: 0.3s;}
    .poster-img:hover { opacity: 0.8; transform: scale(1.02); }
    .badge {background: #333; color: white; padding: 2px 8px; border-radius: 12px; font-size: 10px; margin-right: 5px;}
    .rating-text { font-size: 1.25rem; font-weight: 800; color: #FFD700 !important; /* Dourado vibrante */ margin-top: 8px; display: flex; align-items: center; gap: 5px;}
    </style>
""", unsafe_allow_html=True)

@streamlit.cache_data
def load_data():
    return pd.read_csv("data/movies_enriched.csv")

dataframe = load_data().sort_values(by='personal_rating', ascending=False, na_position='last')

df_metrics = dataframe[dataframe['personal_rating'] > 0].copy()

streamlit.sidebar.header("⚙️ Filtros")
busca = streamlit.sidebar.text_input("Buscar filme por titulo")
streamlit.sidebar.divider()
nota_minima = streamlit.sidebar.slider("Nota minima", 0.0, 10.0, 7.0)

dataframe_filtered = dataframe[
    (dataframe['personal_rating'] >= nota_minima) | 
    (dataframe['personal_rating'].isna()) | 
    (dataframe['personal_rating'] <= 0)
]
if busca:
    dataframe_filtered = dataframe_filtered[dataframe_filtered['title_pt'].str.contains(busca, case=False) |
                                            dataframe_filtered['original_title'].str.contains(busca, case=False)]

top_movie = df_metrics[df_metrics['personal_rating'] == df_metrics['personal_rating'].max()].iloc[-1]

backdrop = top_movie['backdrop_url'] if pd.notna(top_movie['backdrop_url']) else "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba" # Uma imagem genérica de cinema
tagline = top_movie["tagline"] if pd.notna(top_movie['tagline']) and top_movie['tagline'] != "" else "Todas as vezes que vou ao cinema é mágico, e não interessa que filme que é. (Steven Spielberg)"

streamlit.markdown(f"""
    <div style="position: relative; height: 350px; border-radius: 20px; overflow: hidden; background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{backdrop}'); background-size: cover; background-position: center; display: flex; align-items: center; justify-content: center; text-align: center; color: white; margin-bottom: 30px;">
        <div style="padding: 20px;">
            <h1 style="font-size: 3rem; margin-bottom: 0;">{top_movie['original_title']}</h1>
            <p style="font-size: 1.3rem; font-style: italic;">"{tagline}"</p>
        </div>
    </div>
""", unsafe_allow_html=True)

coluna1, coluna2, coluna3, coluna4 = streamlit.columns(4)
coluna1.metric("Filmes Finalizados", len(df_metrics))
coluna2.metric("Média Geral", f"{df_metrics['personal_rating'].mean():.1f}")

if 'runtime' in df_metrics.columns:
    longo = df_metrics.loc[df_metrics['runtime'].idxmax()]
    curto = df_metrics.loc[df_metrics['runtime'].idxmin()]
    coluna3.metric("⌛ Maratona", f"{formatar_duracao(int(longo['runtime']))}", longo['original_title'])
    coluna4.metric("⏱️ Sessão Rápida", f"{formatar_duracao(int(curto['runtime']))}", curto['original_title'])

streamlit.write("---")
streamlit.subheader("🍿 Minha Jornada Cinematográfica")

colunas = streamlit.columns(4)
for index, row in dataframe_filtered.reset_index().iterrows():
    with colunas[index % 4]:
        tmdb_url = f"https://www.themoviedb.org/movie/{row['tmdb_id']}"
        
        rating = row['personal_rating']
        if pd.isna(rating) or rating <= 0:
            rating_display = "🚫 Abandonado"
            rating_color = "#888"
            card_opacity = "0.6"
            border_color = "#444"
        else:
            rating_display = f"⭐ {rating}"
            rating_color = "#FFD700"
            card_opacity = "1.0"
            border_color = "#FFD700" if rating >= 9 else "#333"

        badges_html = ""
        if pd.notna(row['genres']):
            for g in row['genres'].split(',')[:3]:
                badges_html += f'<span class="badge">{g.strip()}</span>'
        
        border_width = "2px" if (not pd.isna(rating) and rating >= 9) else "1px"
        card_style = f"opacity: {card_opacity}; border: {border_width} solid {border_color};"
        ano_display = f"({int(row['launching_year'])})"

        streamlit.markdown(f"""
            <div class="movie-card" style="{card_style}">
                <a href="{tmdb_url}" target="_blank">
                    <img src="{row['poster_url']}" class="poster-img">
                </a>
                <div style="height: 65px; margin-top: 10px; overflow: hidden;">
                    <div class="movie-title-main">{row['original_title']}</div>
                    <div style="color: #888; font-size: 0.85rem;">{row['title_pt']}</div>
                </div>
                <div style="margin-bottom: 10px;">{badges_html}</div>
                <div style="font-size: 0.85rem; color: #ccc;">
                    🎬 {row['director']} <br>
                    <span style="color: #666;">{ano_display}</span>
                </div>
                <div class="rating-text" style="color: {rating_color} !important;">
                    {rating_display}
                </div>
            </div>
        """, unsafe_allow_html=True)

total_minutos = df_metrics['runtime'].sum()
horas_totais = total_minutos // 60
minutos_totais = total_minutos % 60
pipocas = total_minutos // 100

streamlit.markdown(f"""
    <div style="
        background-color: #1e1e1e; 
        padding: 25px; 
        border-radius: 15px; 
        border: 1px solid #333; 
        text-align: center;
        margin: 20px 0;
    ">
        <span style="color: #888; font-size: 1rem; text-transform: uppercase; letter-spacing: 1px;">
            📊 Curiosidades da sua Jornada
        </span>
        <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; margin-top: 15px;">
            <div style="margin: 10px;">
                <span style="font-size: 1.8rem;">⏳</span>
                <span style="font-size: 1.5rem; font-weight: bold; color: white; margin-left: 10px;">
                    {horas_totais}h {minutos_totais}min
                </span>
                <p style="color: #666; margin: 0;">vividos em outras histórias</p>
            </div>
            <div style="margin: 10px;">
                <span style="font-size: 1.8rem;">🍿</span>
                <span style="font-size: 1.5rem; font-weight: bold; color: white; margin-left: 10px;">
                    {pipocas} baldes
                </span>
                <p style="color: #666; margin: 0;">de pipoca (estimados)</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)


streamlit.markdown(
    """
    <div style='text-align: center; color: #666; margin-top: 50px; padding: 20px; border-top: 1px solid #333;'>
        Desenvolvido com Python & Streamlit por 
        <a href='https://github.com/eliasmaia' target='_blank' style='color: #888; text-decoration: none; border-bottom: 1px solid #444;'>
            Elias Maia
        </a> 🎬
    </div>
    """, 
    unsafe_allow_html=True
)