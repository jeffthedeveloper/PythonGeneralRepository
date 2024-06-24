# Importando bibliotecas
import pandas as pd 

# Carregando os dados CSV
dados = pd.read_csv("2018_Central_Park_Squirrel_Census_Squirrel_Data.csv")

# Contando os esquilos por cor de pelo
contagem_esquilos_cinza = len(dados[dados["Primary Fur Color"] == "Gray"])
contagem_esquilos_vermelhos = len(dados[dados["Primary Fur Color"] == "Cinnamon"])
contagem_esquilos_pretos = len(dados[dados["Primary Fur Color"] == "Black"])

# Criando um novo DataFrame e salvando como um CSV
dicionario_dados = {
    "Cor do Pelo": ["Cinza", "Vermelho", "Preto"],
    "Contagem": [contagem_esquilos_cinza, contagem_esquilos_vermelhos, contagem_esquilos_pretos]
}
df = pd.DataFrame(dicionario_dados)
df.to_csv("contagem_esquilos.csv", index=False)

# Explorando DataFrames e Séries

# Acessando colunas
coluna_temperatura = dados["temp"]
coluna_dia = dados["day"]
coluna_condicoes = dados["conditions"]

# Filtrando linhas
segunda_feira = dados[dados.day == "Monday"]
print(segunda_feira.conditions)  # Imprime as condições para segunda-feira
print(segunda_feira.temp)        # Imprime a temperatura para segunda-feira

# Convertendo temperaturas para Fahrenheit
temperatura_segunda = int(segunda_feira.temp)  # Acessar a temperatura de segunda-feira
temperatura_segunda_F = temperatura_segunda * 9/5 + 32  # Converter para Fahrenheit
print(temperatura_segunda_F)
