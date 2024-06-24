def ler_arquivo(nome_arquivo):
  try:
    with open(nome_arquivo, "r") as arquivo:
      dados = arquivo.read()
  except FileNotFoundError:
    print("Arquivo não encontrado")
  finally:
    # Garante que o arquivo seja fechado
    arquivo.close()  # Não é necessário com o 'with open'
