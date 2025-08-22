import streamlit as st
import pandas as pd

# URL do Excel no GitHub (use o link "raw")
url = "https://raw.githubusercontent.com/itsmyvibee/blank-app/main/Book%201.xlsx"
#https://github.com/itsmyvibee/blank-app/blob/main/Book%201.xlsx

import streamlit as st
import pandas as pd
from xlcalculator import ModelCompiler, Model

# Carrega o Excel
model_compiler = ModelCompiler()
new_model = model_compiler.read_and_parse_archive("Book 1.xlsx")
model = Model(new_model)

# Inputs
x = st.number_input("Digite o valor de X:", value=0.0)
y = st.number_input("Digite o valor de Y:", value=0.0)

# Atualiza valores no modelo
model.set_value("Sheet1!B1", x)
model.set_value("Sheet1!B2", y)

# Calcula o resultado da célula B3
resultado = model.evaluate("Sheet1!B3")

st.write("### Resultado (célula B3):", resultado)


st.write("Prévia do arquivo:")
st.dataframe(df)
