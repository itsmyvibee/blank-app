from pathlib import Path
import streamlit as st
from xlcalculator import ModelCompiler, Evaluator

# ⛔ NADA de URL. Use caminho local.
# Dica: renomeie o arquivo para evitar espaço: "Book_1.xlsx"
EXCEL_NAME = "Book 1.xlsx"  # ou "Book_1.xlsx" se você renomear
EXCEL_PATH = Path(__file__).parent / EXCEL_NAME

if not EXCEL_PATH.exists():
    st.error(f"Arquivo '{EXCEL_NAME}' não encontrado na pasta do app. "
             f"Coloque-o no mesmo diretório do streamlit_app.py.")
    st.stop()

# (Opcional) cache para acelerar recompilações
@st.cache_resource
def load_model(path: Path):
    return Evaluator(ModelCompiler().read_and_parse_archive(str(path)))

ev = load_model(EXCEL_PATH)

# Entradas
x = st.number_input("Valor para B1", value=0.0, step=1.0, format="%.2f")
y = st.number_input("Valor para B2", value=0.0, step=1.0, format="%.2f")

if st.button("Calcular"):
    # Ajuste o nome da planilha se não for a primeira/“Planilha1”
    sheet = ev.model.get_sheet_names()[0]
    ev.set_cell_value(f"{sheet}!B1", x)
    ev.set_cell_value(f"{sheet}!B2", y)
    result = ev.evaluate(f"{sheet}!B3")
    st.success(f"Resultado (B3): {float(result):.2f}")
