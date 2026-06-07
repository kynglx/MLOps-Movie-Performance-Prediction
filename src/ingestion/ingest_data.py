import requests
import json
import os
from datetime import datetime

API_KEY = "45c99d078a3a1036afd142669c03c5c5"
BASE_URL = "https://api.themoviedb.org/3/movie"

ENDPOINTS = [
    "popular",
    "now_playing",
    "top_rated",
    "upcoming"
]

def fetch_movies(endpoint, total_pages=6):
    all_movies = []

    for page in range(1, total_pages + 1):
        url = f"{BASE_URL}/{endpoint}"

        params = {
            "api_key": API_KEY,
            "language": "en-US",
            "page": page
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        for movie in data["results"]:
            movie["source"] = endpoint

        all_movies.extend(data["results"])

    return all_movies

def fetch_all_movies():
    all_movies = []

    for endpoint in ENDPOINTS:
        print(f"Fetching: {endpoint}")
        movies = fetch_movies(endpoint, total_pages=5)
        all_movies.extend(movies)

    return all_movies

def save_raw_data(movies):
    os.makedirs("data/raw", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/raw/movies_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(movies, f, indent=4)

    print(f"Data disimpan di: {filename}")

if __name__ == "__main__":
    movies = fetch_all_movies()
    save_raw_data(movies)