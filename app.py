# Importando módulos necessários do Flask e o módulo random
from flask import Flask, render_template, request, session
import random

# Criando uma instância da aplicação Flask.
# O argumento __name__ ajuda a Flask a identificar a raiz do projeto.
app = Flask(__name__)

# Definindo uma chave secreta para a sessão.
# Esta chave é utilizada para manter as sessões do usuário seguras.
# É importante definir uma chave secreta forte e mantê-la protegida.
app.secret_key = 'sua_chave_secreta'

# Uma lista de palavras para o jogo de anagramas.
# Estas são as palavras que serão embaralhadas e apresentadas aos jogadores.
palavras = ['PYTHON', 'FLASK', 'DESENVOLVIMENTO', 'WEB', 'PROGRAMAÇÃO', 'DJANGO', 'CURSO', 'CARRO', 'JANELA']

# Definição da função gerar_anagrama, que aceita uma palavra como argumento.
def gerar_anagrama(palavra):

    # A palavra é convertida em uma lista de letras.
    palavra_embaralhada = list(palavra)

    # A função shuffle do módulo random é usada para embaralhar as letras da palavra.
    random.shuffle(palavra_embaralhada)

    # A lista de letras embaralhadas é unida de volta em uma string e retornada.
    # Isso resulta no anagrama da palavra original.
    return ''.join(palavra_embaralhada)



# A linha abaixo define uma rota em uma aplicação Flask.
# '@app.route('/')' é um decorador que diz ao Flask que sempre que
# um navegador acessar o endereço raiz da aplicação (indicado por '/'),
# a função 'inicio' deve ser chamada.
@app.route('/')
def inicio():

    # Esta função 'inicio' é chamada quando a rota raiz é acessada.

    # 'session' é um dicionário especial do Flask que permite armazenar
    # informações que são específicas para um usuário de uma sessão para outra.
    # Aqui, uma palavra aleatória é escolhida da lista 'palavras' definida anteriormente.
    # Esta palavra é armazenada na sessão sob a chave 'palavra'.
    session['palavra'] = random.choice(palavras)

    # A função 'gerar_anagrama' é chamada com a palavra escolhida.
    # O resultado, que é um anagrama da palavra, é armazenado na sessão
    # sob a chave 'anagrama'.
    session['anagrama'] = gerar_anagrama(session['palavra'])

    # A função 'render_template' é usada para renderizar um template HTML.
    # 'inicio.html' é o nome do arquivo de template que será renderizado.
    # O segundo argumento passado para 'render_template' é uma variável chamada 'anagrama'.
    # Esta variável está disponível no template HTML e contém o anagrama da palavra escolhida,
    # que é retirado da sessão.
    return render_template('inicio.html', anagrama=session['anagrama'])



# O decorador '@app.route' é usado para associar a função 'verificar'
# à rota '/verificar' no servidor web Flask. O parâmetro 'methods=['POST']'
# especifica que esta rota aceitará apenas solicitações POST, que são
# tipicamente usadas para enviar dados de formulários.
@app.route('/verificar', methods=['POST'])
def verificar():

    # Esta função é chamada quando um usuário envia um formulário para a rota '/verificar'.

    # 'request.form.get('resposta', '').strip().upper()' faz várias coisas:
    # 1. 'request.form' é um dicionário que contém os dados enviados pelo usuário.
    # 2. '.get('resposta', '')' obtém o valor associado à chave 'resposta' no formulário.
    #    Se 'resposta' não estiver presente, retorna uma string vazia ('').
    # 3. '.strip()' remove espaços em branco antes e depois da string obtida.
    # 4. '.upper()' converte a string para letras maiúsculas.
    resposta = request.form.get('resposta', '').strip().upper()

    # Aqui a palavra original armazenada na sessão (sob a chave 'palavra') é recuperada
    # e convertida em letras maiúsculas para garantir uma comparação adequada.
    palavra_secreta = session['palavra'].upper()

    # Esta estrutura condicional compara a resposta do usuário com a palavra secreta.
    if resposta == palavra_secreta:

        # Se a resposta for igual à palavra secreta, define uma mensagem de sucesso
        # e uma classe CSS para exibir a mensagem com um estilo de sucesso.
        mensagem = 'Correto! Você acertou.'
        alert_class = 'alert-success'

    else:

        # Se a resposta não for igual à palavra secreta, define uma mensagem de erro
        # e uma classe CSS para exibir a mensagem com um estilo de erro.
        mensagem = 'Incorreto. Tente novamente.'
        alert_class = 'alert-danger'

    # 'render_template' renderiza o template 'resultado.html', passando as variáveis
    # 'mensagem' e 'alert_class' para ele. Estas variáveis podem ser usadas no template
    # para mostrar ao usuário se ele acertou ou errou a resposta.
    return render_template('resultado.html', mensagem=mensagem, alert_class=alert_class)


# Verifica se este script está sendo executado como o principal e não como um módulo importado.
if __name__ == '__main__':

    # Inicia a aplicação Flask com o modo de depuração ativado.
    app.run(debug=True)