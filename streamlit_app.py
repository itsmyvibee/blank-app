import streamlit as st
from pathlib import Path
from openpyxl import load_workbook
from xlcalculator import ModelCompiler, Evaluator, readers

st.set_page_config(page_title="Motor Excel", page_icon="🧮", layout="centered")

# CSS para esconder menu/rodapé/ícone GitHub (visual)
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header [data-testid="stToolbar"] {visibility: hidden;}
button[kind="header"] {visibility: hidden;}
a[href*="github.com"] {display:none !important;}
</style>
""", unsafe_allow_html=True)

st.title("Excel como motor de cálculo")

# Caminho local do Excel (o arquivo deve estar no mesmo repo do app)
EXCEL_FILE = Path(__file__).parent / "Book 1.xlsx"
if not EXCEL_FILE.exists():
    st.error(f"Arquivo não encontrado: {EXCEL_FILE.name}. Coloque-o na raiz do app.")
    st.stop()

# Descobre automaticamente o nome da 1ª planilha para montar endereços tipo Sheet!B1
try:
    wb = load_workbook(EXCEL_FILE, data_only=False, read_only=True)
    sheet_name = wb.sheetnames[0]
except Exception as e:
    st.error(f"Não consegui abrir o Excel: {e}")
    st.stop()

# Entradas
col1, col2 = st.columns(2)
with col1:
    x = st.number_input("Valor para B1", value=0.0, step=1.0, format="%.2f")
with col2:
    y = st.number_input("Valor para B2", value=0.0, step=1.0, format="%.2f")

if st.button("Calcular (preencher B1/B2 e ler B3)"):
    try:
        # Compila o modelo do Excel uma única vez por execução do botão
        model = ModelCompiler().read_and_parse_archive(str(EXCEL_FILE))
        ev = Evaluator(model)

        # Define os valores de entrada
        ev.set_cell_value(f"{sheet_name}!B1", x)
        ev.set_cell_value(f"{sheet_name}!B2", y)

        # Avalia a célula B3
        result = ev.evaluate(f"{sheet_name}!B3")

        # Mostra com 2 casas decimais
        if isinstance(result, (int, float)):
            st.success(f"Resultado em B3: {result:.2f}")
        else:
            st.warning(f"B3 retornou um valor não numérico: {result}")

    except Exception as e:
        st.error(f"Erro ao calcular B3 via xlcalculator: {e}")
