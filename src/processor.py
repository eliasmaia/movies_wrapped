import pandas as pd

class MovieProcessor:
    def __init__(self, client):
        self.client = client

    def enrich_csv(self, input_path, output_path):
        dataframe = pd.read_csv(input_path, skipinitialspace=True)
        enriched_data = []
        total = len(dataframe)

        print(f"🎬 Iniciando o enriquecimento de {total} filmes...\n")

        for index, row in dataframe.iterrows():
            try:
                print(f"[{index + 1}/{total}] Buscando: {row['title']}...")
                
                movie_basic = self.client.search_movie(row['title'], row['launching_year'])
                if not movie_basic:
                    continue

                movie_id = movie_basic.get('tmdb_id')
                details = self.client.get_movie_details(movie_id)
                director = self.client.get_movie_director(movie_id)

                if details:
                    enriched_data.append({
                        **details,
                        'director': director,
                        'personal_rating': row['personal_rating'],
                        'launching_year': row['launching_year'],
                        'tmdb_id': movie_id
                    })
                    
            except Exception as e:
                print(f"\n❌ Erro ao processar {row['title']}: {e}")
    
        if enriched_data:
            pd.DataFrame(enriched_data).to_csv(output_path, index=False)
            print(f"\n\n🚀 Finalizado! {len(enriched_data)} filmes salvos em: {output_path}")
        else:
            print(f"\n\n⚠️ Nenhum dado foi enriquecido.")
