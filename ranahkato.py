import pandas as pd
from fuzzywuzzy import fuzz
import streamlit as st

# 1. Memuat Data Kosakata
file_path = "https://raw.githubusercontent.com/akbaridaman/ranahkato/main/ranahkato.xlsx"
data = pd.read_excel(file_path)

# 2. Memilih Kolom yang Relevan dan Membersihkan Data
cleaned_data = data[['Bentuk Kosakata', 'Transkripsi Fonemis', 'Kata']].dropna()

# 3. Fungsi untuk Mencocokkan String dengan Ketepatan yang Mendekati
def match_strings(str1, str2):
    # Mengubah kedua string menjadi huruf kecil
    str1 = str1.lower()
    str2 = str2.lower()
    return fuzz.ratio(str1, str2)

# 4. Menggunakan Streamlit untuk Input dan Menampilkan Hasil
# Judul aplikasi
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



