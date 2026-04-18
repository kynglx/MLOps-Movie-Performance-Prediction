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
