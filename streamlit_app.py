import streamlit as st
import pandas as pd

# URL do Excel no GitHub (use o link "raw")
url = "https://raw.githubusercontent.com//itsmyvibee/blank-app/tree/main/Book 1.xlsx"

# Ler o Excel direto do GitHub
df = pd.read_excel(url)

st.write("Prévia do arquivo:")
st.dataframe(df)
