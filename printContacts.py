contacts = [
    ('James', 42),
    ('Amy', 24),
    ('John', 31),
    ('Amanda', 63),
    ('Bob', 18)
]

name = input("Digite o nome da pessoa: ")

# Verifica se o nome está na lista
if name in contacts:
    # Imprime o nome e a idade
    print(f"{name} {contacts[contacts.index(name)][1]}")
else:
    # Imprime "Not found"
    print("Not found")

'''

Este código irá primeiro obter o nome da pessoa do usuário.
Em seguida, ele usará a expressão in para verificar se o nome está na lista.
Se o nome estiver na lista, o código irá imprimir o nome e a idade da pessoa. 
Se o nome não estiver na lista, o código irá imprimir "Not found".
'''