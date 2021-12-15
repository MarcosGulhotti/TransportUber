

# Transportuber

## **Introdução**

O projeto foi desenvolvido para sanar a dificuldade em que as pessoas tem para conseguirem transportar cargas por meio de fretistas ou transportadoras, o app simplifica essas relações gerando o contato direto do cliente com o prestador de serviço, assim diminuindo o custo do proprio serviço, e facilitando o dialogo entre motorista/dono-da-carga.
O aplicativo permite que o usuario localize sua carga em tempo real, conforme o motorista avança no trajeto, permite que o cliente avalie o preço antes de finalizar o negocio, tambem possui uma aplicação de webchat, para que o cliente esteja 24hrs conectado com o motorista e receba suas atualizações, e possui um sistema de previsao de entrega integrado diretamente com uma API do IBGE para controle de latitude/longitude da origem e do destino da carga.


## **Como Instalar**


Primeiro crie um diretorio pelo seu terminal:

<code>mkdir **NOME_DO_DIRETORIO**</code>

Em seguida, entre nessa diretorio para realizar o clone do projeto:

<code>cd **DIRETORIO_CRIADO_ACIMA**</code>

Faça o fork do projeto no gitlab e depois clone o projeto pelo seu terminal:

<code>git clone 'git@gitlab.com:**SEU_USUARIO**/transportuber.git'</code>

Acesse o projeto

<code>cd transportuber</code>


## **Como Rodar**


crie um ambiente virtual pro seu projeto:

<code>python -m venv venv</code>

Acesse esse ambiente virtual criado:

<code>source /venv/bin/active</code>

instale as dependencias do projeto que estão no arquivo requirements.txt:

<code>pip install -r requirements.txt</code>

Agora é só rodar a aplicação pelo comando:

<code>flask run</code>

E pronto, seu backend do projeto estará rodando no seu **localhost://5000**



