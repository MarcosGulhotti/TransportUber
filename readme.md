

# Transportuber

Primeiro crie um diretorio pelo seu terminal:

<code>mkdir **NOME_DO_DIRETORIO**</code>

Em seguida, entre nessa diretorio para realizar o clone do projeto:

<code>cd **DIRETORIO_CRIADO_ACIMA**</code>

Faça o fork do projeto no gitlab e depois clone o projeto pelo seu terminal:

<code>git clone 'git@gitlab.com:**SEU_USUARIO**/transportuber.git'</code>

Acesse o projeto

<code>cd transportuber</code>

crie um ambiente virtual pro seu projeto:

<code>python -m venv venv</code>

Acesse esse ambiente virtual criado:

<code>source /venv/bin/active</code>

instale as dependencias do projeto que estão no arquivo requirements.txt:

<code>pip install -r requirements.txt</code>

Agora é só rodar a aplicação pelo comando:

<code>flask run</code>

E pronto, seu backend do projeto estará rodando no seu **localhost://5000**



