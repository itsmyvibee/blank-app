import os
from pathlib import Path
import streamlit as st
from openpyxl import load_workbook  # só para descobrir o nome da planilha
from xlcalculator import ModelCompiler, Evaluator

st.set_page_config(page_title="Excel como motor", page_icon="🧮")

# Oculta menus/ícone do GitHub (visual)
st.markdown("""
<style>
#MainMenu, footer {visibility: hidden;}
header [data-testid="stToolbar"] {visibility: hidden;}
a[href*="github.com"] {display:none !important;}
</style>
""", unsafe_allow_html=True)

st.title("Excel como motor de cálculo (B1, B2 → B3)")

# === AJUSTE AQUI SE PRECISAR ===
# Se o arquivo estiver na mesma pasta do streamlit_app.py:
EXCEL_PATH = Path(__file__).parent / "Book_1.xlsx"
# Exemplo se estiver em subpasta "assets":
# EXCEL_PATH = Path(__file__).parent / "assets" / "Book_1.xlsx"
# ================================

# Debug: listar arquivos da pasta do app
st.caption("Arquivos na pasta do app:")
st.code("\n".join(sorted(os.listdir(Path(__file__).parent))), language="text")

# Checar existência do arquivo local (sem URL!)
if not EXCEL_PATH.exists():
    st.error(f"Arquivo não encontrado: {EXCEL_PATH.name}. "
             f"Coloque-o no mesmo diretório do app ou ajuste EXCEL_PATH.")
    st.stop()

# Descobrir o nome da primeira planilha (caso você não queira fixar)
try:
    wb = load_workbook(EXCEL_PATH, data_only=False, read_only=True)
    SHEET = wb.sheetnames[0]
except Exception as e:
    st.error(f"Não consegui abrir o Excel para ler o nome da planilha: {e}")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    x = st.number_input("Valor para B1", value=0.0, step=1.0, format="%.2f")
with col2:
    y = st.number_input("Valor para B2", value=0.0, step=1.0, format="%.2f")

if st.button("Calcular"):
    try:
        # Compilar e avaliar SEM cache, para evitar vestígios de URL antiga
        model = ModelCompiler().read_and_parse_archive(str(EXCEL_PATH))
        ev = Evaluator(model)

        ev.set_cell_value(f"{SHEET}!B1", x)
        ev.set_cell_value(f"{SHEET}!B2", y)
        result = ev.evaluate(f"{SHEET}!B3")

        if isinstance(result, (int, float)):
            st.success(f"Resultado em B3: {result:.2f}")
        else:
            st.warning(f"B3 retornou um valor não numérico: {result}")

    except Exception as e:
        st.error(f"Erro ao avaliar B3: {e}")
