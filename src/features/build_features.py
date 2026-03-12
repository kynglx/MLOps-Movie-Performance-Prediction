import json
import pandas as pd
import os

# baca file JSON
with open("data/raw/movies_raw.json") as f:
    data = json.load(f)

# ambil bagian results
movies = data["results"]

# ubah jadi dataframe
df = pd.DataFrame(movies)

# pilih kolom yang penting
df = df[[
    "title",
    "popularity",
    "vote_average",
    "vote_count",
    "release_date"
]]

# ubah release_date jadi datetime
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

# buat fitur baru: tahun rilis
df["release_year"] = df["release_date"].dt.year

# hapus data kosong
df = df.dropna()

# buat folder processed jika belum ada
os.makedirs("data/processed", exist_ok=True)

# simpan dataset bersih
df.to_csv("data/processed/movies_clean.csv", index=False)

print("Data cleaning selesai. File disimpan di data/processed/")