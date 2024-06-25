def toBinary(n):
    """
    Converte um número decimal para binário.

    Args:
        n: O número decimal a ser convertido.

    Returns:
        Um único número binário.
    """

    if n == 0:
        return 0

    bin = []
    while n > 0:
        bin.append(n % 2)
        n //= 2

    return int("".join([str(x) for x in bin[::-1]]), 2)


def main():
    n = int(input("Digite um número decimal: "))

    print(f"O número binário de {n} é: {toBinary(n)}")


if __name__ == "__main__":
    main()
