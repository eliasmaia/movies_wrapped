import pandas as pandas
import time

class MovieProcessor:
    def __init__(self, client):
        self.client = client

    def enrich_csv(self, input_path, output_path):
        dataframe = pandas.read_csv(input_path, skipinitialspace=True)
        enriched_data = []

        for index, row in dataframe.iterrows():
            movie_data = self.client.search_movie(row['title'], row['launching_year'])

            if movie_data:
                director = self.client.get_movie_director(movie_data['tmdb_id'])
                enriched_data.append({
                    'title': row['title'],
                    'launching_year': row['launching_year'],
                    'personal_rating': row['personal_rating'],
                    'original_title': movie_data['title_original'],
                    'director': director,
                    'poster_url': movie_data['poster_url'],
                    'tmdb_id': movie_data['tmdb_id']
                })
            else:
                enriched_data.append({**row.to_dict(), 'director': 'N/A', 'poster_url': None, 'tmdb_id': None})

            time.sleep(0.2)

        pandas.DataFrame(enriched_data).to_csv(output_path, index=False)
