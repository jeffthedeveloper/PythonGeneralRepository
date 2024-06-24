import pdfplumber

# Abrir o arquivo PDF
with pdfplumber.open("arquivo.pdf") as document:

    # Obter a primeira página
    page = document.get_page(0)

    # Obter a caixa de texto
    box = page.find_text("Nome do Cliente")

    # Extrair o texto da caixa de texto
    text = box.extract_text()

    # Imprimir o texto
    print(text)
