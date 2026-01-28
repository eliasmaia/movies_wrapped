import pandas as pd
import time

class MovieProcessor:
    def __init__(self, client):
        self.client = client

    def enrich_csv(self, input_path, output_path):
        dataframe = pd.read_csv(input_path, skipinitialspace=True)
        enriched_data = []

        for _, row in dataframe.iterrows():
            movie_basic = self.client.search_movie(row['title'], row['launching_year'])
            if movie_basic:
                movie_id = movie_basic.get('id')

                details = self.client.get_movie_details(movie_id)
                director = self.client.get_movie_director(movie_id)

                if details:
                    full_movie_data = {
                        **details,
                        'director': director,
                        'personal_rating': row['personal_rating'],
                        'launching_year': row['launching_year'],
                        'tmdb_id': movie_id
                    }
                    enriched_data.append(full_movie_data)
                    print(f"✅ Sucesso: {details['original_title']}")
                else:
                    print(f"❌ Não encontrado: {row['title']}")
    
        if enriched_data:
            pd.DataFrame(enriched_data).to_csv(output_path, index=False)
            print(f"\n🚀 Fim! Arquivo salvo em: {output_path}")
        else:
            print(f"\n⚠️ Nenhum dado foi enriquecido.")
