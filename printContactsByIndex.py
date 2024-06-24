contacts = [
    ('James', 42),
    ('Amy', 24),
    ('John', 31),
    ('Amanda', 63),
    ('Bob', 18)
]

name = input("Digite o nome da pessoa: ")

# Verifica se o nome está na lista
index = contacts.index(name)

if index != -1:
    # Imprime o nome e a idade
    print(f"{name} {contacts[index][1]}")
else:
    # Imprime "Not found"
    print("Not found")
