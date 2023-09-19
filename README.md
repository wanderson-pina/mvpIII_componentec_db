# Minha API

Este Projeto se refere a criação de um Banco de Dados (SQLite), desenvolvido em Python, sendo o Componente "C" do Projeto de MVP.
Este Bando de Dados, irá receber dados de um Sistema de Compras fornecido pelo Front-End ( Componente A).

O objetivo aqui é ilustrar as orientações para a execução do código.

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
É necessário ir ao diretório raiz (Comando cd + diretório), pelo terminal, para poder executar os comandos descritos abaixo.

> É indicado o uso de ambientes virtuais:
    No Ambiente Windows foi utilizado o comando (python3 -m venv env), para a criação do ambiente virtual, e o comando ( env/scripts/activate), para ativar o ambiente virtual.

```
Instalar os Requirements para a execução do código:
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.



## Como executar através do Docker
Certifique-se de ter o Docker instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal. Execute como administrador o seguinte comando para construir a imagem Docker:

$ docker build -t rest-api .
Uma vez criada a imagem, para executar o container basta executar, como administrador, seguinte o comando:

$ docker run -p 5000:5000 rest-api
Uma vez executando, para acessar a API, basta abrir o http://localhost:5000/#/ no navegador.

Alguns comandos úteis do Docker
Para verificar se a imagem foi criada você pode executar o seguinte comando:

$ docker images
Caso queira remover uma imagem, basta executar o comando:

$ docker rmi <IMAGE ID>
Subistituindo o IMAGE ID pelo código da imagem

Para verificar se o container está em exceução você pode executar o seguinte comando:

$ docker container ls --all
Caso queira parar um conatiner, basta executar o comando:

$ docker stop <CONTAINER ID>
Subistituindo o CONTAINER ID pelo ID do conatiner

Caso queira destruir um conatiner, basta executar o comando:

$ docker rm <CONTAINER ID>



