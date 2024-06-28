# Importa o módulo principal da biblioteca Dash para criar a aplicação web.
import dash

# Importa componentes específicos da biblioteca Dash para criar elementos
# HTML e dashboards interativos.
from dash import dcc, html, Input, Output, State, dash_table, ALL

# Importa a classe PreventUpdate do Dash, que é usada para evitar atualizações
# desnecessárias dos callbacks.
from dash.exceptions import PreventUpdate

# Importa a biblioteca pandas.
# A biblioteca pandas é extensivamente usada para manipulação e análise de dados.
# Ela oferece estruturas de dados como DataFrames e Series para lidar com dados
# tabulares de forma eficiente.
import pandas as pd

# Importa a biblioteca numpy.
# Numpy é uma biblioteca para a linguagem Python que suporta arrays e matrizes multidimensionais.
# Ela também oferece uma coleção de funções matemáticas para operar nesses arrays.
import numpy as np

# Importa a biblioteca requests para fazer requisições HTTP.
import requests

# Importa o módulo win32com.client para interagir com o Microsoft Outlook.
import win32com.client as win32

# Importa o módulo pythoncom para inicialização do COM.
import pythoncom

# Importa o módulo os para operações relacionadas ao sistema operacional,
# como manipulação de arquivos.
import os

# Define a função buscar_cep que recebe um código postal como argumento.
def buscar_cep(codigo_postal):

    # O bloco try tenta executar as instruções contidas nele.
    try:

        # Usa a biblioteca requests para fazer uma requisição HTTP GET ao serviço de CEP.
        # A URL final será algo como "https://viacep.com.br/ws/01001000/json/".
        resposta = requests.get(f"https://viacep.com.br/ws/{codigo_postal}/json/")

        # Converte a resposta JSON para um dicionário Python usando o método .json() da resposta.
        dados = resposta.json()

        # Verifica se a chave "erro" está presente no dicionário.
        # Se estiver, significa que o CEP é inválido ou não foi encontrado.
        if "erro" in dados:
            return None  # Retorna None para indicar que o CEP é inválido ou não foi encontrado.

        # Monta uma string de endereço completo usando os dados recebidos.
        # dados['logradouro'], dados['bairro'], etc., são campos no dicionário retornado pela API.
        endereco_completo = f"{dados['logradouro']}, {dados['bairro']}, {dados['localidade']}, {dados['uf']}"

        # Retorna a string do endereço completo.
        return endereco_completo

    # O bloco except captura qualquer exceção que ocorra durante a execução do bloco try.
    except Exception as e:

        # Imprime a mensagem "Exceção: " seguida dos detalhes da exceção.
        print("Exceção: ", e)

        # Retorna None para indicar que ocorreu um erro durante a busca do CEP.
        return None


# Define a função enviar_email_com_outlook, que recebe um objeto
# linha (geralmente uma linha de um DataFrame).
def enviar_email_com_outlook(linha):

    # Inicializa o mecanismo COM (Component Object Model) do Windows.
    # Isso é necessário para usar a automação COM, especialmente em ambientes multithread.
    pythoncom.CoInitialize()

    # Cria um objeto Dispatch para a aplicação Microsoft Outlook.
    # Isso inicia o Outlook se ele ainda não estiver em execução.
    outlook = win32.Dispatch('outlook.application')

    # Cria um novo item de e-mail no Outlook.
    # O argumento 0 indica que um e-mail será criado (outros números
    # representam outros tipos de itens, como compromissos).
    email = outlook.CreateItem(0)

    # Define o campo "Assunto" do e-mail usando a chave 'Nome' do objeto linha.
    email.Subject = f"Assunto do E-mail para {linha['Nome']}"

    # Define o corpo do e-mail usando várias chaves do objeto linha.
    # Está sendo usado um string multilinha para formatar o corpo do e-mail de forma mais legível.
    email.Body = f"""Olá {linha['Nome']},

    Estamos muito felizes em ter você como nosso cliente. Abaixo seguem algumas informações úteis:

    - Endereço: {linha['Endereco']}
    - Celular: {linha['Celular']}
    - Telefone: {linha['Telefone']}

    Atenciosamente,
    Equipe da Empresa
    """

    # Define o campo "Para" do e-mail usando a chave 'Email' do objeto linha.
    email.To = linha['Email']

    # Salva o e-mail no Outlook.
    # Isso não envia o e-mail, apenas o salva no rascunho.
    # email.Send()
    # email.Display()
    email.Save()


# O bloco try tenta executar o código dentro dele.
try:

    # Usa a biblioteca pandas para ler uma planilha Excel chamada 'Dados_Agenda.xlsx' e a aba 'Dados'.
    # O DataFrame resultante é armazenado na variável df.
    df = pd.read_excel('Dados_Agenda.xlsx', sheet_name='Dados')

# O bloco except captura uma exceção específica (FileNotFoundError) caso o
# arquivo 'Dados_Agenda.xlsx' não seja encontrado.
except FileNotFoundError:

    # Se o arquivo não for encontrado, um novo DataFrame vazio com as colunas especificadas é criado.
    df = pd.DataFrame(columns=['CEP', 'Nome', 'Endereco', 'Celular', 'Telefone', 'Email'])

# Faz uma cópia profunda do DataFrame df e armazena na variável dataframe_original.
# Isso é feito para manter uma versão original dos dados, que pode ser útil para operações futuras.
dataframe_original = df.copy()

# Inicializa uma nova aplicação Dash e armazena na variável app.
# O argumento __name__ é usado para indicar o nome do script em execução como ponto de entrada para a aplicação.
app = dash.Dash(__name__)

# Define o layout da aplicação Dash. O layout é a estrutura visual da página web.
# O html.Div é um container que pode conter outros componentes HTML e Dash.
app.layout = html.Div([

    # html.H1 cria um cabeçalho de nível 1 na página web.
    # O texto "Agenda de Contatos" será o conteúdo desse cabeçalho.
    # O argumento style é um dicionário que contém estilos CSS. Aqui, ele centraliza o texto do cabeçalho.
    html.H1("Agenda de Contatos", style={'textAlign': 'center', 'color': 'blue'}),

    # Contêiner principal com estilo flex para alinhar os itens horizontalmente.
    html.Div(children=[

        # Contêiner para os campos de entrada com estilo flex para alinhar os itens na mesma linha.
        html.Div(children=[

            # Início do contêiner para o campo "CEP".
            # Este contêiner é um 'Div', que é um contêiner genérico para conteúdo de fluxo e não possui significado semântico específico.
            # Dentro deste 'Div', temos dois elementos filhos: um rótulo e um campo de entrada.
            html.Div(children=[

                # O primeiro filho é um rótulo 'Label' para o campo de entrada.
                # O rótulo é um elemento inline que representa uma legenda para um elemento de entrada de formulário.
                # A propriedade 'children' do rótulo é simplesmente o texto que será exibido ao usuário, neste caso, "CEP:".
                # Este texto ajuda o usuário a entender o que o campo de entrada subsequente espera como informação.
                html.Label("CEP:"),

                # O segundo filho é um campo de entrada 'Input'.
                # Este é um componente do Dash que representa um campo de entrada HTML onde os usuários podem inserir dados.
                # 'id' é um identificador único para o campo de entrada, que pode ser usado para referenciar o campo em callbacks no Dash.
                # O atributo 'type' especifica o tipo de dados que o campo de entrada aceitará, neste caso, 'text' significa que ele aceita texto.
                dcc.Input(id='cep', type='text')

                # Fechamento do 'Div' para o campo "CEP".
                # 'style' é um dicionário de estilos CSS aplicados a este 'Div'.
                # 'marginRight' define uma margem à direita do 'Div'. Isso é usado para criar espaço entre este 'Div' e qualquer elemento vizinho à direita.
                # Aqui, '10px' é a quantidade de espaço entre este contêiner de campo de entrada e o próximo.
            ], style={'marginRight': '10px'}),

            # Início do contêiner para o campo "Nome".
            # A estrutura é idêntica ao contêiner "CEP", com uma 'Div' contendo um 'Label' e um 'Input'.
            html.Div(children=[

                # Rótulo para o campo de entrada "Nome". Funciona da mesma forma que o rótulo para "CEP".
                html.Label("Nome:"),

                # Campo de entrada para o "Nome". 'id' e 'type' funcionam da mesma forma que no campo "CEP".
                dcc.Input(id='nome', type='text')

                # Fechamento do 'Div' para o campo "Nome".
                # A propriedade 'style' com 'marginRight' também é usada aqui para manter a consistência no layout,
                # separando este contêiner do próximo contêiner de campo de entrada.
            ], style={'marginRight': '10px'}),

            # Contêiner para o campo "Endereço".
            # A 'Div' é um bloco de contêiner genérico para outros elementos HTML. Aqui, serve como contêiner para o rótulo e o campo de entrada de "Endereço".
            html.Div(children=[

                # Cria um rótulo para o campo de entrada do endereço.
                # 'Label' representa uma etiqueta para o campo de entrada seguinte, facilitando a identificação do usuário sobre o que deve ser preenchido.
                html.Label("Endereço:"),

                # Cria um campo de entrada de texto.
                # 'Input' é um componente interativo onde os usuários podem digitar o endereço. 'id' é o identificador único para este campo no Dash.
                dcc.Input(id='endereco', type='text')

                # Define o estilo do contêiner Div.
                # 'marginRight' adiciona uma margem à direita do contêiner para separá-lo de elementos adjacentes, garantindo espaço entre os campos de entrada.
            ], style={'marginRight': '10px'}),

            # Contêiner para o campo "Celular".
            # Esta 'Div' atua como contêiner para o rótulo e campo de entrada do celular, seguindo o mesmo padrão do contêiner de "Endereço".
            html.Div(children=[

                # Rótulo para o campo de entrada de celular.
                # Fornece uma indicação clara para o usuário de que o dado a ser inserido é o número de celular.
                html.Label("Celular:"),

                # Campo de entrada para o número de celular.
                # Permite ao usuário inserir um número de celular. O 'id' associado a este campo permite que seja referenciado unicamente na aplicação.
                dcc.Input(id='celular', type='text')

                # Estilo para o contêiner 'Div' de "Celular".
                # Mantém a margem à direita consistente com os outros campos de entrada para alinhamento e espaçamento adequado no layout geral.
            ],  style={'marginRight': '10px'}),

            # Contêiner para o campo "Telefone".
            # Este 'Div' atua como um contêiner para agrupar visualmente o rótulo e o campo de entrada de "Telefone", facilitando a organização do layout.
            html.Div(children=[

                # Cria um rótulo 'Label' para o campo de entrada de "Telefone".
                # 'Label' serve como uma legenda textual para o campo de entrada, indicando ao usuário que informações são esperadas neste campo.
                html.Label("Telefone:"),

                # Define o campo de entrada 'Input' para o número de telefone.
                # 'id' é um identificador único no DOM que permite ao Dash identificar e interagir com este campo de entrada em callbacks.
                # 'type' é definido como 'text', que especifica que o usuário pode inserir texto neste campo.
                dcc.Input(id='telefone', type='text')

                # Aplica estilos CSS ao 'Div' do campo "Telefone".
                # 'marginRight' define uma margem à direita, criando um espaçamento entre este campo de entrada e qualquer elemento vizinho à direita.
            ],  style={'marginRight': '10px'}),

            # Contêiner para o campo "Email".
            # Similarmente, este 'Div' é utilizado para encapsular o rótulo e o campo de entrada de "Email".
            html.Div(children=[

                # Rótulo 'Label' para o campo de entrada de "Email".
                # O texto "Email:" serve como uma indicação clara do propósito do campo de entrada seguinte.
                html.Label("Email:"),

                # Campo de entrada 'Input' para o endereço de email.
                # Com o 'id' 'email', esse campo é identificado unicamente na aplicação para referência em operações de interação ou estilização.
                dcc.Input(id='email', type='text')

                # Neste caso, não estamos aplicando uma margem à direita.
                # Isso pode é o último campo de entrada na linha ou para manter um alinhamento específico dentro do layout.
            ],  style={}),

        ], style={
            'display': 'flex',  # Alinha os itens horizontalmente.
            'align-items': 'center',  # Centraliza os itens verticalmente.
            'width': '100%',  # Largura ajustada para 100% do contêiner pai.
            'padding': '15px',  # Preenchimento interno.
            'flex-wrap': 'wrap'  # Permite que os itens se envolvam conforme necessário.
        }),

    ], style={'width': '100%'}),
    # Alinhamento central com flexbox


    # Este é um novo container Div que contém a tabela de dados e os botões de ação.
    html.Div([

        # Contêiner Div filho que abriga exclusivamente a tabela de dados.
        html.Div([

            # Criando a tabela usando o componente dash_table.DataTable.
            dash_table.DataTable(

                # ID único para a tabela, útil para referenciar em callbacks.
                id='tabela',

                # Definindo as colunas da tabela com base nas colunas do DataFrame df.
                columns=[{"name": i, "id": i} for i in df.columns],

                # Preenchendo os dados na tabela usando os registros do DataFrame df.
                data=df.to_dict('records'),

                # Tornando as células da tabela editáveis.
                editable=True,

                # Permitindo que apenas uma linha seja selecionável de cada vez.
                row_selectable="single",

                # Nenhuma linha está selecionada inicialmente.
                selected_rows=[],

                # Permitindo que as linhas sejam deletáveis.
                row_deletable=True,

                # Estilos para o contêiner da tabela.
                style_table={
                    'overflowX': 'scroll',  # Rolagem horizontal se o conteúdo exceder a largura.
                    'border': 'thin lightgrey solid'  # Borda fina cinza claro ao redor da tabela.
                },

                # Estilos para o cabeçalho da tabela.
                style_header={
                    'backgroundColor': '#007BFF',  # Cor de fundo azul.
                    'color': 'white',  # Texto branco.
                    'fontWeight': 'bold',  # Texto em negrito.
                    'border': '1px solid white'  # Borda branca ao redor das células do cabeçalho.
                },

                # Estilos para as células da tabela.
                style_cell={
                    'textAlign': 'left',  # Alinhamento do texto à esquerda.
                    'padding': '8px',  # Preenchimento interno de 8px.
                    'border': '1px solid lightgrey'  # Borda cinza claro ao redor das células.
                },

                # Estilos condicionais para as células da tabela.
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},  # Condição para linhas ímpares.
                        'backgroundColor': 'lightgrey'  # Cor de fundo cinza claro para linhas ímpares.
                    }
                ],
            )

            # Estilos para o contêiner Div que contém a tabela.
        ], style={
            'width': '75%',  # Ocupa 75% da largura total disponível.
            'display': 'inline-block',  # Disposto como um bloco inline.
            'vertical-align': 'top',  # Alinhamento vertical ao topo.
            'padding': '15px'  # Preenchimento de 15px em todos os lados.
        }),


        # Este trecho de código cria um novo container Div que conterá apenas botões de ação.
        # html.Div é um componente que cria um novo bloco ou seção na página web.
        html.Div([

            # Criando um botão com o texto "Adicionar".
            html.Button(

                "Adicionar",  # Texto exibido no botão.

                # ID único para o botão, que pode ser usado para referenciar este botão em futuros callbacks.
                id='botao_adicionar',

                # Definindo o estilo CSS do botão.
                style={
                    'width': '100%',  # Ocupa 100% da largura do contêiner pai.
                    'marginBottom': '10px',  # Margem inferior de 10 pixels para separá-lo de outros elementos abaixo.
                    'backgroundColor': '#007BFF',  # Cor de fundo azul.
                    'color': 'white',  # Cor do texto branco.
                    'fontSize': '20px'
                    # Tamanho da fonte definido como 20 pixels. Pode ser ajustado conforme necessário.
                }
            ),

            # Um novo botão é criado com o texto "Alterar".
            # Assim como o botão anterior, este botão tem um id único e um estilo específico.
            html.Button(

                "Alterar",  # Texto exibido no botão.

                # ID único para o botão, que pode ser usado para referenciar este botão em futuros callbacks.
                id='botao_alterar',

                # Definindo o estilo CSS do botão.
                style={
                    'width': '100%',  # Ocupa 100% da largura do contêiner pai.
                    'marginBottom': '10px',  # Margem inferior de 10 pixels para separá-lo de outros elementos abaixo.
                    'backgroundColor': '#007BFF',  # Cor de fundo azul.
                    'color': 'white',  # Cor do texto branco.
                    'fontSize': '20px'
                    # Tamanho da fonte definido como 20 pixels. Pode ser ajustado conforme necessário.
                }
            ),

            # Mais um botão é criado com o texto "Pesquisar".
            html.Button(

                "Pesquisar",  # Texto exibido no botão.

                # ID único para o botão, que pode ser usado para referenciar este botão em futuros callbacks.
                id='botao_pesquisar',

                # Definindo o estilo CSS do botão.
                style={
                    'width': '100%',  # Ocupa 100% da largura do contêiner pai.
                    'marginBottom': '10px',  # Margem inferior de 10 pixels para separá-lo de outros elementos abaixo.
                    'backgroundColor': '#007BFF',  # Cor de fundo azul.
                    'color': 'white',  # Cor do texto branco.
                    'fontSize': '20px'
                    # Tamanho da fonte definido como 20 pixels. Pode ser ajustado conforme necessário.
                }
            ),

            # O botão "Excluir" é criado a seguir.
            html.Button(

                "Excluir",  # Texto exibido no botão.

                # ID único para o botão, que pode ser usado para referenciar este botão em futuros callbacks.
                id='botao_excluir',

                # Definindo o estilo CSS do botão.
                style={
                    'width': '100%',  # Ocupa 100% da largura do contêiner pai.
                    'marginBottom': '10px',  # Margem inferior de 10 pixels para separá-lo de outros elementos abaixo.
                    'backgroundColor': '#007BFF',  # Cor de fundo azul.
                    'color': 'white',  # Cor do texto branco.
                    'fontSize': '20px'
                    # Tamanho da fonte definido como 20 pixels. Pode ser ajustado conforme necessário.
                }
            ),

            # O botão "Limpar Filtro" é para redefinir quaisquer filtros aplicados.
            html.Button(

                "Limpar Filtro",  # Texto exibido no botão.

                # ID único para o botão, que pode ser usado para referenciar este botão em futuros callbacks.
                id='botao_limpar',

                # Definindo o estilo CSS do botão.
                style={
                    'width': '100%',  # Ocupa 100% da largura do contêiner pai.
                    'marginBottom': '10px',  # Margem inferior de 10 pixels para separá-lo de outros elementos abaixo.
                    'backgroundColor': '#007BFF',  # Cor de fundo azul.
                    'color': 'white',  # Cor do texto branco.
                    'fontSize': '20px'
                    # Tamanho da fonte definido como 20 pixels. Pode ser ajustado conforme necessário.
                }
            ),

            # O botão "Exportar para Excel" serve para iniciar um processo de exportação de dados.
            html.Button(

                "Exportar para Excel",  # Texto exibido no botão.

                # ID único para o botão, que pode ser usado para referenciar este botão em futuros callbacks.
                id='botao_exportar',

                # Definindo o estilo CSS do botão.
                style={
                    'width': '100%',  # Ocupa 100% da largura do contêiner pai.
                    'marginBottom': '10px',  # Margem inferior de 10 pixels para separá-lo de outros elementos abaixo.
                    'backgroundColor': '#007BFF',  # Cor de fundo azul.
                    'color': 'white',  # Cor do texto branco.
                    'fontSize': '20px'
                    # Tamanho da fonte definido como 20 pixels. Pode ser ajustado conforme necessário.
                }
            ),

            # O último botão, "Criar E-mail", servirá para enviar e-mails.
            html.Button(

                "Criar E-mail",  # Texto exibido no botão.

                # ID único para o botão, que pode ser usado para referenciar este botão em futuros callbacks.
                id='botao_email',

                # Definindo o estilo CSS do botão.
                style={
                    'width': '100%',  # Ocupa 100% da largura do contêiner pai.
                    'marginBottom': '10px',  # Margem inferior de 10 pixels para separá-lo de outros elementos abaixo.
                    'backgroundColor': '#007BFF',  # Cor de fundo azul.
                    'color': 'white',  # Cor do texto branco.
                    'fontSize': '20px'
                    # Tamanho da fonte definido como 20 pixels. Pode ser ajustado conforme necessário.
                }
            ),

            # O estilo desta Div é configurado para que ela ocupe 25% da largura total disponível da página.
            # Ela é exibida como um bloco inline para que possa ficar ao lado de outros elementos.
            # O alinhamento vertical é definido como 'top', o que significa que ela se alinhará ao topo do seu container pai.
            # Um padding de 15 pixels é adicionado para algum espaço extra ao redor do conteúdo.
            # Por fim, o texto dentro desta Div é centralizado usando 'textAlign': 'center'.
        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '15px',
                  'textAlign': 'center'}),

        # Este é o estilo da Div principal que contém a tabela e os botões.
        # Ela é configurada para ocupar 100% da largura disponível e para dispor seus elementos filhos em uma linha (flex).
    ], style={'width': '100%', 'display': 'flex'}),
])

# O layout agora está completo. Todos os componentes HTML e Dash estão aninhados em Divs,
# o que permite um controle preciso sobre o layout e o estilo da aplicação.


# @app.callback é um decorador que define uma função de callback em uma aplicação Dash.
# A função decorada será chamada sempre que os componentes especificados nos argumentos
# Input, Output e State forem modificados.
@app.callback(

    # A lista de Outputs define os componentes cujas propriedades serão atualizadas pelo callback.
    # Cada Output é um objeto que leva dois argumentos: o id do componente e a propriedade que será atualizada.
    [Output('tabela', 'data'),  # Atualiza os dados na tabela.
     Output('cep', 'value'),  # Atualiza o valor do campo CEP.
     Output('nome', 'value'),  # Atualiza o valor do campo Nome.
     Output('endereco', 'value'),  # Atualiza o valor do campo Endereço.
     Output('celular', 'value'),  # Atualiza o valor do campo Celular.
     Output('telefone', 'value'),  # Atualiza o valor do campo Telefone.
     Output('email', 'value')],  # Atualiza o valor do campo Email.

    # A lista de Inputs define os componentes que, quando interagidos, irão disparar o callback.
    # Semelhante ao Output, cada Input é um objeto que leva dois argumentos: o id do componente e a propriedade que irá disparar o callback.
    [Input('botao_adicionar', 'n_clicks'),  # Número de cliques no botão Adicionar.
     Input('botao_alterar', 'n_clicks'),  # Número de cliques no botão Alterar.
     Input('botao_pesquisar', 'n_clicks'),  # Número de cliques no botão Pesquisar.
     Input('botao_excluir', 'n_clicks'),  # Número de cliques no botão Excluir.
     Input('botao_limpar', 'n_clicks'),  # Número de cliques no botão Limpar Filtro.
     Input('botao_exportar', 'n_clicks'),  # Número de cliques no botão Exportar para Excel.
     Input('botao_email', 'n_clicks'),  # Número de cliques no botão Criar E-mail.
     Input('cep', 'value'),  # Valor atual do campo CEP.
     Input('tabela', 'active_cell'),  # Informações sobre a célula ativa na tabela.
     Input('tabela', 'data_previous')],  # Dados anteriores da tabela antes da última edição.

    # A lista de States contém os componentes cujos estados atuais serão passados para o callback, mas que não disparam o callback.
    # Assim como em Output e Input, cada State é um objeto que leva dois argumentos: o id do componente e a propriedade que será passada.
    [State('cep', 'value'),  # Valor atual do campo CEP.
     State('nome', 'value'),  # Valor atual do campo Nome.
     State('endereco', 'value'),  # Valor atual do campo Endereço.
     State('celular', 'value'),  # Valor atual do campo Celular.
     State('telefone', 'value'),  # Valor atual do campo Telefone.
     State('email', 'value'),  # Valor atual do campo Email.
     State('tabela', 'data'),  # Dados atuais da tabela.
     State('tabela', 'selected_rows')]  # Índices das linhas selecionadas na tabela.
)

# A função atualizar_tabela é definida como o callback que será disparado quando os Inputs e States especificados forem alterados.
def atualizar_tabela(cliques_adicionar, cliques_alterar, cliques_pesquisar, cliques_excluir, cliques_limpar,
                     cliques_exportar, cliques_email, valor_cep, celula_ativa, dados_anteriores, cep, nome, endereco,
                     celular, telefone, email, dados_tabela, linhas_selecionadas):

    # A palavra-chave global é usada para indicar que a variável dataframe_original é uma variável global.
    # Isso permite que a função modifique a variável fora do seu escopo local.
    global dataframe_original

    # dash.callback_context fornece informações sobre o componente que disparou o callback.
    # Isso é útil quando você tem múltiplos Inputs e precisa saber qual deles foi acionado.
    contexto = dash.callback_context

    # Se nenhum Input foi disparado (por exemplo, na inicialização da aplicação), a função raise PreventUpdate é chamada.
    # Isso evita que o callback atualize qualquer Output, efetivamente "cancelando" a execução do callback.
    if not contexto.triggered:
        raise PreventUpdate

    # O Input que disparou o callback é identificado e o seu id é armazenado na variável input_ativado.
    # A propriedade 'prop_id' contém o id e a propriedade do Input que disparou o callback, separados por um ponto.
    # O método split('.') é usado para separar o id do nome da propriedade, e somente o id é usado.
    input_ativado = contexto.triggered[0]['prop_id'].split('.')[0]

    # Um novo DataFrame df é criado a partir dos dados atuais da tabela.
    # Isso é feito para que qualquer modificação nos dados possa ser feita neste DataFrame local, sem afetar os dados originais.
    df = pd.DataFrame(dados_tabela)

    # Este bloco de código é executado se o Input que disparou o callback é o campo 'cep'.
    # A variável input_ativado contém o id do componente que disparou o callback, que neste caso é 'cep'.
    if input_ativado == 'cep':

        # https://www.consultarcep.com.br/rj/rio-de-janeiro/

        # A função buscar_cep é chamada com o valor atual do campo 'cep' (valor_cep) como argumento.
        # Esta função é responsável por buscar informações de endereço com base no CEP fornecido.
        endereco = buscar_cep(valor_cep)

        # Se a função buscar_cep retornar None (o que significa que o CEP não foi encontrado),
        # a variável endereco é atualizada com a string "CEP não encontrado".
        if endereco is None:
            endereco = "CEP não encontrado"

        # O callback então retorna as atualizações para os Outputs.
        # Neste caso, apenas o valor do campo 'endereco' é atualizado com o valor da variável endereco.
        # Todos os outros Outputs são mantidos como estão, o que é indicado por dash.no_update.
        return dash.no_update, dash.no_update, dash.no_update, endereco, dash.no_update, dash.no_update, dash.no_update

    # Este bloco de código é executado se o Input que disparou o callback é a 'tabela'.
    # A variável input_ativado contém o id do componente que disparou o callback, que neste caso é 'tabela'.
    elif input_ativado == 'tabela':

        # Verifica se a variável dados_anteriores não é None.
        # dados_anteriores contém o estado anterior dos dados da tabela antes de qualquer edição.
        if dados_anteriores is not None:

            # Compara o tamanho dos dados anteriores e dos dados atuais da tabela.
            # Se os dados anteriores são maiores em tamanho, isso indica que uma linha foi excluída.
            if len(dados_anteriores) > len(dados_tabela):

                # Salva o DataFrame df atualizado como um arquivo Excel.
                df.to_excel('Dados_Agenda.xlsx', sheet_name='Dados', index=False)

                # Retorna os dados atualizados da tabela e limpa todos os outros campos.
                return df.to_dict('records'), '', '', '', '', '', ''

        # Verifica se a variável celula_ativa não é None.
        # celula_ativa contém informações sobre a célula que está atualmente ativa (selecionada) na tabela.

        if celula_ativa is not None:

            # Extrai o índice da linha da célula ativa.
            linha = celula_ativa['row']

            # Usa o índice da linha para obter os dados da linha correspondente no DataFrame df.
            dados_selecionados = df.iloc[linha]

            # Retorna os valores dos campos CEP, Nome, Endereço, Celular, Telefone e Email dessa linha específica.
            # dash.no_update é usado para os outros Outputs que não precisam ser atualizados.
            return dash.no_update, dados_selecionados['CEP'], dados_selecionados['Nome'], dados_selecionados[
                'Endereco'], dados_selecionados['Celular'], dados_selecionados['Telefone'], dados_selecionados['Email']



    # Este bloco de código é executado se o Input que disparou o callback é o botão 'botao_adicionar'.
    # A variável input_ativado contém o id do componente que disparou o callback, que neste caso é 'botao_adicionar'.
    elif input_ativado == 'botao_adicionar':

        # Um novo DataFrame chamado nova_linha é criado para armazenar os valores dos campos de entrada: cep, nome, endereco, celular, telefone e email.
        # As colunas deste novo DataFrame são as mesmas que as do DataFrame df existente.
        nova_linha = pd.DataFrame([[cep, nome, endereco, celular, telefone, email]], columns=df.columns)

        # O novo DataFrame nova_linha é concatenado ao DataFrame df existente.
        # O parâmetro ignore_index=True reindexa o DataFrame resultante para que os índices sejam contínuos.
        df = pd.concat([df, nova_linha], ignore_index=True)

        # O DataFrame df atualizado é salvo como um arquivo Excel com o nome 'Dados_Agenda.xlsx' e a aba 'Dados'.
        # O parâmetro index=False evita que os índices do DataFrame sejam salvos no arquivo Excel.
        df.to_excel('Dados_Agenda.xlsx', sheet_name='Dados', index=False)

        # O callback retorna os dados atualizados da tabela e limpa todos os outros campos.
        # O DataFrame df é convertido para um dicionário de registros para ser compatível com a tabela Dash.
        # Todos os outros campos são limpos, retornando strings vazias.
        return df.to_dict('records'), '', '', '', '', '', ''


    # Este bloco de código é ativado quando o Input que disparou o callback é o botão 'botao_alterar'.
    # A variável input_ativado contém o id do componente que disparou o callback, neste caso, 'botao_alterar'.
    elif input_ativado == 'botao_alterar':

        # Verifica se alguma linha foi selecionada na tabela.
        # Se nenhuma linha foi selecionada (ou seja, linhas_selecionadas é None ou sua extensão é 0),
        # a atualização é impedida usando o comando PreventUpdate.
        if linhas_selecionadas is None or len(linhas_selecionadas) == 0:
            raise PreventUpdate

        # Itera sobre cada índice de linha selecionada na variável linhas_selecionadas.
        for i in linhas_selecionadas:

            # Atualiza o valor da coluna 'CEP' na linha i do DataFrame df se o valor de cep não for None.
            if cep is not None:
                df.loc[i, 'CEP'] = cep

            # Similarmente, atualiza os valores das outras colunas com base nas entradas fornecidas, se elas não forem None.
            if nome is not None:
                df.loc[i, 'Nome'] = nome
            if endereco is not None:
                df.loc[i, 'Endereco'] = endereco
            if celular is not None:
                df.loc[i, 'Celular'] = celular
            if telefone is not None:
                df.loc[i, 'Telefone'] = telefone
            if email is not None:
                df.loc[i, 'Email'] = email

        # Após realizar todas as alterações, o DataFrame df atualizado é salvo como um arquivo Excel.
        df.to_excel('Dados_Agenda.xlsx', sheet_name='Dados', index=False)

        # Finalmente, o callback retorna os dados atualizados da tabela e limpa todos os outros campos de entrada.
        # O DataFrame df é convertido para um dicionário de registros para atualizar a tabela da interface do usuário.
        return df.to_dict('records'), '', '', '', '', '', ''


    # Este bloco de código é ativado quando o botão 'Pesquisar' é clicado.
    elif input_ativado == 'botao_pesquisar':

        # Cria uma máscara booleana inicial com todos os valores como True.
        # Essa máscara terá o mesmo número de linhas que o DataFrame 'df'.
        # A ideia é que, inicialmente, todos os registros são elegíveis para serem retornados pela pesquisa.
        final_mask = np.array([True] * len(df))

        # Para cada campo de entrada, atualizamos a máscara booleana para refletir os registros que satisfazem a condição.
        # Utilizamos a operação 'logical_and' para combinar a máscara atual com a nova condição.
        # Assim, a máscara final só conterá 'True' para os registros que satisfazem todas as condições.

        # Atualiza a máscara se o campo 'Nome' não estiver vazio.
        if nome:
            final_mask = np.logical_and(final_mask, df['Nome'].str.contains(nome, case=False))

        # Atualiza a máscara se o campo 'CEP' não estiver vazio.
        if cep:
            final_mask = np.logical_and(final_mask, df['CEP'].str.contains(cep, case=False))

        # Atualiza a máscara se o campo 'Endereco' não estiver vazio.
        if endereco:
            final_mask = np.logical_and(final_mask, df['Endereco'].str.contains(endereco, case=False))

        # Atualiza a máscara se o campo 'Celular' não estiver vazio.
        if celular:
            final_mask = np.logical_and(final_mask, df['Celular'].str.contains(celular, case=False))

        # Atualiza a máscara se o campo 'Telefone' não estiver vazio.
        if telefone:
            final_mask = np.logical_and(final_mask, df['Telefone'].str.contains(telefone, case=False))

        # Atualiza a máscara se o campo 'Email' não estiver vazio.
        if email:
            final_mask = np.logical_and(final_mask, df['Email'].str.contains(email, case=False))

        # Aplica a máscara booleana final ao DataFrame para filtrar os registros.
        # Isso resulta em um novo DataFrame que contém apenas os registros que satisfazem todas as condições de pesquisa.
        resultado_pesquisa = df[final_mask]

        # Retorna o resultado da pesquisa como um dicionário de registros.
        # Os argumentos 'dash.no_update' indicam que os outros outputs do callback não devem ser atualizados.
        return resultado_pesquisa.to_dict(
            'records'), dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update


    # Este bloco de código é ativado quando o botão 'botao_excluir' é pressionado.
    # A variável 'input_ativado' conterá o valor 'botao_excluir', indicando que este botão disparou o callback.
    elif input_ativado == 'botao_excluir':

        # Primeiramente, verifica se qualquer linha foi selecionada na tabela.
        # 'linhas_selecionadas' é uma lista dos índices das linhas selecionadas.
        # Se nenhuma linha for selecionada, o código impede qualquer atualização adicional usando 'raise PreventUpdate'.
        if linhas_selecionadas is None or len(linhas_selecionadas) == 0:
            raise PreventUpdate

        # O método 'drop' do DataFrame é utilizado para excluir as linhas selecionadas.
        # 'axis=0' especifica que queremos excluir linhas (e não colunas).
        # 'inplace=True' modifica o DataFrame original.
        df.drop(linhas_selecionadas, axis=0, inplace=True)

        # O índice do DataFrame é redefinido e o antigo índice é descartado.
        df.reset_index(drop=True, inplace=True)

        # O DataFrame modificado é salvo em um arquivo Excel.
        df.to_excel('Dados_Agenda.xlsx', sheet_name='Dados', index=False)

        # Retorna os dados atualizados para preencher a tabela na interface do usuário.
        # O DataFrame 'df' é convertido para um formato de dicionário de registros.
        # Todos os outros campos de entrada são limpos e retornam strings vazias.
        return df.to_dict('records'), '', '', '', '', '', ''


    # Este bloco é ativado quando o botão 'botao_limpar' é clicado.
    # A variável input_ativado conterá o valor 'botao_limpar', indicando que este botão disparou o callback.
    elif input_ativado == 'botao_limpar':

        # Um bloco try-except é utilizado para capturar qualquer erro que
        # possa ocorrer durante a leitura do arquivo Excel.
        try:

            # Tenta ler o arquivo 'Dados_Agenda.xlsx' na planilha 'Dados' para um novo DataFrame chamado novo_df.
            novo_df = pd.read_excel('Dados_Agenda.xlsx', sheet_name='Dados')

            # Cria uma cópia profunda do novo DataFrame para a variável global dataframe_original.
            # Isso é feito para que qualquer operação futura não afete o DataFrame original.
            dataframe_original = novo_df.copy()

            # Retorna os dados atualizados para preencher a tabela na interface do usuário.
            # O DataFrame dataframe_original é convertido em um dicionário de registros para ser compatível com a tabela Dash.
            # Todos os outros campos de entrada são limpos e retornam strings vazias.
            return dataframe_original.to_dict('records'), '', '', '', '', '', ''

        # Se ocorrer um FileNotFoundError (por exemplo, se o arquivo Excel não for encontrado),
        # o código entrará no bloco except.
        except FileNotFoundError:

            # Neste caso, retorna um dash.no_update para a tabela, indicando que os dados da tabela não devem ser atualizados.
            # Todos os outros campos de entrada são limpos e retornam strings vazias.
            return dash.no_update, '', '', '', '', '', ''


    # Este bloco de código é ativado quando o botão 'botao_exportar' é clicado.
    # A variável 'input_ativado' conterá o valor 'botao_exportar', sinalizando que
    # este botão disparou o callback.
    elif input_ativado == 'botao_exportar':

        # Um bloco try-except é usado para capturar qualquer exceção que possa
        # ocorrer durante a exportação dos dados para o Excel.
        try:

            # A função os.path.abspath é usada para obter o caminho absoluto onde o arquivo Excel exportado será salvo.
            caminho_exportacao = os.path.abspath('Dados_Agenda_Exportado.xlsx')

            # O método to_excel do DataFrame 'df' é usado para salvar os dados no arquivo Excel.
            # O parâmetro 'sheet_name' especifica o nome da aba do Excel e 'index=False' evita que os índices do DataFrame sejam exportados.
            df.to_excel(caminho_exportacao, sheet_name='Dados', index=False)

        # O bloco except captura qualquer tipo de exceção e imprime uma mensagem de erro.
        except Exception as e:
            print(f"Erro ao exportar: {e}")

        # Independentemente de a exportação ser bem-sucedida ou não, este
        # retorno garante que a tabela e os campos de entrada não sejam atualizados.
        return dash.no_update, '', '', '', '', '', ''


    # Este bloco de código é ativado quando o botão 'botao_email' é pressionado na interface do usuário.
    # A variável 'input_ativado' terá o valor 'botao_email', indicando que este botão é o responsável por disparar o callback.
    elif input_ativado == 'botao_email':

        # Um bloco try-except é usado para capturar qualquer exceção que possa ocorrer durante o envio de e-mails.
        try:

            # O método 'iterrows()' do DataFrame 'df' é usado para iterar sobre todas as linhas do DataFrame.
            # Cada 'linha' é uma Series do Pandas que contém todos os dados de uma linha individual do DataFrame.
            for _, linha in df.iterrows():

                # A função 'enviar_email_com_outlook' é chamada para cada linha do DataFrame.
                # Esta função foi definida anteriormente no script para enviar um e-mail usando a API do Outlook.
                enviar_email_com_outlook(linha)

        # O bloco 'except' captura qualquer tipo de exceção que possa ocorrer durante o envio de e-mails.
        # A exceção é armazenada na variável 'e', e uma mensagem de erro é impressa no console.
        except Exception as e:
            print(f"Erro ao criar e-mails: {e}")

        # Independentemente do sucesso ou falha do envio de e-mails, o código retorna 'dash.no_update' para todos os Outputs.
        # Isso significa que a interface do usuário não será atualizada.
        return dash.no_update, '', '', '', '', '', ''

    # Este é o retorno padrão se nenhum dos blocos 'elif' anteriores for ativado.
    # Ele evita qualquer atualização na interface do usuário.
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

# Este é o ponto de entrada principal do script.
# Ele inicia o servidor Dash na porta 8055 e com a depuração ativada.
if __name__ == '__main__':
    app.run_server(debug=True, port=8055)