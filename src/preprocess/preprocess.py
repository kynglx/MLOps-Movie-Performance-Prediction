import json
import pandas as pd
import numpy as np
import os
from datetime import datetime

def get_latest_file():
    files = os.listdir("data/raw")
    json_files = [f for f in files if f.endswith(".json")]

    if not json_files:
        raise FileNotFoundError("Tidak ada file di data/raw/")

    json_files = ["data/raw/" + f for f in json_files]

    latest_file = max(json_files, key=os.path.getctime)
    print(f"Menggunakan file terbaru: {latest_file}")

    return latest_file

def preprocess_data(file_path):
    with open(file_path, "r") as f:
        movies = json.load(f)

    df = pd.DataFrame(movies)

    # pilih kolom
    df = df[[
        "id",
        "title",
        "popularity",
        "vote_average",
        "vote_count",
        "release_date",
        "source"
    ]]

    # ubah tipe tanggal
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

    # feature engineering
    df["release_year"] = df["release_date"].dt.year
    df["is_recent"] = df["release_year"] >= 2020
    df["popularity_log"] = np.log1p(df["popularity"])

    # encode source jadi fitur
    df["is_popular"] = df["source"] == "popular"

    # hapus duplikat (film bisa muncul di 2 endpoint)
    df = df.drop_duplicates(subset="id")

    # handle missing values
    df = df.dropna(subset=["title", "popularity", "vote_average"])

    return df

def save_processed_data(df):
    os.makedirs("data/processed", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/processed/movies_clean_{timestamp}.csv"

    df.to_csv(filename, index=False)
    print(f"Data bersih disimpan di: {filename}")

if __name__ == "__main__":
    latest_file = get_latest_file()
    df = preprocess_data(latest_file)
    save_processed_data(df)