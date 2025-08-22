import streamlit as st
import requests
from io import BytesIO
from xlcalculator import ModelCompiler, Evaluator

# URL do arquivo Excel bruto do GitHub
EXCEL_URL = "https://github.com/itsmyvibee/blank-app/raw/main/Book%201.xlsx"

st.title("Excel como motor de cálculo direto do GitHub")

# Campos de entrada
x = st.number_input("Digite o valor de X:", value=0.0)
y = st.number_input("Digite o valor de Y:", value=0.0)

if st.button("Calcular resultado"):
    try:
        # Baixa o Excel do GitHub
        response = requests.get(EXCEL_URL)
        response.raise_for_status()  # garante que a requisição deu certo
        file_stream = BytesIO(response.content)

        # Compila o modelo do Excel
        compiler = ModelCompiler()
        model = compiler.read_and_parse_archive(file_stream)

        # Cria o avaliador
        evaluator = Evaluator(model)

        # Define os valores nas células
        evaluator.set_cell_value("Sheet1!B1", x)
        evaluator.set_cell_value("Sheet1!B2", y)

        # Avalia o resultado de B3
        resultado = evaluator.evaluate("Sheet1!B3")

        st.success(f"O resultado calculado no Excel (B3) é: {float(resultado)):.2f}")


    except Exception as e:
        st.error(f"Erro: {e}")
