import requests

class TMDBClient:
    def __init__(self, token):
        self.base_url = "https://api.themoviedb.org/3"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "accept": "application/json"
        }
    
    def search_movie(self, title, year):
        url = f"{self.base_url}/search/movie"
        params = {"query": title, "year": year, "language": "pt-BR"}

        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            results = response.json().get('results')
            if results: 
                movie = results[0]
                return {
                    "tmdb_id": movie.get("id"),
                    "title_original": movie.get("original_title"),
                    "poster_url": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get('poster_path') else None
                }
        return None
    
    def get_movie_details(self, movie_id):
        if not movie_id: return None

        url = f"{self.base_url}/movie/{movie_id}"
        params = {"language": "pt-BR"}

        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()

            return {
                "title_pt": data.get("title"),
                "original_title": data.get("original_title"),
                "runtime": data.get("runtime", 0),
                "tagline": data.get("tagline", 0),
                "genres": ", ".join([g['name'] for g in data.get('genres', [])]),
                "backdrop_url": f"http://image.tmdb.org/t/p/original{data.get('backdrop_path')}" if data.get('backdrop_path') else None,
                "poster_url": f"http://image.tmdb.org/t/p/w500{data.get('poster_path')}" if data.get('poster_path') else None
            }
        return None
    
    def get_movie_director(self, movie_id):
        if not movie_id: return "Desconhecido"

        url = f"{self.base_url}/movie/{movie_id}/credits"
        response = requests.get(url, headers=self.headers)
 
        if response.status_code == 200:
            crew = response.json().get('crew', [])
            directors = [m['name'] for m in crew if m['job'] == 'Director']
            return ", ".join(directors) if directors else "Desconhecido"
        return "Desconhecido"