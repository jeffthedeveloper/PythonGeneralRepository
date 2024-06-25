def convert(num):
    """
    Converte um número decimal para binário.

    Args:
        num: O número decimal a ser convertido.

    Returns:
        Uma lista de bits binários.
    """

    if num == 0:
        return [0]

    binary = []
    while num > 0:
        binary.append(num % 2)
        num //= 2

    return binary[::-1]
