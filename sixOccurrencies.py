def numero_de_ocorrencias(limite):
  """Retorna o número de ocorrências do dígito 6 nos números de 0 a `limite`."""
  total = 0
  for i in range(1, limite + 1):
    total += numero_de_ocorrencias_em_um_numero(i)
  return total

def numero_de_ocorrencias_em_um_numero(numero):
  """Retorna o número de ocorrências do dígito 6 em um número."""
  if numero < 10:
    if numero == 6:
      return 1
    else:
      return 0
  else:
    dezenas = numero // 10
    unidades = numero % 10
    if unidades == 6:
      return 1
    elif dezenas == 6:
      return 2
    else:
      return 0

print(numero_de_ocorrencias(1536))
