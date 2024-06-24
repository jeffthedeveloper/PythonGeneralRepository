import requests
from bs4 import BeautifulSoup

url = 'URL_DO_SEU_SITE'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extrair tags <script> (JavaScript)
scripts = soup.find_all('script')
for script in scripts:
    print(script.text)

# Extrair tags <style> (CSS)
styles = soup.find_all('style')
for style in styles:
    print(style.text)