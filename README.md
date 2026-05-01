# MLOps-Movie-Performance-Prediction
MLOps project for predicting movie performance to support cinema screening optimization.

## Project Overview

Proyek ini bertujuan untuk memprediksi performa film di bioskop menggunakan pendekatan machine learning. Model akan memanfaatkan data film seperti genre, rating, budget, dan popularity untuk memprediksi apakah sebuah film berpotensi menjadi sukses di bioskop.

Proyek ini juga menerapkan praktik MLOps untuk memastikan pipeline machine learning dapat direproduksi dan dikelola dengan baik.

## Tech Stack

- Python
- Jupyter Notebook
- GitHub Codespaces
- GitHub Flow

## Project Structure
data/ → dataset film
models/ → model hasil training
notebooks/ → eksplorasi data (EDA)
src/ → kode utama machine learning
config/ → konfigurasi eksperimen


## Development Environment

Proyek ini menggunakan **GitHub Codespaces** untuk memastikan lingkungan pengembangan yang konsisten.

### Cara menjalankan Codespaces

1. Buka repository GitHub
2. Klik **Code**
3. Pilih tab **Codespaces**
4. Klik **Create Codespace**

Lingkungan Python akan otomatis dikonfigurasi sesuai dengan devcontainer yang tersedia.

## Branching Strategy

Repository ini menggunakan **GitHub Flow**.

Contoh branch:

feat/initial-eda

Branch ini digunakan untuk melakukan eksplorasi data awal sebelum digabungkan ke branch `main`.

## 📥 Data Ingestion

Script `ingest_data.py` digunakan untuk mengambil data film dari TMDB API.

Sumber data:

* `now_playing` → film yang sedang tayang
* `popular` → film yang sedang populer

Setiap kali script dijalankan:

* Data terbaru akan diambil dari API
* Data disimpan ke folder `data/raw/`
* Nama file menggunakan timestamp (tidak overwrite)

### ▶️ Cara Menjalankan

```bash
python src/ingest_data.py
```

### 📂 Output

Contoh file:

```
data/raw/movies_20260405_101530.json
```

---

## 🧹 Data Preprocessing

Script `preprocess.py` digunakan untuk membersihkan dan menyiapkan data.

Proses yang dilakukan:

* Mengambil file terbaru dari folder `data/raw/`
* Memilih kolom penting
* Mengubah format tanggal
* Menambahkan fitur baru
* Menghapus data duplikat dan kosong

### ▶️ Cara Menjalankan

```bash
python src/preprocess.py
```

### 📂 Output

Contoh file:

```
data/processed/movies_clean_20260405_101600.csv
```

---

## 🔁 Continual Learning Concept

Pipeline ini mendukung konsep continual learning karena:

* Data disimpan menggunakan timestamp
* Setiap proses menghasilkan file baru
* Data lama tidak dihapus
* Data dapat dikumpulkan secara bertahap

---

## ⚙️ Teknologi yang Digunakan

* Python
* Requests
* Pandas
* NumPy

---

## 📌 Catatan

* Pastikan API Key TMDB sudah dimasukkan di `ingest_data.py`
* Script dapat dijalankan berulang kali untuk mengambil data terbaru
* Dokumentasi dan kode telah diperbarui sesuai kebutuhan pipeline


## 📦 Data Versioning dengan DVC

Pada proyek ini digunakan DVC (Data Version Control) untuk mengelola versi dataset tanpa membebani Git dengan file berukuran besar. DVC memungkinkan pelacakan perubahan data melalui file metadata (.dvc), sehingga setiap perubahan dataset dapat direkam dengan jelas.

---

### 🚀 Inisialisasi DVC

Langkah pertama adalah menginisialisasi DVC pada repository:

```bash
dvc init
git add .dvc .gitignore
git commit -m "init DVC"
```

---

### 📥 Tracking Dataset Awal

Dataset hasil preprocessing (`dataset.csv`) mulai dilacak menggunakan DVC:

```bash
dvc add data/processed/dataset.csv
git add data/processed/dataset.csv.dvc .gitignore
git commit -m "track initial dataset"
```

File `.dvc` yang dihasilkan berisi metadata seperti hash dan ukuran file, sedangkan file dataset asli tidak disimpan di Git.

---

### 🔄 Simulasi Continual Learning

Untuk mensimulasikan penambahan data baru:

1. Jalankan kembali pipeline:

```bash
python src/ingest_data.py
python src/preprocess.py
```

2. Dataset akan diperbarui (ditambahkan data baru).

---

### 🆕 Versioning Dataset Baru

Setelah dataset berubah, lakukan tracking ulang:

```bash
dvc add data/processed/dataset.csv
git add data/processed/dataset.csv.dvc
git commit -m "update dataset version"
```

Perubahan isi dataset akan menghasilkan hash baru pada file `.dvc`, yang menandakan adanya versi data baru.

---

### 🔍 Audit Perubahan Data

Untuk melihat perbedaan antar versi dataset:

```bash
dvc diff HEAD~1 HEAD
```

Contoh output:

```
Modified:
    data/processed/dataset.csv

files summary: 1 modified
```

Hal ini menunjukkan bahwa dataset telah mengalami perubahan antara dua versi yang berbeda.

---

### MLflow
Model dilatih menggunakan Random Forest Regressor dengan beberapa percobaan parameter.  
Setiap eksperimen dicatat menggunakan MLflow (parameter, RMSE, dan model).

Model terbaik:
- n_estimators = 90  
- max_depth = 5  
- RMSE = 105.65  

Lebih baik dibandingkan hasil sebelumnya (RMSE = 109.89).

---

### Model Registry
Model terbaik didaftarkan ke MLflow Model Registry dengan nama:

movie-popularity-model

Setiap training menghasilkan versi model (v1, v2, dst).  
Model dengan RMSE terendah dipilih dan dipromosikan ke **Production**.

---

### DVC Metadata
Metadata model disimpan dalam file:

model_info.yaml

Contoh:
model_name: movie-popularity-model  
version: 8  
stage: Production  
rmse: 105.65  

---

### Inference
Model Production dapat digunakan untuk prediksi dengan MLflow:

model = mlflow.pyfunc.load_model("models:/movie-popularity-model/Production")

Model berhasil digunakan untuk prediksi sehingga siap digunakan.
