def isprime(x):
  """Verifica se um número é primo.

  Args:
    x: O número a ser verificado.

  Returns:
    True se o número for primo, False caso contrário.
  """

  if x <= 1:
    return False

  for i in range(2, int(x ** 0.5) + 1):
    if x % i == 0:
      return False

  return True


def primeGenerator(inicial, final):
  """Gera uma lista de números primos em um intervalo.

  Args:
    inicial: O primeiro número do intervalo.
    final: O último número do intervalo.

  Yields:
    Os números primos no intervalo.
  """

  for i in range(inicial, final + 1):
    if isprime(i):
      yield i
