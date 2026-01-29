import os
from dotenv import load_dotenv
from src.tmdb_client import TMDBClient
from src.processor import MovieProcessor

def main():
    load_dotenv()

    client = TMDBClient(os.getenv('TMDB_TOKEN'))
    processor = MovieProcessor(client)

    processor.enrich_csv('data/movies_watched.csv', 'data/movies_enriched.csv')

if __name__ == "__main__":
    main()
