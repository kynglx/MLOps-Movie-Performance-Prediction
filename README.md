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
