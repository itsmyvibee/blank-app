import os
from pathlib import Path
import streamlit as st
from openpyxl import load_workbook  # só para descobrir o nome da planilha
from xlcalculator import ModelCompiler, Evaluator

# st.set_page_config(page_title="Excel como motor", page_icon="🧮")

# # Oculta menus/ícone do GitHub (visual)
# st.markdown("""
# <style>
# #MainMenu, footer {visibility: hidden;}
# header [data-testid="stToolbar"] {visibility: hidden;}
# a[href*="github.com"] {display:none !important;}
# </style>
# """, unsafe_allow_html=True)

# st.title("Excel como motor de cálculo (B1, B2 → B3)")

# # === AJUSTE AQUI SE PRECISAR ===
# # Se o arquivo estiver na mesma pasta do streamlit_app.py:
# EXCEL_PATH = Path(__file__).parent / "Book_1.xlsx"
# # Exemplo se estiver em subpasta "assets":
# # EXCEL_PATH = Path(__file__).parent / "assets" / "Book_1.xlsx"
# # ================================

# # Debug: listar arquivos da pasta do app
# st.caption("Arquivos na pasta do app:")
# st.code("\n".join(sorted(os.listdir(Path(__file__).parent))), language="text")

# # Checar existência do arquivo local (sem URL!)
# if not EXCEL_PATH.exists():
#     st.error(f"Arquivo não encontrado: {EXCEL_PATH.name}. "
#              f"Coloque-o no mesmo diretório do app ou ajuste EXCEL_PATH.")
#     st.stop()

# # Descobrir o nome da primeira planilha (caso você não queira fixar)
# try:
#     wb = load_workbook(EXCEL_PATH, data_only=False, read_only=True)
#     SHEET = wb.sheetnames[0]
# except Exception as e:
#     st.error(f"Não consegui abrir o Excel para ler o nome da planilha: {e}")
#     st.stop()

# col1, col2 = st.columns(2)
# with col1:
#     x = st.number_input("Valor para B1", value=0.0, step=1.0, format="%.2f")
# with col2:
#     y = st.number_input("Valor para B2", value=0.0, step=1.0, format="%.2f")

# if st.button("Calcular"):
#     try:
#         # Compilar e avaliar SEM cache, para evitar vestígios de URL antiga
#         model = ModelCompiler().read_and_parse_archive(str(EXCEL_PATH))
#         ev = Evaluator(model)

#         ev.set_cell_value(f"{SHEET}!B1", x)
#         ev.set_cell_value(f"{SHEET}!B2", y)
#         result = ev.evaluate(f"{SHEET}!B3")

#         if isinstance(result, (int, float)):
#             st.success(f"Resultado em B3: {result:.2f}")
#         else:
#             st.warning(f"B3 retornou um valor não numérico: {result}")

#     except Exception as e:
#         st.error(f"Erro ao avaliar B3: {e}")

# INTERFACE TESTE ----------------------------------------------------------------------------------

import streamlit as st
from pathlib import Path

st.set_page_config(page_title="P&L – Credenciamento", layout="wide")

# ====== TOPO / BRANDING ======
logo_path = Path(__file__).parent / "images" / "logo.png"

top_left, top_right = st.columns([1, 3])
with top_left:
    if logo_path.exists():
        st.image(str(logo_path), caption=None, use_column_width=False, width=160)
    else:
        st.warning("Coloque sua logo em **images/logo.png**")
with top_right:
    st.markdown("<h3 style='margin-top:0'>Ferramenta P&L</h3>", unsafe_allow_html=True)

# ====== CONTROLES GERAIS ======
c1, c2 = st.columns(2)
with c1:
    antecipacao = st.radio("Antecipação?", ["SIM", "NÃO"], horizontal=True)
with c2:
    captura = st.radio("Captura", ["FÍSICO", "ECOMMERCE"], horizontal=True)

st.divider()

# ====== TABELA DE TAXAS POR BANDEIRA (texto no lugar dos logos) ======
st.subheader("Taxas por bandeira")

# Cabeçalho da tabela
h0, h1, h2, h3 = st.columns([2.0, 1.2, 1.2, 1.2])
with h0: st.markdown("<p style='text-align:center; font-weight:600;'>Bandeira</p>", unsafe_allow_html=True)
with h1: st.markdown("<p style='text-align:center; font-weight:600;'>Débito (%)</p>", unsafe_allow_html=True)
with h2: st.markdown("<p style='text-align:center; font-weight:600;'>Crédito à vista (%)</p>", unsafe_allow_html=True)
with h3: st.markdown("<p style='text-align:center; font-weight:600;'>Crédito parcelado (%)</p>", unsafe_allow_html=True)

# Lista de bandeiras apenas como TEXTO
bandeiras = ["Visa", "Mastercard", "Elo", "American Express", "Hipercard"]

taxas = {}
for b in bandeiras:
    c0, c1, c2, c3 = st.columns([2.0, 1.2, 1.2, 1.2])
    with c0:
        st.markdown(f"<p style='text-align:center; margin-top:10px;'>{b}</p>", unsafe_allow_html=True)
    with c1:
        deb = st.number_input(f"Débito % - {b}", value=0.00, step=0.01, format="%.2f",
                              label_visibility="collapsed", key=f"deb_{b}")
    with c2:
        av = st.number_input(f"Crédito à vista % - {b}", value=0.00, step=0.01, format="%.2f",
                             label_visibility="collapsed", key=f"avista_{b}")
    with c3:
        par = st.number_input(f"Crédito parcelado % - {b}", value=0.00, step=0.01, format="%.2f",
                              label_visibility="collapsed", key=f"parcel_{b}")
    taxas[b] = {"debito": deb, "cre

