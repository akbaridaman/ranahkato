import pandas as pd
from fuzzywuzzy import fuzz
import streamlit as st

# 1. Memuat Data Kosakata dari URL Raw GitHub
file_url = "https://raw.githubusercontent.com/akbaridaman/ranahkato/main/ranahkato.xlsx"
try:
    data = pd.read_excel(file_url)
except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat file: {e}")
    st.stop()

# 2. Memeriksa kolom yang ada di dalam file
st.write("Kolom yang ada dalam data:")
st.write(data.columns)

# 3. Memilih Kolom yang Relevan dan Membersihkan Data
if 'Bentuk Kosakata' in data.columns and 'Transkripsi Fonemis' in data.columns and 'Kata' in data.columns:
    cleaned_data = data[['Bentuk Kosakata', 'Transkripsi Fonemis', 'Kata']].dropna()
else:
    st.error("Kolom yang diperlukan tidak ditemukan dalam data.")
    st.stop()

# 4. Fungsi untuk Mencocokkan String dengan Ketepatan yang Mendekati (menggunakan partial_ratio untuk case-insensitive)
def match_strings(str1, str2):
    # Mengubah kedua string menjadi huruf kecil dan menghapus spasi ekstra
    str1 = str1.strip().lower()
    str2 = str2.strip().lower()
    return fuzz.partial_ratio(str1, str2)

# 5. Menggunakan Streamlit untuk Input dan Menampilkan Hasil
st.title("Aplikasi Pencarian Kosakata Minangkabau")

# Input dari pengguna
user_input = st.text_input("Masukkan Kosakata:")

# Proses pencarian jika pengguna memasukkan input
if user_input:
    # Mencocokkan kosakata pengguna dengan data yang ada
    matched_words = cleaned_data[cleaned_data['Bentuk Kosakata'].apply(lambda x: match_strings(user_input, x) > 80)]
    
    # Menampilkan kosakata yang cocok dengan input
    if matched_words.empty:
        st.write("Tidak ada kosakata yang cocok dengan input Anda.")
    else:
        st.write("Kosakata yang cocok dengan input:")
        st.write(matched_words)
