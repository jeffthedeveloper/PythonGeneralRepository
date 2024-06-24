def sacar_dinheiro(valor):
  try:
    # Código que pode gerar exceções
    if valor > 1000:
      raise ValueError("Valor de saque muito alto")
    print(f"{valor} sacado com sucesso!")
  except ValueError as e:
    print(e)
