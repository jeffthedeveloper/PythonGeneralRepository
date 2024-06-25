def primeGenerator(a, b):
    """Gera uma lista de números primos em um intervalo.

    Args:
        a: O primeiro número do intervalo.
        b: O último número do intervalo.

    Returns:
        Uma lista de números primos no intervalo.
    """

    primes = []
    for n in range(a, b + 1):
        if isPrime(n):
            primes.append(n)

    return primes
