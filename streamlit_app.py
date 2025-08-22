import streamlit as st
from xlcalculator import ModelCompiler, Model

# Carrega o Excel (coloque no repositório junto com seu app)
EXCEL_FILE = "Book 1.xlsx"

st.title("Excel como motor de cálculo")

# Campos de entrada
x = st.number_input("Digite o valor de X:", value=0.0)
y = st.number_input("Digite o valor de Y:", value=0.0)

# Botão para calcular
if st.button("Calcular resultado"):
    try:
        # Compila o modelo do Excel
        model_compiler = ModelCompiler()
        new_model = model_compiler.read_and_parse_archive(EXCEL_FILE)
        model = Model(new_model)

        # Define os valores nas células
        model.set_value("Sheet1!B1", x)
        model.set_value("Sheet1!B2", y)

        # Avalia o resultado de B3
        resultado = model.evaluate("Sheet1!B3")

        st.success(f"O resultado calculado no Excel (B3) é: {resultado}")
    except Exception as e:
        st.error(f"Erro: {e}")
