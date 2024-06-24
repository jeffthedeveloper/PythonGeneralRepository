import zipfile

# Abre o arquivo zip
with zipfile.ZipFile("arquivo.zip", "r") as zip:

    # Lista os arquivos do arquivo zip
    for arquivo in zip.namelist():

        # Verifica se o arquivo é um dos arquivos necessários
        if arquivo == "arquivo1.txt" or arquivo == "arquivo2.txt":

            # O arquivo está presente
            print("O arquivo {} está presente.".format(arquivo))

        else:

            # O arquivo não está presente
            print("O arquivo {} não está presente.".format(arquivo))
