import PyPDF2
import re

# Abre o arquivo PDF
pdf_file = open("arquivo.pdf", "rb")

# Cria um objeto PDFReader
pdf_reader = PyPDF2.PdfFileReader(pdf_file)

# Obtém a primeira página do PDF
page = pdf_reader.getPage(0)

# Converte a página em texto
text = page.extractText()

# Procura por uma linha que contenha o texto "Total a recolher"
match = re.search(r"Total a recolher: \d+", text)

# Obtém o valor do total a recolher
total_a_recolher = match.group(1)

# Imprime o valor do total a recolher
print(total_a_recolher)


'''

arquivo_pdf = "arquivo.pdf"

localizado na mesma pasta

'''

'''

import os

# Obtém o caminho do arquivo PDF
arquivo_pdf = os.path.join(os.getcwd(), "arquivo.pdf")

localizado em uma outra pasta

'''
