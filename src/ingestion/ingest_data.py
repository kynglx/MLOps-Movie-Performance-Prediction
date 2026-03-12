import requests
import json
import os

API_KEY = "45c99d078a3a1036afd142669c03c5c5"
url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page=1"

response = requests.get(url)

data = response.json()

os.makedirs("data/raw", exist_ok=True)

with open("data/raw/movies_raw.json", "w") as f:
    json.dump(data, f, indent=4)

print("Data berhasil diambil dan disimpan di data/raw/")