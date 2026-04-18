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

    df = df[[
        "id",
        "title",
        "popularity",
        "vote_average",
        "vote_count",
        "release_date",
        "source"
    ]]

    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

    df["release_year"] = df["release_date"].dt.year
    df["is_recent"] = df["release_year"] >= 2020
    df["popularity_log"] = np.log1p(df["popularity"])

    df["is_popular"] = df["source"] == "popular"

    df = df.drop_duplicates(subset="id")
    df = df.dropna(subset=["title", "popularity", "vote_average"])

    return df

def save_processed_data(df):
    os.makedirs("data", exist_ok=True)

    file_path = "data/processed/dataset.csv"

    # kalau file sudah ada → gabung + drop duplicate
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)

        combined_df = pd.concat([existing_df, df], ignore_index=True)

        # agar tidak double antar ingestion
        combined_df = combined_df.drop_duplicates(subset="id")

        combined_df.to_csv(file_path, index=False)
        print("Dataset berhasil diupdate (append + deduplicate).")

    else:
        df.to_csv(file_path, index=False)
        print("Dataset baru dibuat.")

if __name__ == "__main__":
    latest_file = get_latest_file()
    df = preprocess_data(latest_file)
    save_processed_data(df)