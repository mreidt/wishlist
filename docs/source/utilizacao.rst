Utilização
==========

As instruções abaixo referem-se ao uso em distribuições Unix.

O projeto roda localmente utilizando Docker, portanto é necessário ter essa ferramenta instalada.

Após fazer o clone do projeto do Github, é necessário configurar o seu ambiente local, criando um arquivo .env (seguir exemplo disponibilizado .env.example).

Para rodar localmente o projeto, basta executar os comandos:
::

	$ docker build .
	$ docker-compose up