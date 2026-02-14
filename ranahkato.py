import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz

# Fungsi untuk mencocokkan string dengan ketepatan yang mendekati
def match_strings(str1, str2):
    return fuzz.ratio(str1, str2)

# Upload file Excel dari pengguna
uploaded_file = st.file_uploader("Pilih file Excel", type=["xlsx"])

if uploaded_file is not None:
    # Memuat data dari file Excel yang di-upload
    data = pd.read_excel(uploaded_file)

    # Memilih Kolom yang Relevan dan Membersihkan Data
    cleaned_data = data[['Bentuk Kosakata', 'Transkripsi Fonemis', 'Kata']].dropna()

    # Menampilkan beberapa baris pertama untuk verifikasi
    st.write("Data Kosakata yang Diterima:")
    st.write(cleaned_data.head())

    # Input dari pengguna untuk mencari kosakata
    user_input = st.text_input("Masukkan Kosakata:")

    if user_input:
        # Mencocokkan kosakata pengguna dengan data yang ada
        matched_words = cleaned_data[cleaned_data['Bentuk Kosakata'].apply(lambda x: match_strings(user_input, x) > 80)]

        # Menampilkan hasil pencocokan
        if matched_words.empty:
            st.write("Tidak ada kosakata yang cocok dengan input Anda.")
        else:
            st.write("Kosakata yang cocok dengan input:")
            st.write(matched_words)
