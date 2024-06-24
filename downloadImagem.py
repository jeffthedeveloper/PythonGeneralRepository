from googleapiclient.discovery import build
from google.oauth2 import service_account

# Configure a autenticação com o Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Arquivo JSON com credenciais do Google Drive

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive = build('drive', 'v3', credentials=credentials)

# Função para baixar imagens e criar pastas
def baixar_imagens(pasta_principal, url_imagem, numero_imagem):
    # Criar nome da pasta para a imagem
    nome_pasta_imagem = f"{pasta_principal}/{numero_imagem}"

    # Criar pasta no Google Drive
    pasta = drive.files().create(
        body={
            'name': nome_pasta_imagem,
            'parents': ['root'],
            'mimeType': 'application/vnd.google-apps.folder'
        },
        fields='id'
    ).execute()
    pasta_id = pasta['id']

    # Baixar a imagem e salvar na pasta
    imagem_blob = requests.get(url_imagem).content
    drive.files().create(
        parentId=pasta_id,
        body={
            'name': f"{numero_imagem}.jpg",
            'mimeType': 'image/jpeg'
        },
        media_body=MediaFileUpload(imagem_blob, resumable=True)
    ).execute()

# Exemplo de uso
pasta_principal = "Torre/o.s rápida"  # Nome da pasta principal no Google Drive
url_imagem = "https://exemplo.com/imagem10076.jpg"  # URL da imagem
numero_imagem = 10076  # Número da imagem (extraído do URL)

baixar_imagens(pasta_principal, url_imagem, numero_imagem)
