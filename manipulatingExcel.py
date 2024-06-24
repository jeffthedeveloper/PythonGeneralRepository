import pandas as pd

# Carregar o arquivo Excel
df = pd.read_excel("meu_arquivo.xlsx")

# Obter a coluna C
coluna_c = df["C"]

Iterar sobre as células preenchidas da coluna C

for valor in coluna_c.dropna():
    # Processar o valor da célula
    print(valor)
    # ...

# Another Manner

import numpy as np

# Carregar o arquivo Excel
data = np.loadtxt("meu_arquivo.xlsx", dtype=str, skiprows=1)

# Obter a coluna C
coluna_c = data[:, 2]

# Iterar sobre as células preenchidas da coluna C
for valor in coluna_c:
    if valor != '':
        # Processar o valor da célula
        print(valor)
        # ...



#Now using openpyxl

from openpyxl import load_workbook

# Carregar o arquivo Excel
wb = load_workbook("meu_arquivo.xlsx")

# Acessar a planilha
sheet = wb.active

# Obter a coluna C
coluna_c = sheet['C']

# Iterar sobre as células preenchidas da coluna C
for cell in coluna_c[2:]:  # Ignora a primeira linha (cabeçalho)
    if cell.value is not None:
        # Processar o valor da célula
        print(cell.value)
        # ...
