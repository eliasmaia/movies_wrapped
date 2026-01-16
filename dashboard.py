import streamlit as st
import pandas as pd

st.set_page_config(page_title="Meu Movie Wrapped", layout="wide")

st.title("Meu Ano em Filmes")
st.markdown("---")

df = pd.read_csv("meus_filmes_enriquecidos.csv")

# --- NOVO: SEÇÃO DE ESTATÍSTICAS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total de Filmes", value=len(df))

with col2:
    media_nota = df['personal_rating'].mean()
    st.metric(label="Média de Notas", value=f"{media_nota:.1f} ⭐")

with col3:
    # Conta quantos filmes têm nota 10
    top_filmes = len(df[df['personal_rating'] == 10])
    st.metric(label="Favoritos (Nota 10)", value=top_filmes)

nota_minima = st.slider("Filtar por nota minima", 0.0, 10.0, 7.0)

df_filtrado = df[df['personal_rating'] >= nota_minima]

cols = st.columns(4)

for index, row in df_filtrado.reset_index().iterrows():
    with cols[index % 4]:
        if pd.notna(row['poster_url']):
            st.image(row['poster_url'], caption=f"`{row['title']} ({int(row['launching_year'])})")
        else:
            st.warning(f"Sem poster para {row['title']}")

        
        st.write(f"Minha nota: **{row['personal_rating']}**")