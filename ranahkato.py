import pandas as pd
from rapidfuzz import fuzz
import streamlit as st

# 1. Memuat Data Kosakata dari URL Raw GitHub
file_url = "https://raw.githubusercontent.com/akbaridaman/ranahkato/main/ranahkato.xlsx"
try:
    # Membaca semua sheet dalam file Excel
    data = pd.read_excel(file_url, sheet_name=None)
except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat file: {e}")
    st.stop()

# 2. Menampilkan nama-nama sheet yang ada dalam file
st.write("Nama-nama sheet dalam file Excel:")
st.write(data.keys())

# 3. Menyiapkan Data dari Setiap Sheet
cleaned_data = {}
for sheet_name, sheet_data in data.items():
    if 'Bentuk Kosakata' in sheet_data.columns and 'Transkripsi Fonemis' in sheet_data.columns and 'Kata' in sheet_data.columns:
        cleaned_data[sheet_name] = sheet_data[['Bentuk Kosakata', 'Transkripsi Fonemis', 'Kata']].dropna()

# 4. Fungsi untuk Mencocokkan String dengan Ketepatan yang Mendekati (menggunakan partial_ratio untuk case-insensitive)
def match_strings(str1, str2):
    str1 = str1.strip().lower()
    str2 = str2.strip().lower()
    return fuzz.partial_ratio(str1, str2)

# 5. Menggunakan Streamlit untuk Input dan Menampilkan Hasil
st.title("Aplikasi Pencarian Kosakata Minangkabau")

# Input dari pengguna
user_input = st.text_input("Masukkan Kosakata:")

# Proses pencarian jika pengguna memasukkan input
if user_input:
    all_matches = {}
    
    # Mencocokkan kosakata pengguna dengan data yang ada pada setiap sheet
    for sheet_name, sheet_data in cleaned_data.items():
        matched_words = sheet_data[sheet_data['Bentuk Kosakata'].apply(lambda x: match_strings(user_input, x) > 80)]
        
        if not matched_words.empty:
            all_matches[sheet_name] = matched_words

    # Menampilkan hasil pencocokan
    if not all_matches:
        st.write("Tidak ada kosakata yang cocok dengan input Anda.")
    else:
        for sheet_name, matched_words in all_matches.items():
            st.write(f"Kosakata yang cocok pada tabel '{sheet_name}':")
            st.write(matched_words)
